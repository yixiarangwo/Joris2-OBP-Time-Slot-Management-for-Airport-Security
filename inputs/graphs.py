import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from inputs.functions import unixToDateTime

# Make histogram for arrivals
totalArrivalsHistogram = go.Figure().add_trace(
    go.Histogram(
        x = [None],
        bingroup = "1",
        marker_color = "hsv(240,100%,40%)",
        xbins = {
            "start": "2024-01-30T02:17:00",
            "end": "2024-01-30T02:17:00",
            "size": 15 * 60 * 1000      # 15 minutes, and plotly only takes milliseconds
        },
        marker = {
            "line": {
                "width": 1,
                "color": "#FFFFFF"
            },  
        },
        hovertemplate = "Total arrivals<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
    )
).add_traces(
    go.Scatter(
        x = [None],
        y = [None], 
        mode = "lines",
        line = {
            "dash": "dot",
            "color": "white",
            "shape": "hv"
        },
        hovertemplate = "Time interval: %{x}<br>Maximal security capacity: %{y}<extra></extra>"
    )
).add_traces(
    go.Histogram(
        x = [None],
        bingroup = "1",
        marker_color = "#FFFF00",
        marker = {
            "line": {
                "width": 1,
                "color": "#FFFFFF"
            },
        },
        hovertemplate = ""
    )
).update_layout(
    title = "Arrivals from all flights",
    margin = {
        "l": 0, 
        "r": 0, 
        "t": 26,
        "b": 0,
        "pad": 0
    },
    xaxis = {
        "title": "Time of day", 
        "showgrid": False,
        "tickformat": "%H:%M",
        "range": [0,10]
    },
    yaxis = {
        "title": "Amount of passengers", 
        "rangemode": "tozero",
        "showgrid": False,
    },
    showlegend = False,
    annotations = [{
        "showarrow": False,
        "text": "",
        "font": {"color": "white"},
        "xref": "paper",
        "x": "0",
        "y": "60",
    }],
    barmode = "overlay"
).add_vline(
    x = -1,
    line_color = "red",
    annotation_text = "Departure",
    annotation_position = "top left",
    annotation_font_color = "red"
)



# Make histogram for all arrivals
caseArrivalsHistogram = go.Figure().add_trace(
    go.Histogram(
        x = [None],
        name = "Top pick",
        bingroup = "1",
        marker_color = "green",
        xbins = {
            "start": "2024-01-30T02:17:00",
            "end": "2024-01-30T02:17:00",
            "size": 15 * 60 * 1000      # 15 minutes, and plotly only takes milliseconds
        },
        marker = {
            "line": {
                "width": 1,
                "color": "#FFFFFF"
            },
        },
        opacity = 0.5,
        hovertemplate = "Top pick scenario<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
    )
).add_trace(
    go.Histogram(
        x = [None],
        name = "Bottom pick",
        bingroup = "1",
        marker_color = "red",
        marker = {
            "line": {
                "width": 1,
                "color": "#FFFFFF"
            },
        },
        opacity = 0.5,
        hovertemplate = "Bottom pick scenario<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
    )
).add_trace(
    go.Histogram(
        x = [None],
        name = "Average pick",
        bingroup = "1",
        marker_color = "blue",
        marker = {
            "line": {
                "width": 1,
                "color": "#FFFFFF"
            },
        },
        opacity = 0.5,
        hovertemplate = "Average pick scenario<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
    )
).add_traces(
    go.Scatter(
        x = [None],
        y = [None], 
        mode = "lines",
        line = {
            "dash": "dot",
            "color": "white",
            "shape": "hv"
        },
        showlegend = False,
        hovertemplate = "Time interval: %{x}<br>Maximal security capacity: %{y}<extra></extra>"
    )
).update_layout(
    title = "Change of arrival times by time slots in different cases",
    barmode = "overlay",
    xaxis = {
        "title": "Time of day", 
        "showgrid": False,
        "tickformat": "%H:%M",
        "range": [0,10]
    },
    yaxis = {
        "title": "Amount of passengers", 
        "rangemode": "tozero",
        "showgrid": False,
    },
    annotations = [{
        "showarrow": False,
        "text": "",
        "font": {"color": "white"},
        "xref": "paper",
        "x": "0",
        "y": "60",
    }],
    margin = {
        "l": 0, 
        "r": 0, 
        "t": 26,
        "b": 0,
        "pad": 0
    }
)

# To Do now:
# HANDLE THE RECOMS FOR DROPDOWN
# Make action icon for taking over time slot recommendations usable
# Make option for setting max capacity of arrivals for time interval and show in total arrivals historgram



"""
To add time slot boundaries in for loop, use this with patch (found out how to add to figure with patch):

fig
"""



# use cumulative_enabled=True for analysis tab
