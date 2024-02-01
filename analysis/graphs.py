import plotly.graph_objs as go
import numpy as np
import plotly.express as px

from inputs.functions import unixToDateTime


# Create a line plot with markers using plotly express
def avgWaitingOverTime(times, totalWaiting, vqWaiting, gqWaiting):
    return go.Figure().add_trace(
        go.Scatter(
            x = times,
            y = totalWaiting,
            name = "Total",
            mode = "lines",
            marker_color = "blue",
        )
    ).add_trace(
        go.Scatter(
            x = times,
            y = vqWaiting,
            name = "Virtual queue",
            mode = "lines",
            marker_color = "red"
        )
    ).add_trace(
        go.Scatter(
            x = times,
            y = gqWaiting,
            name = "General queue",
            mode = "lines",
            marker_color = "green"
        )
    ).update_layout(
        title = "Average waiting time of passengers",
        xaxis = {
            "title": "Time of day (per 15 min.)",
            "showgrid": False,
        },
        yaxis = {
            "title": "Average waiting time (min.)",
            "showgrid": False,
        },
        margin = {
            "l": 0, 
            "r": 0, 
            "t": 26,
            "b": 0,
            "pad": 0
        },
        showlegend=True,
        legend = {
            "yanchor": "top",
            "xanchor":"left",
            "x": 0.01,
            "y": 0.99
        },
        hovermode = "x unified"
    )


def cumulativeWaitingTimes(waitingTimes):
    return go.Figure().add_trace(
        go.Histogram(
            x = waitingTimes,
            marker_color = "hsv(240,100%,40%)",
            marker = {
                "line": {
                    "width": 1,
                    "color": "#FFFFFF"
                },
            },
            cumulative_enabled = True,
            histnorm = "probability",
            hovertemplate = "Waiting time (min.): %{x}<br>Ration of occurence: %{y}<extra></extra>",
        )
    ).update_layout(
        title = "Cumulative distribution of waiting times",
        margin = {
            "l": 0,
            "r": 0,
            "t": 26,
            "b": 0,
            "pad": 0
        },
        xaxis = {
            "title": "Waiting time (min.)",
            "showgrid": False,
        },
        yaxis = {
            "title": "Density",
            "rangemode": "tozero",
            "showgrid": False,
        },
    )

def missedFlightsHist(arrivalData, arrivalsMissed):
    return go.Figure().add_trace(
        go.Histogram(
            x = [unixToDateTime(time) for time in arrivalData],
            bingroup = "1",
            marker_color = "hsv(240,100%,40%)",
            xbins = {
                "size": 15 * 60 * 1000      # 15 minutes, and plotly only takes milliseconds
            },
            marker = {
                "line": {
                    "width": 1,
                    "color": "#FFFFFF"
                },  
            },
            hovertemplate = "Arrivals<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
            opacity = 0.5
        )
    ).add_traces(
        go.Histogram(
            x = [unixToDateTime(time) for time in arrivalsMissed],
            bingroup = "1",
            marker_color = "#FFFF00",
            marker = {
                "line": {
                    "width": 1,
                    "color": "#FFFFFF"
                },
            },
            yaxis = "y2",
            hovertemplate = "Arrivals of missed flights<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
            opacity = 0.5
        )
    ).update_layout(
        title = "Arrivals from missed flights",
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
            "tickformat": "%H:%M"
        },
        yaxis = {
            "title": "Amount of passengers", 
            "rangemode": "tozero",
            "showgrid": False,
        },
        yaxis2 = {
            "title": "Amount of missed flights",
            "rangemode": "tozero",
            "showgrid": False,
            "overlaying": "y",
            "side": "right",
        },
        showlegend = False,
        barmode = "overlay"
    )

arrivalHistograms = go.Figure().add_trace(
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
        hovertemplate = "Arrivals without virtual queue<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>",
        name = "Arrivals with time slots"
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
        hovertemplate = "Arrivals with virtual queue<br>Time interavl:%{x}<br>Amount of arrivals: %{y}<extra></extra>",
        name = "Arrivals with time slots"
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
)
