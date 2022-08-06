from typing import Dict, Any, List, Tuple

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import html
from dash.development.base_component import Component

from kindergarten.constants import NONE_OPTION, SUPPORTED_GRAPH_TYPES, DEFAULT_GRAPH_TYPE
from kindergarten.graph_options import (
    GRAPH_OPTIONS,
    GraphOption,
    PX_KEYWORDS,
    LAYOUT_KEYWORDS,
    TRACES_KEYWORDS,
    to_options,
)


class Tab:
    def __init__(self, tab_id: int):
        self.tab_id = tab_id
        self.graph_kwargs: Dict[str, Any] = {}
        self.graph_type = DEFAULT_GRAPH_TYPE
        self.df_name = None
        self.options: Dict[str, GraphOption] = {
            option.keyword: option(pd.DataFrame(), self.tab_id)
            for option in GRAPH_OPTIONS
        }
        self.graph_type_component = self._build_graph_type_component()
        self.dataframe_component = self._build_dataframe_component()

        self._init_graph_kwargs()

    def update_option(self, kw: str, value: Any):
        if kw == "graph-type":
            self.update_graph_type(value)
        elif kw == "dataframe":
            self.update_dataframe(value)
        else:
            # dbc or dash turn option "value"
            # fields into strings; we recover the list here.
            if kw == "color_discrete_sequence":
                value = value.split(",")

            if kw == "y" and len(value) == 1:
                value = value[0]

            # dbc or dash turn option "value" fields
            # into strings, so {"label": None, "value": None}
            # leads to value being an empty string
            # ('') instead of None.
            if value == "" or (kw == "y" and value == []):
                value = None

            self.graph_kwargs.update(self.options[kw].kwarg(value))

    def update_graph_type(self, graph_type: str):
        self.graph_type = graph_type
        self._reset_graph_kwargs()

    def update_dataframe(self, df_name: str):
        import __main__

        self.df_name = df_name
        self.options: Dict[str, GraphOption] = {
            option.keyword: option(getattr(__main__, self.df_name), self.tab_id)
            for option in GRAPH_OPTIONS
        }

    def figure(self) -> go.Figure:
        if not self.has_figure():
            return go.Figure()

        px_kwargs, update_traces_kwargs, _ = self._figure_kwargs()

        import __main__

        fig = getattr(px, self.graph_type)(getattr(__main__, self.df_name), **px_kwargs)
        fig.update_traces(**update_traces_kwargs)

        if self.graph_type in ("scatter", "line"):
            try:
                fig.update_traces(textposition="bottom right")
            except Exception:
                pass

        # If we don't do this, Plotly doesn't show the legend for single traces
        for d in fig["data"]:
            d["showlegend"] = True

        return fig

    def layout_kwargs(self):
        _, _, update_layout_kwargs = self._figure_kwargs()
        return update_layout_kwargs

    def figure_str(self, varname: str) -> str:
        px_kwargs, update_traces_kwargs, _ = self._figure_kwargs(ignore_defaults=True)

        s = "# Trace {}\n".format(self.tab_id)

        if px_kwargs:
            s += "{} = px.{}({}, **{})\n".format(varname, self.graph_type, self.df_name, px_kwargs)
        else:
            s += "{} = px.{}({})\n".format(varname, self.graph_type, self.df_name)
        if update_traces_kwargs:
            s += "{}.update_traces(**{})\n".format(varname, update_traces_kwargs)

        return s

    def has_figure(self) -> bool:
        return bool(self.graph_type)

    def _figure_kwargs(self, ignore_defaults: bool = True) -> Tuple[Dict, Dict, Dict]:
        if ignore_defaults:
            graph_keywords = set(
                key
                for key, val in self.graph_kwargs.items()
                if val != self.options[key].default_kwarg_value()
            )
        else:
            graph_keywords = set(self.graph_kwargs.keys())

        layout_keywords = graph_keywords & LAYOUT_KEYWORDS
        px_keywords = graph_keywords & PX_KEYWORDS
        traces_keywords = graph_keywords & TRACES_KEYWORDS

        px_kwargs = {kw: self.graph_kwargs[kw] for kw in px_keywords}
        update_traces_kwargs = {kw: self.graph_kwargs[kw] for kw in traces_keywords}
        update_layout_kwargs = {kw: self.graph_kwargs[kw] for kw in layout_keywords}

        return px_kwargs, update_traces_kwargs, update_layout_kwargs

    def component(self):
        return html.Div(
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(self.dataframe_component)),
                            dbc.Col(html.Div(self.graph_type_component)),
                        ]
                    ),
                    html.Div(
                        self.options_component(),
                        id=self.add_tab_id("selector"),
                    ),
                ],
                body=True,
            ),
        )

    def add_tab_id(self, component_id: str):
        return "{}-{}".format(component_id, self.tab_id)

    @staticmethod
    def _build_basic_component(basic_option_components: List[Component]):
        rows = []
        for i in range(0, len(basic_option_components), 3):
            cols = []
            for component in basic_option_components[i : i + 3]:
                cols.append(dbc.Col(component))

            rows.append(dbc.Row(cols))

        return html.Div(rows)

    @staticmethod
    def _build_extended_component(extended_option_components: List[Component]):
        rows = []
        for i in range(0, len(extended_option_components), 3):
            cols = []
            for component in extended_option_components[i : i + 3]:
                cols.append(dbc.Col(component))

            rows.append(dbc.Row(cols))

        return html.Div(
            dbc.Accordion(
                [
                    dbc.AccordionItem(html.Div(rows), title="More Options"),
                ],
                start_collapsed=True,
            ),
            style={"padding-top": 10},
        )

    def options_component(self):
        (
            basic_option_components,
            extended_option_components,
            hidden_option_components,
        ) = ([], [], [])

        for option in self.options.values():
            if self.graph_type not in option.valid_graph_types:
                hidden_option_components.append(option.hidden_component)
            elif option.basic:
                basic_option_components.append(option.component)
            else:
                extended_option_components.append(option.component)

        basic_component = self._build_basic_component(basic_option_components)
        extended_component = self._build_extended_component(extended_option_components)

        return [
            basic_component,
            extended_component,
        ] + hidden_option_components

    def _build_graph_type_component(self) -> html.Label:
        return html.Label(
            [
                "Graph Type",
                dbc.Select(
                    id=self.add_tab_id("graph-type"),
                    required=True,
                    value=DEFAULT_GRAPH_TYPE,
                    options=[NONE_OPTION] + to_options(SUPPORTED_GRAPH_TYPES),
                ),
            ]
        )

    def _build_dataframe_component(self) -> html.Label:
        import __main__

        dataframes = [
            var
            for var in dir(__main__)
            if isinstance(getattr(__main__, var), pd.DataFrame)
        ]

        return html.Label(
            [
                "Dataframe",
                dbc.Select(
                    id=self.add_tab_id("dataframe"),
                    required=True,
                    value=None,
                    options=[NONE_OPTION] + to_options(dataframes),
                ),
            ]
        )

    def _reset_graph_kwargs(self):
        self.graph_kwargs.clear()

        for option in self.options.values():
            if self.graph_type in option.valid_graph_types:
                self.graph_kwargs.update(option.default_kwarg())

    def _init_graph_kwargs(self):
        self._reset_graph_kwargs()
