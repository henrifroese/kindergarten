import inspect

from plotly import express as px

MAX_NUM_TRACES = 3

NONE_OPTION = {"label": "", "value": None}

QUALITATIVE_COLOR_SCALES = {
    name: body
    for name, body in inspect.getmembers(px.colors.qualitative)
    if isinstance(body, list)
    and not name.startswith("__")
    and not name.endswith("_r")
    and body[0].startswith("#")
}

NAMED_COLORS = [
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgrey",
    "darkgreen",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "grey",
    "green",
    "greenyellow",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgrey",
    "lightgreen",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "red",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
]

MARKER_SYMBOLS = [
    "arrow-bar-up",
    "circle",
    "hexagram",
    "star-diamond",
    "y-up",
    "diamond-wide",
    "octagon",
    "arrow-bar-down",
    "triangle-se",
    "cross",
    "triangle-left",
    "x-thin",
    "y-right",
    "star-triangle-down",
    "asterisk",
    "triangle-nw",
    "x",
    "diamond-cross",
    "arrow-down",
    "arrow-bar-right",
    "triangle-down",
    "arrow-bar-left",
    "circle-cross",
    "square-cross",
    "triangle-right",
    "diamond-x",
    "line-ns",
    "y-left",
    "line-nw",
    "hourglass",
    "arrow-right",
    "arrow-left",
    "diamond-tall",
    "triangle-up",
    "star",
    "y-down",
    "star-triangle-up",
    "hexagon2",
    "square-x",
    "hexagon",
    "pentagon",
    "hash",
    "triangle-ne",
    "line-ew",
    "line-ne",
    "diamond",
    "star-square",
    "cross-thin",
    "circle-x",
    "bowtie",
    "triangle-sw",
    "arrow-up",
    "square",
]

SUPPORTED_GRAPH_TYPES = (
    "bar",
    "line",
    "area",
    "violin",
    "timeline",
    "pie",
    "density_heatmap",
    "scatter_matrix",
    "strip",
    "histogram",
    "density_contour",
    "box",
    "scatter",
    "scatter_ternary",
    "parallel_coordinates",
    "scatter_3d",
    "line_3d",
)

DEFAULT_GRAPH_TYPE = ""

UNSUPPORTED_PARAMS = {
    "animation_group",
    "category_orders",
    "facet_row_spacing",
    "data_frame",
    "facet_col_wrap",
    "labels",
    "range_y",
    "custom_data",
    "color_discrete_map",
    "facet_col_spacing",
    "orientation",
    "template",
    "hover_name",
    "range_x",
    "animation_frame",
    "trendline_scope",
    "symbol_map",
    "line_dash_map",
    "symbol_sequence",
    "trendline_color_override",
    "line_dash_sequence",
    "trendline",
    "color_continuous_midpoint",
    "range_color",
    "render_mode",
    "pattern_shape_sequence",
    "pattern_shape_map",
    "hole",
    "size_max",
    "trendline_options",
    "range_z",
}
