import collections
import inspect
import warnings
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Type

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.development.base_component import Component

from kindergarten.constants import (
    NONE_OPTION,
    QUALITATIVE_COLOR_SCALES,
    SUPPORTED_GRAPH_TYPES,
    UNSUPPORTED_PARAMS,
    NAMED_COLORS,
    MARKER_SYMBOLS,
)


def to_options(values) -> Any:
    return [
        {
            "label": value.replace("_", " ") if isinstance(value, str) else value,
            "value": value,
        }
        for value in sorted(values, key=lambda val: str(val))
    ]


def column_options(df, include_none=True, include_name_if_present=True):
    if include_name_if_present and (df.columns.name is not None):
        cols = to_options(list(df.columns) + [df.columns.name])
    else:
        cols = to_options(list(df.columns))

    if include_none:
        return [NONE_OPTION] + cols
    else:
        return cols


def nth_numeric_column_name(df, n):
    numeric_cols = [
        df.columns[i]
        for i in range(len(df.columns))
        if pd.api.types.is_numeric_dtype(df.dtypes[i])
    ]
    try:
        return numeric_cols[n]
    except IndexError:
        return None


class GraphOption(ABC):
    basic = False
    is_px_keyword = True
    valid_graph_types = ()
    keyword = ""
    label = ""

    def __init__(self, df: pd.DataFrame, option_id: int):
        self.df: pd.DataFrame = df
        self.id = "{}-{}".format(self.keyword, option_id)
        self.component: Component = self._build_component()
        self.hidden_component: Component = self._build_hidden_component()

    def _build_hidden_component(self) -> Component:
        return self._build_component(style={"display": "none"})

    def _build_component(self, **kwargs) -> Component:
        return html.Div(
            [html.Label([self.label, self._build_inner_component()])], **kwargs
        )

    def kwarg(self, value) -> Dict[str, Any]:
        return {self.keyword: value}

    def default_kwarg(self) -> Dict[str, Any]:
        return {self.keyword: self.default_kwarg_value()}

    def is_valid_for_graph_type(self, graph_type: str) -> bool:
        return graph_type in self.valid_graph_types

    @abstractmethod
    def _build_inner_component(self) -> Component:
        pass

    @abstractmethod
    def default_kwarg_value(self):
        pass


