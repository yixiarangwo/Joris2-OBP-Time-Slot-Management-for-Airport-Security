from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Make figure for subplots
serviceTestFig = make_subplots(specs = [[{"secondary_y": True}]])
serviceTestFig.add_trace(
    go.Histogram(
        x = [],
        name = "Sampled service times"
    ),
    secondary_y = False
)
serviceTestFig.add_trace(
    go.Scatter(
        x = [],
        y = [],
        name = "Inputted function",
        mode = "lines"
    ),
    secondary_y = True
)
serviceTestFig.update_layout(
    yaxis = {"showticklabels": False},
    yaxis2 = {"showticklabels": False, "rangemode": "tozero"},
    margin = {"l": 0, "r": 0, "t": 0, "b": 0},
    legend = {"yanchor": "top", "xanchor": "right"}
)
