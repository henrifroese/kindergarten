import random
from typing import Any

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash
from plotly.subplots import make_subplots

from kindergarten.constants import MAX_NUM_TRACES
from kindergarten.tab import Tab


class Kindergarten:
    def __init__(self, num_traces=MAX_NUM_TRACES):
        self.tabs = [Tab(tab_id=i) for i in range(num_traces)]

        self.app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self._initialize_app()

    def _initialize_app(self):
        self.app.config.suppress_callback_exceptions = True

        self.app.layout = dbc.Container(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(
                            self.tabs[i].component(), label="Trace {}".format(i), id="tab-{}".format(i)
                        )
                        for i in range(len(self.tabs))
                    ],
                    id="tabs",
                ),
                dbc.Row(dbc.Col(dcc.Graph(id="graph"))),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(
                                dbc.Button(
                                    "Print Code",
                                    id="print-code",
                                    color="secondary",
                                    n_clicks=0,
                                    style={"margin-top": 15},
                                )
                            ),
                            html.Div(
                                id="hidden-div",
                                style={"display": "none"},
                            ),
                        ]
                    )
                ),
            ],
            fluid=True,
            className="dash-bootstrap",
        )

        for i in range(len(self.tabs)):

            @self.app.callback(
                Output("selector-{}".format(i), "children"),
                [Input("graph-type-{}".format(i), "value"), Input("dataframe-{}".format(i), "value")],
                prevent_initial_call=True,
            )
            def _on_graph_type_or_dataframe_change_update_selector(
                graph_type, dataframe_name
            ):
                triggered_component_id = callback_context.triggered_id
                kw, tab_id = triggered_component_id.rsplit("-", 1)

                self.tabs[int(tab_id)].update_option(
                    kw, graph_type if kw == "graph-type" else dataframe_name
                )
                return self.tabs[int(tab_id)].options_component()

        all_options = sum(
            [list(tab.options.values()) for tab in self.tabs],
            [],
        )
        inputs = (
            [Input(option.id, "value") for option in all_options]
            + [Input("graph-type-{}".format(i), "value") for i in range(len(self.tabs))]
            + [Input("dataframe-{}".format(i), "value") for i in range(len(self.tabs))]
        )
        input_names = (
            [option.id for option in all_options]
            + ["graph-type-{}".format(i) for i in range(len(self.tabs))]
            + ["dataframe-{}".format(i) for i in range(len(self.tabs))]
        )

        @self.app.callback(
            Output("graph", "figure"), inputs, prevent_initial_call=False
        )
        def _on_change_update_graph(*args) -> Any:
            triggered_component_id = callback_context.triggered_id

            if triggered_component_id is not None:
                kwargs = dict(zip(input_names, args))
                value = kwargs[triggered_component_id]

                kw, tab_id = triggered_component_id.rsplit("-", 1)
                self.tabs[int(tab_id)].update_option(kw, value)

            return self._figure()

        @self.app.callback(
            Output("hidden-div", "children"), Input("print-code", "n_clicks")
        )
        def _on_print_code(n_clicks: int):
            if n_clicks > 0:
                s = """
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

fig = make_subplots()
"""

                for tab in self.tabs:
                    if tab.has_figure():
                        varname = "trace_{}".format(tab.tab_id)
                        s += """
{}
fig.add_traces(list({}.select_traces()))
fig.update_layout({}.layout)
""".format(tab.figure_str(varname)[:-1], varname, varname)

                for tab in self.tabs:
                    if tab.layout_kwargs():
                        s += "\nfig.update_layout(**{})".format(tab.layout_kwargs())

                s += "\nfig.update_layout(showlegend=True)"
                s += "\nfig.show()"
                print(s)

            return html.Div()

    def _figure(self) -> go.Figure:
        fig = make_subplots()

        for tab in self.tabs:
            f = tab.figure()
            fig.add_traces(list(f.select_traces()))
            # noinspection PyTypeChecker
            fig.update_layout(f.layout)

        for tab in self.tabs:
            fig.update_layout(tab.layout_kwargs())

        return fig

    def run(self):
        return self.app.run_server(
            port=random.randint(2000, 4000),
            mode="inline",
        )


def plot(num_traces=MAX_NUM_TRACES):
    Kindergarten(num_traces).run()


__all__ = ["plot"]