def build_graph_option(
    _basic: bool,
    _keyword: str,
    _label: str,
    _build_inner_component_callable,
    _default_kwarg_value_callable,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    class C(GraphOption):
        basic = _basic
        keyword = _keyword
        label = _label
        is_px_keyword = _is_px_keyword
        valid_graph_types = _valid_graph_types

        def _build_inner_component(self) -> Component:
            return _build_inner_component_callable(self)

        def default_kwarg_value(self):
            return _default_kwarg_value_callable(self)

    return C


def build_select_graph_option(
    _keyword: str,
    _label: str,
    _basic: bool = False,
    _default_kwarg_value_callable: Any = lambda self: None,
    _select_options_callable: Any = lambda self: column_options(self.df),
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dbc.Select(
            id=self.id,
            required=_required,
            value=self.default_kwarg_value(),
            options=_select_options_callable(self),
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


def build_multiselect_graph_option(
    _keyword: str,
    _label: str,
    _basic: bool = False,
    _default_kwarg_value_callable=lambda self: None,
    _select_options_callable: Any = lambda self: column_options(
        self.df, include_none=False
    ),
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dcc.Dropdown(
            id=self.id,
            clearable=_required,
            value=self.default_kwarg_value(),
            options=_select_options_callable(self),
            multi=True,
            style={"min-width": 150},
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


def build_checklist_graph_option(
    _keyword: str,
    _label: str,
    _basic: bool = False,
    _default_kwarg_value_callable=lambda self: [],
    _checklist_options_callable=lambda self: column_options(
        self.df, include_none=False
    ),
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dbc.Checklist(
            id=self.id,
            value=self.default_kwarg_value(),
            options=_checklist_options_callable(self),
            switch=True,
            inline=True,
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


def build_switch_graph_option(
    _keyword: str,
    _label: str,
    _basic: bool = False,
    _default_kwarg_value_callable=lambda self: False,
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dbc.Switch(
            id=self.id,
            value=self.default_kwarg_value(),
            style={"margin-left": 17},
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


def build_numeric_graph_option(
    _keyword: str,
    _label: str,
    _min: float,
    _max: float,
    _step: float,
    _basic: bool = False,
    _default_kwarg_value_callable=lambda self: None,
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dbc.Input(
            type="number",
            min=_min,
            max=_max,
            step=_step,
            id=self.id,
            value=self.default_kwarg_value(),
            debounce=True,
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


def build_text_graph_option(
    _keyword: str,
    _label: str,
    _basic: bool = False,
    _default_kwarg_value_callable: Any = lambda self: "",
    _required: bool = False,
    _is_px_keyword: bool = True,
    _valid_graph_types: Tuple[str, ...] = (),
):
    def _build_inner_component_callable(self: GraphOption) -> Component:
        return dbc.Input(
            type="text", id=self.id, value=self.default_kwarg_value(), debounce=True
        )

    return build_graph_option(
        _basic=_basic,
        _keyword=_keyword,
        _label=_label,
        _build_inner_component_callable=_build_inner_component_callable,
        _default_kwarg_value_callable=_default_kwarg_value_callable,
        _is_px_keyword=_is_px_keyword,
        _valid_graph_types=_valid_graph_types,
    )


XAxis = build_select_graph_option(
    _keyword="x",
    _label="X-Axis",
    _basic=True,
)

Dimensions = build_multiselect_graph_option(
    _keyword="dimensions",
    _label="Dimensions",
    _basic=True,
)

XStart = build_select_graph_option(
    _keyword="x_start",
    _label="X-Axis Start Values",
    _basic=True,
)

XEnd = build_select_graph_option(
    _keyword="x_end",
    _label="X-Axis End Values",
    _basic=True,
)

YAxis = build_multiselect_graph_option(
    _keyword="y",
    _label="Y-Axis",
    _basic=True,
)

ZAxis = build_select_graph_option(
    _keyword="z",
    _label="Z-Axis",
    _basic=True,
)

Title = build_text_graph_option(
    _keyword="title",
    _label="Title",
)

A = build_select_graph_option(
    _keyword="a",
    _label="A",
    _basic=True,
)

B = build_select_graph_option(
    _keyword="b",
    _label="B",
    _basic=True,
)

C = build_select_graph_option(
    _keyword="c",
    _label="C",
    _basic=True,
)

Names = build_select_graph_option(_keyword="names", _label="Names", _basic=True)

Values = build_select_graph_option(_keyword="values", _label="Values", _basic=True)

LineGroup = build_select_graph_option(_keyword="line_group", _label="Group By")

LineDash = build_select_graph_option(_keyword="line_dash", _label="Dash Type")

Color = build_select_graph_option(_keyword="color", _label="Color")

LineColor = build_select_graph_option(
    _keyword="line_color",
    _label="Line Color",
    _select_options_callable=lambda self: [NONE_OPTION] + to_options(NAMED_COLORS),
    _is_px_keyword=False,
    _valid_graph_types=("line",),
)

PatternShape = build_select_graph_option(
    _keyword="pattern_shape", _label="Pattern Shape"
)

# noinspection PyTypeChecker
BarMode = build_select_graph_option(
    _keyword="barmode",
    _label="Bar Mode",
    _default_kwarg_value_callable=lambda self: "relative",
    _select_options_callable=lambda self: to_options(("relative", "group", "overlay")),
)

# noinspection PyTypeChecker
BoxMode = build_select_graph_option(
    _keyword="boxmode",
    _label="Box Mode",
    _default_kwarg_value_callable=lambda self: "group",
    _select_options_callable=lambda self: to_options(("group", "overlay")),
)

# noinspection PyTypeChecker
ViolinMode = build_select_graph_option(
    _keyword="violinmode",
    _label="Violin Mode",
    _default_kwarg_value_callable=lambda self: "group",
    _select_options_callable=lambda self: to_options(("group", "overlay")),
)

# noinspection PyTypeChecker
StripMode = build_select_graph_option(
    _keyword="stripmode",
    _label="Strip Mode",
    _default_kwarg_value_callable=lambda self: "group",
    _select_options_callable=lambda self: to_options(("group", "overlay")),
)

# noinspection PyTypeChecker
Points = build_select_graph_option(
    _keyword="points",
    _label="Points to Show",
    _default_kwarg_value_callable=lambda self: "outliers",
    _select_options_callable=lambda self: to_options(
        ("outliers", "suspectedoutliers", "all", False)
    ),
)

ColorContinuousScale = build_select_graph_option(
    _keyword="color_continuous_scale",
    _label="Color Scale",
    _select_options_callable=lambda self: to_options(px.colors.named_colorscales()),
)

# noinspection PyTypeChecker
ColorDiscreteSequence = build_select_graph_option(
    _keyword="color_discrete_sequence",
    _label="Color Sequence",
    _default_kwarg_value_callable=lambda self: QUALITATIVE_COLOR_SCALES["Plotly"],
    _select_options_callable=lambda self: [
        {"label": name, "value": body}
        for name, body in QUALITATIVE_COLOR_SCALES.items()
    ],
)

Size = build_select_graph_option(_keyword="size", _label="Size")

Symbol = build_select_graph_option(_keyword="symbol", _label="Symbol")

XError = build_select_graph_option(_keyword="error_x", _label="X-Axis Error Bars")

YError = build_select_graph_option(_keyword="error_y", _label="Y-Axis Error Bars")

ZError = build_select_graph_option(_keyword="error_z", _label="Z-Axis Error Bars")

XErrorMinus = build_select_graph_option(
    _keyword="error_x_minus", _label="X-Axis Error Bars in Negative Direction"
)

YErrorMinus = build_select_graph_option(
    _keyword="error_y_minus", _label="Y-Axis Error Bars in Negative Direction"
)

ZErrorMinus = build_select_graph_option(
    _keyword="error_z_minus", _label="Z-Axis Error Bars in Negative Direction"
)

HoverData = build_checklist_graph_option(_keyword="hover_data", _label="Show on Hover")

Marginal = build_select_graph_option(
    _keyword="marginal",
    _label="Marginal Distribution",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("histogram", "rug", "box", "violin")),
)

MarginalX = build_select_graph_option(
    _keyword="marginal_x",
    _label="X-Axis Marginal Distribution",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("histogram", "rug", "box", "violin")),
)

MarginalY = build_select_graph_option(
    _keyword="marginal_y",
    _label="Y-Axis Marginal Distribution",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("histogram", "rug", "box", "violin")),
)

FacetCol = build_select_graph_option(_keyword="facet_col", _label="Facet Column")

FacetRow = build_select_graph_option(_keyword="facet_row", _label="Facet Row")

LogX = build_switch_graph_option(_keyword="log_x", _label="Logarithmic X-Axis")

LogY = build_switch_graph_option(_keyword="log_y", _label="Logarithmic Y-Axis")

LogZ = build_switch_graph_option(_keyword="log_z", _label="Logarithmic Z-Axis")

Markers = build_switch_graph_option(_keyword="markers", _label="Markers")

MarkerColor = build_select_graph_option(
    _keyword="marker_color",
    _label="Marker Color",
    _select_options_callable=lambda self: [NONE_OPTION] + to_options(NAMED_COLORS),
    _is_px_keyword=False,
    _valid_graph_types=("scatter",),
)

MarkerSymbol = build_select_graph_option(
    _keyword="marker_symbol",
    _label="Marker Symbol",
    _select_options_callable=lambda self: [NONE_OPTION] + to_options(MARKER_SYMBOLS),
    _is_px_keyword=False,
    _valid_graph_types=("scatter", "line"),
)

LegendName = build_text_graph_option(
    _keyword="name",
    _label="Legend Name",
    _is_px_keyword=False,
    _valid_graph_types=("scatter", "line"),
    _default_kwarg_value_callable=lambda self: None,
)

Notched = build_switch_graph_option(_keyword="notched", _label="Notched Boxes")

Cumulative = build_switch_graph_option(_keyword="cumulative", _label="Cumulative")

TextAuto = build_switch_graph_option(_keyword="text_auto", _label="Show Text")

Box = build_switch_graph_option(_keyword="box", _label="Show Box")

NBins = build_numeric_graph_option(
    _keyword="nbins", _label="Bins", _min=0, _max=1000, _step=1
)

NBinsX = build_numeric_graph_option(
    _keyword="nbinsx", _label="X Bins", _min=0, _max=1000, _step=1
)

NBinsY = build_numeric_graph_option(
    _keyword="nbinsy", _label="Y Bins", _min=0, _max=1000, _step=1
)

MarkerSize = build_numeric_graph_option(
    _keyword="marker_size",
    _label="Marker Size",
    _min=0,
    _max=100,
    _step=1,
    _is_px_keyword=False,
    _valid_graph_types=("scatter", "line"),
)

LineShape = build_select_graph_option(
    _keyword="line_shape",
    _label="Line Shape",
    _select_options_callable=lambda self: to_options(("linear", "spline")),
)

GroupNorm = build_select_graph_option(
    _keyword="groupnorm",
    _label="Normalization",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("fraction", "percent")),
)

BarNorm = build_select_graph_option(
    _keyword="barnorm",
    _label="Bar Normalization",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("fraction", "percent")),
)

HistNorm = build_select_graph_option(
    _keyword="histnorm",
    _label="Histogram Normalization",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("percent", "probability", "density", "probability density")),
)

# noinspection PyTypeChecker
HistFunc = build_select_graph_option(
    _keyword="histfunc",
    _label="Aggregation Function",
    _default_kwarg_value_callable=lambda self: "count",
    _select_options_callable=lambda self: [NONE_OPTION]
    + to_options(("count", "sum", "avg", "min", "max")),
)

Text = build_select_graph_option(_keyword="text", _label="Text")

Base = build_select_graph_option(_keyword="base", _label="Base Position")

Width = build_numeric_graph_option(
    _keyword="width", _label="Width", _min=0, _max=10_000, _step=50
)

Height = build_numeric_graph_option(
    _keyword="height", _label="Height", _min=0, _max=10_000, _step=50
)

XAxisTitle = build_text_graph_option(
    _keyword="xaxis_title",
    _label="X-Axis Title",
    _valid_graph_types=SUPPORTED_GRAPH_TYPES,
    _is_px_keyword=False,
)

YAxisTitle = build_text_graph_option(
    _keyword="yaxis_title",
    _label="Y-Axis Title",
    _valid_graph_types=SUPPORTED_GRAPH_TYPES,
    _is_px_keyword=False,
)

ZAxisTitle = build_text_graph_option(
    _keyword="zaxis_title",
    _label="Z-Axis Title",
    _valid_graph_types=("scatter_3d", "line_3d"),
    _is_px_keyword=False,
)

LegendTitle = build_text_graph_option(
    _keyword="legend_title",
    _label="Legend Title",
    _valid_graph_types=SUPPORTED_GRAPH_TYPES,
    _is_px_keyword=False,
)

TitleFontSize = build_numeric_graph_option(
    _keyword="title_font_size",
    _label="Title Font Size",
    _valid_graph_types=SUPPORTED_GRAPH_TYPES,
    _is_px_keyword=False,
    _min=0,
    _max=100,
    _step=1,
)

GRAPH_OPTIONS: Tuple[Type["GraphOption"], ...] = tuple(GraphOption.__subclasses__())

param_to_graph_types = collections.defaultdict(set)

for graph_type in SUPPORTED_GRAPH_TYPES:
    signature = inspect.signature(getattr(px, graph_type))
    for param in signature.parameters.keys():
        if param not in UNSUPPORTED_PARAMS:
            param_to_graph_types[param].add(graph_type)

params_without_implementation = set(param_to_graph_types.keys()) - set(
    graph_option.keyword for graph_option in GRAPH_OPTIONS
)
if params_without_implementation:
    warnings.warn(
        "The following parameters "
        "are not ignored but do not "
        "have an implementation: "
        "{}".format(params_without_implementation)
    )

for graph_option in GRAPH_OPTIONS:
    graph_option.valid_graph_types += tuple(param_to_graph_types[graph_option.keyword])

PX_KEYWORDS = {option.keyword for option in GRAPH_OPTIONS if option.is_px_keyword}
LAYOUT_KEYWORDS = {"xaxis_title", "yaxis_title", "legend_title", "title_font_size"}
TRACES_KEYWORDS = (
    {option.keyword for option in GRAPH_OPTIONS} - PX_KEYWORDS - LAYOUT_KEYWORDS
)
