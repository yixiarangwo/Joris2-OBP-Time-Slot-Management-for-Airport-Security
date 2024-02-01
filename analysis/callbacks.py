from dash import callback, Input, Output, State, no_update, Patch
import numpy as np
import json

from importables.functions import latexToNumpy

from analysis.analysis import *
from analysis.functions import *
from analysis.simulation import *
from analysis.graphs import *



# Open selection panel with button
@callback(
    Output({"section": "analysis", "type": "panel", "index": "sim-selection"}, "is_open",
           allow_duplicate = True),
    Input({ "section": "analysis", "type": "button", "index": "open-panel"},   "n_clicks"),
    prevent_initial_call = True
)
def openPanel(n_clicks):
    return True



# When analysis tab is selected and not all data is uploaded, show error alert and disable run simulation and dropdown for graphs
@callback(
    Output({"section": "analysis", "type": "text", "index": "missing-data"},     "children"),
    Output({"section": "analysis", "type": "alert", "index": "missing-data"},    "is_open"),
    Output({"section": "analysis", "type": "button", "index": "run-simulation"}, "disabled"),
    Output({"section": "analysis", "type": "alert", "index": "missing-data"},    "color"),
    Output({"section": "analysis", "type": "panel", "index": "sim-selection"},   "is_open"),
    
    Input({ "section": "app",          "type": "tabs"},                               "active_tab"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},     "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},      "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "lanes"},        "data"),
    State({ "section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),
    State({ "section": "intermediate", "type": "parameters", "index": "time-slots"},  "data"),
    State({ "section": "inputs", "type": "button", "index": "submit-time-slots"},     "n_clicks"),
    State({ "section": "analysis", "type": "button", "index": "run-simulation"},      "n_clicks"),
    prevent_initial_call = True
)
def showSimWarning(activeTab, arrivalData, flightData, laneData, distInfo, timeSlotsInfo, clicksSlots, clicksSim):
    # Check if inputs tab is current tab and whether there are no arrivals uploaded
    if activeTab != "tab-analysis":
        return no_update, no_update, no_update, no_update, False

    # Open selection panel if no simulation has run yet
    openPanel = False
    if clicksSim == 0 or clicksSim is None:
        openPanel = True
    
    if arrivalData == {}:
        return "Arrival data has not been uploaded yet", True,  True, "danger", openPanel
    elif flightData == {}:
        return "Flight schedule has not been uploaded yet", True, True, "danger", openPanel
    elif laneData == {}:
        return "Lane schedule has not been uploaded yet", True, True, "danger", openPanel
    elif latexToNumpy(distInfo["latex"]) is None:
        return "Service time distribution is not valid", True, True, "danger", openPanel
    elif clicksSlots == 0 or clicksSlots is None:
        return "Time slots have not been submitted yet", True,  True, "danger", openPanel
    elif all(all(not isinstance(cap, int) for cap in timeSlotsInfo[flight]["capacity"]) 
             for flight in timeSlotsInfo.keys() if flight != "slot-duration"):
        return "No time slot have been set", True, False, "warning", openPanel

    # No error or warning
    return "", False, False, no_update, openPanel



# Run the simulation
import pandas as pd
@callback(
    Output({"section": "analysis", "type": "text", "index": "sim-avg-total-waiting-min"}, "children"),
    Output({"section": "analysis", "type": "text", "index": "sim-avg-total-waiting-sec"}, "children"),
    Output({"section": "analysis", "type": "text", "index": "sim-avg-vq-waiting-min"},    "children"),
    Output({"section": "analysis", "type": "text", "index": "sim-avg-vq-waiting-sec"},    "children"),
    Output({"section": "analysis", "type": "text", "index": "sim-avg-gq-waiting-min"},    "children"),
    Output({"section": "analysis", "type": "text", "index": "sim-avg-gq-waiting-sec"},    "children"),
    Output({"section": "analysis", "type": "div", "index": "sim-stats"},              "className"),
    Output({"section": "analysis", "type": "graph", "index": 0},                      "figure"),
    Output({"section": "analysis", "type": "graph", "index": 0},                      "style"),
    Output({"section": "analysis", "type": "graph", "index": 1},                      "figure"),
    Output({"section": "analysis", "type": "graph", "index": 1},                      "style"),
    Output({"section": "analysis", "type": "graph", "index": 2},                      "figure"),
    Output({"section": "analysis", "type": "graph", "index": 2},                      "style"),
    Output({"section": "analysis", "type": "graph", "index": 3},                      "figure"),
    Output({"section": "analysis", "type": "graph", "index": 3},                      "style"),
    
    Input({"section": "analysis", "type": "button", "index": "run-simulation"},      "n_clicks"),
    State({"section": "analysis", "type": "input", "index": "simulation-runs"},      "value"),
    State({"section": "intermediate", "type": "dataframe", "index": "arrivals"},     "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "flights"},      "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "lanes"},        "data"),
    State({"section": "intermediate", "type": "parameters", "index": "time-slots"},  "data"),
    State({"section": "intermediate", "type": "parameters", "index": "lane-cap"},    "data"),
    State({"section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),
    prevent_initial_call = True
)
def runSimulation(n_clicks, amountRuns, arrivalData, flightData, laneData, timeSlotsInfo, laneCap, distInfo):
    # Convert format
    slotDuration = timeSlotsInfo["slot-duration"]
    timeSlots = {flight: timeSlotsInfo[flight] for flight in timeSlotsInfo if flight != "slot-duration"}
    
    # Run simulation with given maximal time and amount of runs
    totalAvgs, allWaitingTimes, missedFlight, waitingPerInverval, avgTotal, avgVQ, avgGQ = multiple_run_simulation(amountRuns, 40000, arrivalData, flightData, laneData, timeSlots, slotDuration, laneCap, distInfo)

    figure1 = avgWaitingOverTime(
        totalAvgs["Time in hour"],
        totalAvgs["Average Waiting Time"],
        totalAvgs["Average Virtual Queue Waiting Time"],
        totalAvgs["Average Normal Queue Waiting Time"]
    )
    figure2 = cumulativeWaitingTimes([time / 60 for interval in allWaitingTimes for time in interval])
    figure3 = missedFlightsHist(arrivalData["ArrivalTime"], missedFlight["new_ArrivalTime"])

    # waitingPerInverval are all the waiting times per intervals, so slider for this one
    
    figure4 = go.Figure()
    for i, intervalWaiting in enumerate(waitingPerInverval):        # 15 min
        figure4.add_trace(
            go.Histogram(
                x = intervalWaiting,
                visible = False,
                marker = {
                    "color": "hsv(240,100%,40%)",
                    "line": {
                        "width": 1,
                        "color": "#FFFFFF"
                    },
                },
                hovertemplate = "Waiting time: %{x}<br>Count: %{y}<extra></extra>"
            )
        )
    
    # Make 10th trace visible
    figure4.data[10].visible = True
    
    # Create and add slider
    steps = []
    times = [f"{i//4:02d}:{i*15%60:d}-{(i+1)//4:d}:{(i+1)*15%60:02d}" for i in range(len(figure4.data))]
    for i in range(len(figure4.data)):
        step = {
            "method": "update",
            "args": [
                {"visible": [False] * len(figure4.data)},
                {"title": "Waiting times of time interval: " + times[i]}
            ],
            "label": ""
        }
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)
    
    sliders = [{
        "active": 10,
        "currentvalue": {
            "prefix": "Time: ",
            "font": {
                "color": "rgba(0,0,0,0)"
            },
        },
        "pad": {"t": 15, "l": 0, "b": 0, "r": 0},
        "steps": steps
    }]
    
    figure4.update_layout(
        sliders = sliders,
        margin = {
            "l": 0, 
            "r": 0, 
            "t": 26,
            "b": 5,
            "pad": 0
        },
        xaxis = {
            "title": "Waiting time (min)", 
            "showgrid": False,
            "tickformat": "%H:%M"
        },
        yaxis = {
            "title": "Amount of passengers", 
            "rangemode": "tozero",
            "showgrid": False,
        },
    )

    # Show graphs
    patchedGraph1 = Patch()
    patchedGraph2 = Patch()
    patchedGraph3 = Patch()
    patchedGraph4 = Patch()
    patchedGraph1["display"] = "block"
    patchedGraph2["display"] = "block"
    patchedGraph3["display"] = "block"
    patchedGraph4["display"] = "block"

    # Show dropdown and global waiting time statistics using patch
    patchedDropdown = Patch()
    patchedStats = Patch()
    patchedDropdown["display"] = "block"
    patchedStats["display"] = "block"

    return avgTotal[0], avgTotal[1], avgVQ[0], avgVQ[1], avgGQ[0], avgVQ[1], "d-flex justify-content-evenly", figure1, patchedGraph1, figure2, patchedGraph2, figure3, patchedGraph3, figure4, patchedGraph4
