from dash import callback, Output, Input, State, Patch, html, MATCH, ALL, ctx, no_update
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

from math import isclose

from pathlib import Path
import base64
import json
import io

from inputs.time_slot_recommendations import *
from inputs.functions import *


# When flights data is updated, update dropdown options, make children for time slot inputs,
# and deselect selection in dropdown of input tab by setting its value to ""
@callback(
    Output({"section": "inputs",       "type": "dropdown",  "index": "flight-selection"}, "options"),
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"}, "children",
           allow_duplicate = True),
    
    Input({ "section": "intermediate", "type": "dataframe", "index": "flights"},          "data"),
    prevent_initial_call = True
)
def updateInputsFlights(flights):
    # Get new dropdown options
    options = [
        {
            "label": [
                html.Label(
                    children = ["FLT: " + flt], 
                ),
                html.Span(
                    children = [
                        "__ETD: " + unixToTime24(etd) + 
                        "__PAX: " + "_" * (4 - len(str(pax))) + str(pax)    # bit of underscore number padding
                    ],
                )
            ],
            "value": flt,
            "search": unixToTime24(etd)
        }
        for flt, etd, pax in zip(flights["FlightNumber"], flights["DepartureTime"], flights["Passengers"])
    ]

    # For each flight create a row with single time slot input
    divs = [
        dbc.Row(
            children = [timeSlotsDiv(flight["value"], 0)],
            id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight["value"]},
            style = {"display": "none"},
            justify = "center",
            align = "center",
        )
        for flight in options
    ]
    
    return options, divs



# When input tab is selected and no arrival is uploaded, show warning alert
# When arrivals are uploaded, show total arrivals histogram
@callback(
    Output({"section": "inputs",       "type": "alert",     "index": "arrival-check"},   "is_open"),
    Output({"section": "inputs",       "type": "text",      "index": "arrival-check"},   "children"),
    Output({"section": "inputs",       "type": "graph",     "index": "total-arrivals"},  "figure",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "div",       "index": "arrivals-graphs"}, "style"),
    Output({"section": "inputs",       "type": "graph",     "index": "case-arrivals"},   "figure",
           allow_duplicate = True),
    
    Input({ "section": "app",          "type": "tabs"},                                 "active_tab"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},       "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},        "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "lanes"},          "data"),
    State({ "section": "inputs",       "type": "input",     "index": "lane-cap"},       "value"),
    State({"section": "inputs",       "type": "graph",     "index": "total-arrivals"},  "figure"),
    prevent_initial_call = True
)
def showArrivalWarning(activeTab, arrivalData, flightData, laneData, laneCap, figure):
    # Check if inputs tab is current tab and whether there are no arrivals uploaded
    if activeTab != "tab-inputs":
        return no_update, no_update, no_update, no_update, no_update

    # Check if not all data uploaded
    if arrivalData == {}:
        # Hide figures
        patchedDivStyle = Patch()
        patchedDivStyle["display"] = "none"
    
        return True, "Arrival times of passengers not yet uploaded", no_update, patchedDivStyle, no_update


    # Check missing flights through checking if all arrivals have an existing FLT
    uploadedFlightData = True
    showWarning = False
    warningMessage = ""
    if flightData == {}:
        showWarning = True
        uploadedFlightData = False
        warningMessage = "Flight schedule not yet uploaded"
    elif not all([arrivalFlight in flightData.get("FlightNumber", [])
                for arrivalFlight in arrivalData.get("FlightNumber", [])]):
        showWarning = True
        warningMessage = "Flight numbers missing for some arrivals"

    # Get patches for histogram
    patchedFigure = Patch()
    patchedDivStyle = Patch()

    # Get patches for case histograms
    patchedCaseFigure = Patch()

    # Set lane data in figures if uploaded
    if laneData != {}:
        patchedFigure["data"][1]["x"] = [unixToDateTime(time) for time in laneData["Time"]]
        patchedFigure["data"][1]["y"] = [amountLanes * laneCap for amountLanes in laneData["Lanes"]]
        patchedFigure["layout"]["annotations"][0]["text"] = "Security<br>capacity"
        patchedFigure["layout"]["annotations"][0]["y"] = laneCap

        patchedCaseFigure["data"][3]["x"] = [unixToDateTime(time) for time in laneData["Time"]]
        patchedCaseFigure["data"][3]["y"] = [amountLanes * laneCap for amountLanes in laneData["Lanes"]]
        patchedCaseFigure["layout"]["annotations"][0]["text"] = "Security<br>capacity"
        patchedCaseFigure["layout"]["annotations"][0]["y"] = laneCap
    else:
        showWarning = True
        warningMessage = "Security lane schedule not yet uploaded"

    # Get list of all arrivals and set times to datetime
    figureData = [unixToDateTime(time) for time in arrivalData["ArrivalTime"]]
        
    # Set data for histograms
    patchedFigure["data"][0]["x"] = figureData
    patchedCaseFigure["data"][0]["x"] = figureData
    patchedCaseFigure["data"][1]["x"] = figureData
    patchedCaseFigure["data"][2]["x"] = figureData

    # Set range for case histograms
    timeRange = [min(figureData), max(figureData)]
    patchedCaseFigure["layout"]["xaxis"]["range"] = timeRange
    patchedCaseFigure["data"][0]["xbins"]["start"] = timeRange[0]
    patchedCaseFigure["data"][0]["xbins"]["end"] =   timeRange[1]

    # Adjust range if departure times are out of range
    if uploadedFlightData:
        departTimes = [unixToDateTime(time) for time in flightData["DepartureTime"]]
        timeRange = [min([*figureData, *departTimes]), max([*figureData, *departTimes])]
    
    patchedFigure["layout"]["xaxis"]["range"] = timeRange
    patchedFigure["data"][0]["xbins"]["start"] = timeRange[0]
    patchedFigure["data"][0]["xbins"]["end"] =   timeRange[1]

    # Show histograms
    patchedDivStyle["display"] = "block"

    return showWarning, warningMessage, patchedFigure, patchedDivStyle, patchedCaseFigure



@callback(
    Output({"section": "inputs",  "type": "graph", "index": "total-arrivals"}, "figure",
           allow_duplicate = True),
    Output({"section": "inputs",  "type": "graph", "index": "case-arrivals"},  "figure",
           allow_duplicate = True),
    Input({ "section": "inputs",       "type": "input",     "index": "time-slots", "flight": ALL, "info": "capacity",   "count": ALL}, "value"),
    Input({ "section": "inputs",       "type": "input",     "index": "time-slots", "flight": ALL, "info": "start-time", "count": ALL}, "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},       "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},        "data"),
    State({ "section": "inputs",       "type": "graph",     "index": "total-arrivals"}, "figure"),
    prevent_initial_call = True
)
def changeBins(capacities, slotStartTimes, arrivalData, flightData, figure):
    if arrivalData == {}:
        return no_update, no_update

    # Parse context divs
    #print(ctx.args_grouping[0])
    #triggered = [{"flight": trigger["id"]["flight"], "count": trigger["id"]["count"], "n_clicks": trigger["value"]}
    #             for trigger in ctx.args_grouping[0] if trigger["triggered"]][0]
    
    # Check if any time slots are inputted yet
    capacities = [capacity if isinstance(capacity, int) else -1 for capacity in capacities]
    totalCapacity = sum(capacities)
    if totalCapacity <= 0:
        # Patch figure: memory efficient
        patchedFigure = Patch()
        patchedCaseFigure = Patch()

        # Set color for total arrivals histogram
        patchedFigure["data"][0]["marker"]["color"] = "hsv(240,100%,40%)"

        # Reset case histograms
        figureData = [unixToDateTime(time) for time in arrivalData["ArrivalTime"]]
            
        # Set data and x-axis range, and show histograms
        patchedCaseFigure["data"][0]["x"] = figureData
        patchedCaseFigure["data"][1]["x"] = figureData
        patchedCaseFigure["data"][2]["x"] = figureData
        
        return patchedFigure, patchedCaseFigure

    # Determine start and end of histograms
    figureData = [time for time in arrivalData["ArrivalTime"]]
    binStart = min(figureData)
    binEnd = max(figureData)
    binSize = 15 * 60                                            # FIXED VALUE AS THE SECURITY CAPACITY IS GIVEN ONLY FOR 15 MIN.

    # Convert inputs to unix
    unixSlots = [time24ToUnix(time, -1) for time in slotStartTimes]

    # Find out in which bin each starting time belongs
    histBinStarts = [binStart + i * binSize for i in range((int(binEnd) - int(binStart)) // binSize)]
    binSlotIndices = [
        max([
            i if start > time or isclose(start, time) else -1
            for i, time in enumerate(histBinStarts)
        ])
        for start in unixSlots
    ]

    # Get capacity of time slots per bin
    binCapacity = [
        sum([capacities[i] for i, index in enumerate(binSlotIndices)
             if index > -1 and capacities[i] > -1
             and index == binIdx])
        for binIdx in range(len(histBinStarts))
    ]

    # Set bin color weighted by capacity
    weightedCapacity = [cap / totalCapacity for cap in binCapacity]

    # if weight > 0 set change color in different ways
    colorInterp = [
        f"hsv({240 - 80 * weight:.0f},{60 - 50 * weight:.0f}%,{60 + 40 * weight:.0f}%)" 
        if weight > 0 and not isclose(weight, 0)
        else f"hsv(240,100%,40%)"
        for weight in weightedCapacity
    ]
    
    # Patch figure for colors
    patchedFigure = Patch()
    patchedFigure["data"][0]["marker"]["color"] = colorInterp

    
    # Adjust second histogram for seeing how arrivals "change" with given time slots
    #flight = [flight if isinstance(capacity, int) else -1 for capacity in capacities]
    bestArrivalData, worstArrivalData, avgArrivalData = timeSlotCases(arrivalData["ArrivalTime"],# arrivalData["FlightNumber"],
                                                                      capacities, unixSlots, histBinStarts, binSlotIndices)
    
    # Give data to histograms
    patchedCaseFig = Patch()
    patchedCaseFig["data"][0]["x"] = [unixToDateTime(time) for time in bestArrivalData]
    patchedCaseFig["data"][1]["x"] = [unixToDateTime(time) for time in worstArrivalData]
    patchedCaseFig["data"][2]["x"] = [unixToDateTime(time) for time in avgArrivalData]

    return patchedFigure, patchedCaseFig



# Update time slots and histograms when flight is selected from dropdown
@callback(
    Output({"section": "inputs", "type": "div", "index": "time-slots-flight",       "flight": ALL}, "style"),
    Output({"section": "inputs", "type": "div", "index": "recom-time-slots-flight", "flight": ALL}, "style"),
    Output({"section": "inputs", "type": "div", "index": "time-slot-recom"},                        "style",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "div",    "index": "time-slot-inputs"},              "style"),
    Output({"section": "inputs", "type": "button", "index": "delete-time-slots"},             "disabled"),
    Output({"section": "inputs", "type": "button", "index": "suggest-time-slots"},            "children",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "button", "index": "suggest-time-slots"},            "disabled"),
    Output({"section": "inputs",  "type": "graph", "index": "total-arrivals"},                "figure",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "button", "index": "copy-recom-time-slots"},         "style",
           allow_duplicate = True),
    
    Input({ "section": "inputs",       "type": "dropdown",  "index": "flight-selection"},                       "value"),
    Input({"section": "inputs", "type": "div", "index": "time-slot-recom"},                                     "children"),
    Input({"section": "inputs", "type": "div", "index": "time-slot-inputs"},                                    "children"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},                                "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},                               "data"),
    State({ "section": "inputs",       "type": "div",       "index": "time-slots-flight",       "flight": ALL}, "style"),
    State({ "section": "inputs",       "type": "div",       "index": "recom-time-slots-flight", "flight": ALL}, "style"),
    State({ "section": "inputs",       "type": "div",       "index": "time-slot-inputs"},                       "style"),
    State({ "section": "intermediate", "type": "tracking",  "index": "prev-recom-button-state"},                "data"),
    prevent_initial_call = True
)
def showTimeSlots(flight, slotDivs, recomDivs, flightData, arrivalData, inputStyles, 
                  recomStyles, inputBlockStyle, recomsShownBefore):
    # Get patch for histogram
    patchedHistFigure = Patch()

    # Get patch for showing recommended time slots
    patchedRecStyle = Patch()

    # Make all time slot divs of both input and recommendations hide
    for i in range(len(inputStyles)):
        inputStyles[i]["display"] = "none"
    for i in range(len(recomStyles)):
        recomStyles[i]["display"] = "none"


    # If no flight is selected, empty flight stats
    if flight == "" or flight is None:
        # Notify to select a flight
        buttonDiv = dbc.Row([
            dbc.Col([
                html.I(DashIconify(icon = "ion:information-circle-outline", width = 35))
            ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
            dbc.Col([
                "Select a flight to show time slots"
            ], width = 10, align = "center")
        ], justify = "center", align = "center")

        # Hide input time slots text
        inputBlockStyle["display"] = "none"

        # Hide figure and remove data from flight specific histogram
        #patchedHistStyle["display"] = "none"
        patchedHistFigure["data"][2]["x"] = [None]
        patchedHistFigure["layout"]["shapes"][0]["x0"] = -1
        patchedHistFigure["layout"]["shapes"][0]["x1"] = -1
        patchedHistFigure["layout"]["annotations"][1]["x"] = -1

        # Hide time slot recommendations
        patchedRecStyle["display"] = "none"

        # Make patch to hide action icon for copying time slots
        patchedIcon = Patch()
        patchedIcon["display"] = "none"
        
        return inputStyles, recomStyles, patchedRecStyle, inputBlockStyle, True, buttonDiv, True, patchedHistFigure, patchedIcon


    # Search for index of flight in both time slot children and show this div
    flightIndex = flightData["FlightNumber"].index(flight)
    inputStyles[flightIndex]["display"] = "block"
    if len(recomStyles) > 0:
        recomStyles[flightIndex]["display"] = "block"

    # Show input time slots text
    inputBlockStyle["display"] = "block"
    
    # Make the notification a button to get suggestions for time slots
    # If recommendations were shown before, make button a hide button for recoms
    if recomsShownBefore:
        buttonDiv = dbc.Row([
            dbc.Col([
                html.I(DashIconify(icon = "ion:eye-off-outline", width = 35))
            ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
            dbc.Col([
                "Click to hide recommendations"
            ], width = 10, align = "center")
        ], justify = "center", align = "center"),

        # Hide recommendations
        patchedRecStyle["display"] = "block"

        # Show action icon for copying time slots
        patchedIcon = Patch()
        patchedIcon["display"] = "block"
        
    else:
        buttonDiv = dbc.Row([
            dbc.Col([
                html.I(DashIconify(icon = "ion:bulb-outline", width = 35))
            ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
            dbc.Col([
                "Click for time slot recommendations"
            ], width = 10, align = "center")
        ], justify = "center", align = "center"),

        # Show recommendations
        patchedRecStyle["display"] = "none"

        # Show action icon for copying time slots
        patchedIcon = Patch()
        patchedIcon["display"] = "none"

    # Show histograms if arrivals are uploaded
    if arrivalData == {} or arrivalData == ""  or arrivalData is None:
        # Hide time slots recoms
        inputBlockStyle["display"] = "none"

        # Remove data from histogram
        patchedHistFigure["data"][2]["x"] = [None]

    else:
        # Show figure
        #patchedHistStyle["display"] = "block"

        # Set hover info
        patchedHistFigure["data"][2]["hovertemplate"] = "Arrivals of flight " + flight + "<br>Time interval: %{x}<br>Amount of arrivals: %{y}<extra></extra>"

        # Set data for flight specific histogram
        patchedHistFigure["data"][2]["x"] = [
            unixToDateTime(time)
            for time, flightNumber in zip(arrivalData["ArrivalTime"], arrivalData["FlightNumber"])
            if flightNumber == flight
        ]

        # Get flight departure time for vline and set x's
        departTime = unixToDateTime(flightData["DepartureTime"][flightData["FlightNumber"].index(flight)])
        patchedHistFigure["layout"]["shapes"][0]["x0"] = departTime
        patchedHistFigure["layout"]["shapes"][0]["x1"] = departTime
        patchedHistFigure["layout"]["annotations"][1]["x"] = departTime

    # Return data of flight
    return inputStyles, recomStyles, patchedRecStyle, inputBlockStyle, False, buttonDiv, False, patchedHistFigure, patchedIcon



# Make new time slot input option when button for this purpose is pressed
@callback(
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"},                    "children",
           allow_duplicate = True),

    Input({ "section": "inputs",       "type": "button",    "index": "time-slots", "info": "add-time-slot"}, "n_clicks"),
    State({ "section": "inputs",       "type": "dropdown",  "index": "flight-selection"},                    "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},                             "data"),
    State({ "section": "inputs",       "type": "div",       "index": "time-slots-outer"},                    "children"),
    prevent_initial_call = True
)
def addTimeSlotInput(n_clicks, flight, flightData, children):
    if flight == "" or flight is None:
        return no_update
    
    # Make patch so new component can be added
    patchedChildren = Patch()
    
    # Get the count of different time slots inputs for this flight
    flightIndex = flightData["FlightNumber"].index(flight)
    count = len(children[flightIndex]["props"]["children"])
    
    # Add new component to front
    patchedChildren[flightIndex]["props"]["children"].insert(0, timeSlotsDiv(flight, count))
    return patchedChildren



# Remove time slots when activation button is pressed
@callback(
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"},                                                "children",
           allow_duplicate = True),
           
    Input({ "section": "inputs",       "type": "button",     "index": "time-slots", "flight": ALL, "info": "remove-slot", "count": ALL}, "n_clicks"),
    State({ "section": "inputs",       "type": "div",       "index": "time-slots-outer"},                                                "children"),
    State({ "section": "inputs",       "type": "dropdown",  "index": "flight-selection"},                                                "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},                                                         "data"),
    prevent_initial_call = True
)
def removeTimeSlotsInput(n_clicks, divs, flight, flightData):
    # Check if flight is selected and whether callback is triggered by creation of button
    amountTriggered = sum([trigger["triggered"] for trigger in ctx.args_grouping[0]])
    if flight == "" or flight is None or amountTriggered > 1:
        return divs

    # Get info on trigger
    triggered = [{"flight": trigger["id"]["flight"], "count": trigger["id"]["count"], "n_clicks": trigger["value"]}
                 for trigger in ctx.args_grouping[0] if trigger["triggered"]][0]

    # If there is only one flight and a button was created, return
    if triggered["n_clicks"] == 0:
        return divs

    # Remove component in div using trigger ID
    flightIndex, componentIndex = [
        (i,j)
        for i, inputFlight in enumerate(divs) if triggered["flight"] in str(inputFlight["props"]["children"])
        for j, inputRow in enumerate(inputFlight["props"]["children"]) if str(triggered["count"]) in str(inputRow)
    ][0]
    divs[flightIndex]["props"]["children"].pop(componentIndex)
    
    # Return divs
    return divs



# Save time slot parameters when submit button is clicked
@callback(
    Output({"section": "intermediate", "type": "parameters", "index": "time-slots"},   "data",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "text",       "index": "input-check"},  "children",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "alert",       "index": "input-check"}, "color",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "alert",      "index": "input-check"},  "is_open",
           allow_duplicate = True),
    Output({"section": "intermediate", "type": "parameters", "index": "lane-cap"},     "data"),
    
    Input({ "section": "inputs", "type": "button",   "index": "submit-time-slots"},                                             "n_clicks"),
    State({ "section": "inputs", "type": "input",    "index": "time-slots", "flight": ALL, "info": "capacity",   "count": ALL}, "value"),
    State({ "section": "inputs", "type": "input",    "index": "time-slots", "flight": ALL, "info": "start-time", "count": ALL}, "value"),
    State({ "section": "inputs", "type": "dropdown", "index": "time-slot-duration"},                                            "value"),
    State({ "section": "inputs", "type": "text",     "index": "input-check"},                                                   "children"),
    State({ "section": "inputs", "type": "input",    "index": "lane-cap"},                                                      "value"),
    prevent_initial_call = True
)
def storeTimeSlots(n_clicks, capacitiesS, timeSlotsStart, timeSlotsDuration, warningText, laneCap):
    # Get all data from the states
    capacities, startTimes = ctx.args_grouping[1:3]

    # Save time slot info per flight, giving a list with {capacity, unix start time} dicts
    timeSlotsInfo = timeSlotsFromDiv(capacities, startTimes)

    # Check for missing data: only one of capacity or start time given
    missing = [
        flightNumber
        for flightNumber in timeSlotsInfo
        if any(
            [
                ((not isinstance(cap, int) or cap == 0) and isinstance(start, int)) or 
                (isinstance(cap, int) or cap > 0) and not isinstance(start, int)
                for cap, start in zip(timeSlotsInfo[flightNumber]["capacity"], timeSlotsInfo[flightNumber]["start"])
            ]
        )
    ]

    # Check for missing data: no duration given
    timeSlotsInfo.update({"slot-duration": timeSlotsDuration})
    if not isinstance(timeSlotsInfo["slot-duration"], int):
        missing += ["time slot duration"]

    # If missing data, prevent time slot update and give message where data is missing
    if len(missing) > 0:
        errorMessage = [
            html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)), 
            "  Missing input in " + ", ".join(missing)
        ]
        return no_update, errorMessage, "danger", True, no_update

    # Remove this error if from this function
    if warningText != "" and "Missing input in" in warningText[1]:
        return timeSlotsInfo, "", no_update, False, laneCap
    else:    
        return timeSlotsInfo, no_update, no_update, no_update, no_update



# Save time slots so they can be retreived later (very similar function to storeTimeSlots)
@callback(
    Output({"section": "inputs",       "type": "interval",   "index": "save-time-slots" }, "disabled",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "text",     "index": "save-time-slots"},    "children",
           allow_duplicate = True),

    Output({"section": "inputs",       "type": "text",       "index": "input-check"}, "children",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "alert",      "index": "input-check"}, "color",
           allow_duplicate = True),
    Output({"section": "inputs",       "type": "alert",      "index": "input-check"}, "is_open",
           allow_duplicate = True),
    
    Input({ "section": "inputs", "type": "button",   "index": "save-time-slots"},                                               "n_clicks"),
    State({ "section": "inputs", "type": "input",    "index": "time-slots", "flight": ALL, "info": "capacity",   "count": ALL}, "value"),
    State({ "section": "inputs", "type": "input",    "index": "time-slots", "flight": ALL, "info": "start-time", "count": ALL}, "value"),
    State({ "section": "inputs", "type": "dropdown", "index": "time-slot-duration"},                                            "value"),
    State({ "section": "inputs", "type": "text",     "index": "input-check"},                                                   "children"),
    prevent_initial_call = True
)
def saveTimeSlots(n_clicks, capacities, timeSlotsStart, timeSlotsDuration, warningText):
    # Get all data from the states
    capacities, startTimes = ctx.args_grouping[1:3]

    # Save time slot info per flight, giving a list with {capacity, unix start time} dicts
    timeSlotsInfo = timeSlotsFromDiv(capacities, startTimes)
    
    # Check for missing data: only one of capacity or start time given
    missing = [
        flightNumber
        for flightNumber in timeSlotsInfo
        if any(
            [
                ((not isinstance(cap, int) or cap == 0) and isinstance(start, int)) or 
                (isinstance(cap, int) or cap > 0) and not isinstance(start, int)
                for cap, start in zip(timeSlotsInfo[flightNumber]["capacity"], timeSlotsInfo[flightNumber]["start"])
            ]
        )
    ]

    # Check for missing data: no duration given
    timeSlotsInfo.update({"slot-duration": timeSlotsDuration})
    if not isinstance(timeSlotsInfo["slot-duration"], int):
        missing += ["time slot duration"]

    # Create folder to save time slots in
    Path("./timeslots").mkdir(exist_ok = True)

    # Find a non-existing file name
    pathName = "./timeslots/save"
    nameIndex = 0
    while Path(pathName + ".json").is_file():
        nameIndex += 1
        pathName = pathName.split('_')[0] + f'_{nameIndex}'

    # Save timeSlots to file
    with open(pathName + ".json", 'w', encoding = "utf-8") as f:
        json.dump(timeSlotsInfo, f, ensure_ascii = False, indent = 4)

    # If missing data, prevent time slot update and give message where data is missing
    saveDiv = "Saved!"
    warningMessage = []
    showWarning = False
    if len(missing) > 0:
        saveDiv = "Warning!"
    
        warningMessage = [
            html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)), 
            "  Saved with missing input in " + ", ".join(missing)
        ]
        showWarning = True

    # Don't update warning message if not needed
    if showWarning:
        return False, saveDiv, warningMessage, "warning", showWarning
    else:
        # Remove warning if from this function
        if warningText != "" and "Saved with missing input in" in warningText[1]:
            return False, saveDiv, "", no_update, False
        else:
            return False, saveDiv, no_update, no_update, no_update



# After interval time update the text back to original
@callback(
    Output({"section": "inputs",  "type": "interval",  "index": "save-time-slots"}, "disabled"),
    Output({"section": "inputs",  "type": "text",      "index": "save-time-slots"}, "children"),
    
    Input({ "section": "inputs",  "type": "interval",  "index": "save-time-slots"}, "n_intervals"),
    prevent_initial_call = True
)
def notifySaveTimeSlots(n_intervals):
    return True, "Save time slots"



# Load saved time slots
@callback(
    Output({"section": "inputs", "type": "div",      "index": "time-slots-outer"},   "children",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "text",     "index": "load-time-slots" },   "children",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "interval", "index": "load-time-slots"},    "disabled",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "dropdown", "index": "time-slot-duration"}, "value"),

    Output({"section": "inputs", "type": "text",     "index": "input-check"},        "children",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "alert",    "index": "input-check"},        "color",
           allow_duplicate = True),
    Output({"section": "inputs", "type": "alert",    "index": "input-check"},        "is_open",
           allow_duplicate = True),
    
    Input({ "section": "inputs", "type": "upload",   "index": "load-time-slots"},    "contents"),         
    State({ "section": "inputs", "type": "dropdown", "index": "flight-selection"},   "options"),
    State({ "section": "inputs", "type": "text",     "index": "input-check"},        "children"),
    prevent_initial_call = True
)
def loadTimeSlots(contents, options, warningText):
    if contents is None:
        warningMessage = [
            html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)), 
            "  No contents found in uploaded file. Inputted time slots are not replaced."
        ]
        
        return no_update, "No contents!", False, no_update, warningMessage, "danger", True

    # Check if flights have been uploaded
    if options is None:
        warningMessage = [
            html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)), 
            "  Upload the flight schedule first."
        ]
        
        return no_update, no_update, True, no_update, warningMessage, "warning", True
    
    try:
        # Decode contents
        contents_type, contents_string = contents.split(',')
        decoded = base64.b64decode(contents_string)
        
        # Decode json-file
        loadedTimeSlots = json.loads(decoded)

        # First get time slot duration
        slotsDuration = loadedTimeSlots.pop("slot-duration")
    
        # Determine whether there are flights missing for dropdown
        dropdownFlights = [option["value"] for option in options]
        missingFlightsDashboard = [flight for flight in loadedTimeSlots if not flight in dropdownFlights]
    
        # Make warning if flights missing
        showWarning = False
        warningMessage = []
        uploadStatusMessage = "Success!"
        if len(missingFlightsDashboard) > 0:
            showWarning = True
            
            warningMessage = [
                html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)), 
                "  No uploaded flights found for " + ", ".join(missingFlightsDashboard)
            ]
    
            uploadStatusMessage = "Warning!"
    
        # Make divs from uploaded time slots
        missingFlightsUpload = [flight["value"] for flight in options if not flight["value"] in loadedTimeSlots.keys()]
        divs = [
            dbc.Row(
                children = [
                    timeSlotsDiv(flight, i, unixToDateTime(time), cap)
                    for i, (time, cap) in enumerate(zip(loadedTimeSlots[flight]["start"], loadedTimeSlots[flight]["capacity"]))
                ],
                id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight},
                style = {"display": "none"},
                justify = "center",
                align = "center",
            )
            if not flight in missingFlightsUpload
            else dbc.Row(
                children = [timeSlotsDiv(flight, 0)],
                id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight},
                style = {"display": "none"},
                justify = "center",
                align = "center",
            )
            for flight in dropdownFlights
        ]

        # Don't update warning if not needed
        if showWarning:
            return divs, uploadStatusMessage, False, slotsDuration, warningMessage, "warning", showWarning
        else:
            # Remove warning message if from this function
            if warningText != "" and ("No uploaded flights found for" in warningText[1] or 
               "There was an error parsing this file." in warningText[1]):
                return divs, uploadStatusMessage, False, slotsDuration, "", no_update, False
            else:
                return divs, uploadStatusMessage, False, slotsDuration, no_update, no_update, no_update
        
    except Exception as e:
        warningMessage = [
            html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)),
            "  There was an error while parsing the file."
        ]
        
        return no_update, "Error!", False, no_update, warningMessage, "danger", True




# After interval time update the text back to original
@callback(
    Output({"section": "inputs", "type": "interval",  "index": "load-time-slots"},  "disabled"),
    Output({"section": "inputs", "type": "text",      "index": "load-time-slots" }, "children"),
    Input({ "section": "inputs", "type": "interval",  "index": "load-time-slots"},  "n_intervals"),
    prevent_initial_call = True
)
def notifyUploadTimeSlots(n_intervals):
    return True, "Upload time slots"



# Show recommended time slots when button is pressed
@callback(
    Output({"section": "inputs",       "type": "div",       "index": "time-slot-recom-outer"},   "style"),
    Output({"section": "inputs",       "type": "div",       "index": "time-slot-recom"},         "children"),
    Output({"section": "inputs",       "type": "button",    "index": "copy-recom-time-slots"},   "style"),
    Output({"section": "inputs",       "type": "text",      "index": "input-check"},             "children"),
    Output({"section": "inputs",       "type": "alert",     "index": "input-check"},             "color"),
    Output({"section": "inputs",       "type": "alert",     "index": "input-check"},             "is_open"),
    Output({"section": "inputs",       "type": "button",    "index": "suggest-time-slots"},      "children"),
    Output({"section": "intermediate", "type": "tracking",  "index": "prev-recom-button-state"}, "data"),
    
    Input({ "section": "inputs",       "type": "button",    "index": "suggest-time-slots"},      "n_clicks"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},                "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},                 "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "lanes"},                   "data"),
    State({ "section": "inputs",       "type": "dropdown",  "index": "time-slot-duration"},      "value"),
    State({ "section": "intermediate", "type": "tracking",  "index": "prev-recom-button-state"}, "data"),
    State({ "section": "inputs",       "type": "text",      "index": "input-check"},             "children"),
    State({ "section": "inputs",       "type": "input",     "index": "lane-cap"},                "value"),
    prevent_initial_call = True
)
def showRecomSlots(n_clicks, arrivalData, flightData, laneData, slotsDuration, prevButtonGoal, warningText, laneCap):
    if prevButtonGoal:
        # Change button purpose
        buttonDiv = dbc.Row([
            dbc.Col([
                html.I(DashIconify(icon = "ion:bulb-outline", width = 35))
            ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
            dbc.Col([
                "Click for time slot recommendations"
            ], width = 10, align = "center")
        ], justify = "center", align = "center"),

        # Patch styles to hide the slots
        patchedStyleTimeSlotsDiv = Patch()
        patchedStyleArrow = Patch()
        patchedStyleTimeSlotsDiv["display"] = "none"
        patchedStyleArrow["display"] = "none"

        recomDivs = []

    else:
        # Give warning and return when no time slot duration is given
        if not isinstance(slotsDuration, int):
            warningMessage = [
                html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25)),
                "  For time slot recommendations the time slot duration needs to be given"
            ]

            return no_update, no_update, no_update, warningMessage, "warning", True, no_update, prevButtonGoal

        
        # Get recommendations from function
        recomDict = recommendedTimeSlots(arrivalData, laneData, flightData, slotsDuration, laneCap)

        # Remove recommendations with zero capacities
        recomDict = {
            flight: {
                "start":    [start for i, start in enumerate(recomDict[flight]["start"]) 
                             if recomDict[flight]["capacity"][i] > 0],
                "capacity": [cap   for cap in recomDict[flight]["capacity"] if cap > 0]
            }
            for flight in recomDict
        }

        # Make divs from determined recommended time slots
        recomDivs = [
            dbc.Row(
                children = [
                    timeSlotsRecsDiv(flight, i, unixToDateTime(time), cap)
                    for i, (time, cap) in enumerate(zip(recomDict[flight]["start"], recomDict[flight]["capacity"]))
                ],
                id = {"section": "inputs", "type": "div", "index": "recom-time-slots-flight", "flight": flight},
                style = {"display": "none"},
                justify = "center",
                align = "center",
            )
            for flight in recomDict
            if flight in recomDict.keys()
        ]
        
        # Change button purpose
        buttonDiv = dbc.Row([
            dbc.Col([
                html.I(DashIconify(icon = "ion:eye-off-outline", width = 35))
            ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
            dbc.Col([
                "Click to hide recommendations"
            ], width = 10, align = "center")
        ], justify = "center", align = "center")

        # Patch the style to show the slots
        patchedStyleTimeSlotsDiv = Patch()
        patchedStyleArrow = Patch()
        patchedStyleTimeSlotsDiv["display"] = "block"
        patchedStyleArrow["display"] = "block"

    
    # Switch stored variable
    prevButtonGoal = not prevButtonGoal

    # Remove warning if from this function
    if warningText != "" and "For time slot recommendations the time slot duration needs to be given" in warningText[1]:
        # If time slots were calculated, return them else no update
        if len(recomDivs) > 0:
            return patchedStyleTimeSlotsDiv, recomDivs, patchedStyleArrow, "", no_update, False, buttonDiv, prevButtonGoal
        else:
            return patchedStyleTimeSlotsDiv, no_update, patchedStyleArrow, "", no_update, False, buttonDiv, prevButtonGoal
    else:
        if len(recomDivs) > 0:
            return patchedStyleTimeSlotsDiv, recomDivs, patchedStyleArrow, no_update, no_update, no_update, buttonDiv, prevButtonGoal
        else:
            return patchedStyleTimeSlotsDiv, no_update, patchedStyleArrow, no_update, no_update, no_update, buttonDiv, prevButtonGoal



# Take over recommendations when actionIcon is clicked
@callback(
    Output({"section": "inputs", "type": "div",    "index": "time-slots-outer"},                                                     "children",
           allow_duplicate = True),
    Input({ "section": "inputs", "type": "button", "index": "copy-recom-time-slots"},                                                "n_clicks"),
    State({ "section": "inputs", "type": "input",  "index": "time-slots-recom", "flight": ALL, "info": "capacity",   "count": ALL}, "value"),
    State({ "section": "inputs", "type": "input",  "index": "time-slots-recom",  "flight": ALL, "info": "start-time", "count": ALL}, "value"),
    prevent_initial_call = True
)
def takeOverRecoms(n_clicks, recomCapacities, recomSlotsStart):
    # Get time slot recommendations info, CHANGE OF VARIABLE NAMES
    recomCapacities = ctx.args_grouping[1]
    recomSlotsStart = ctx.args_grouping[2]
    recomTimeSlots = timeSlotsFromDiv(recomCapacities, recomSlotsStart)
    
    # Make divs for input time slots
    inputDivs = [
        dbc.Row(
            children = [
                timeSlotsDiv(flight, i, unixToDateTime(time), cap)
                for i, (time, cap) in enumerate(zip(recomTimeSlots[flight]["start"], recomTimeSlots[flight]["capacity"]))
            ],
            id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight},
            style = {"display": "none"},
            justify = "center",
            align = "center",
        )
        if recomTimeSlots[flight]["start"][0] is not None
        else dbc.Row(
            [timeSlotsDiv(flight, 0)],
            id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight},
            style = {"display": "none"},
            justify = "center",
            align = "center",
        )
        for flight in recomTimeSlots.keys()
    ]

    return inputDivs



# Take over recommendations when actionIcon is clicked
@callback(
    Output({"section": "inputs", "type": "div",      "index": "time-slots-outer"},  "children"),
    Input({ "section": "inputs", "type": "button",   "index": "delete-time-slots"}, "n_clicks"),
    State({ "section": "inputs", "type": "dropdown", "index": "flight-selection"},  "options"),
    prevent_initial_call = True
)
def deleteInputs(n_clicks, options):
   # For each flight create a row with single time slot input
    divs = [
        dbc.Row(
            children = [timeSlotsDiv(flight["value"], 0)],
            id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight["value"]},
            style = {"display": "none"},
            justify = "center",
            align = "center",
        )
        for flight in options
    ]
    
    return divs



# Change max capacity in histogram
@callback(
    Output({"section": "inputs",       "type": "graph",     "index": "total-arrivals"}, "figure"),
    Output({"section": "inputs",       "type": "graph",     "index": "case-arrivals"},  "figure"),
    Input({ "section": "inputs",       "type": "input",     "index": "lane-cap"},       "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "arrivals"},       "data"),
    State({ "section": "intermediate", "type": "dataframe", "index": "lanes"},          "data"),
    prevent_initial_call = True
)
def showLanes(laneCap, arrivalData, laneData):
    if arrivalData == {} or laneData == {}:
        return no_update, no_update
    else:
        # Figure patches: memory efficient
        patchedFigure = Patch()
        patchedCaseFigure = Patch()

        # Change lane capacity over time in figure with arrivals
        patchedFigure["data"][1]["x"] = [unixToDateTime(time) for time in laneData["Time"]]
        patchedFigure["data"][1]["y"] = [amountLanes * laneCap for amountLanes in laneData["Lanes"]]
        patchedFigure["layout"]["annotations"][0]["text"] = "Security<br>capacity"
        patchedFigure["layout"]["annotations"][0]["y"] = laneCap

        patchedCaseFigure["data"][3]["x"] = [unixToDateTime(time) for time in laneData["Time"]]
        patchedCaseFigure["data"][3]["y"] = [amountLanes * laneCap for amountLanes in laneData["Lanes"]]
        patchedCaseFigure["layout"]["annotations"][0]["text"] = "Security<br>capacity"
        patchedCaseFigure["layout"]["annotations"][0]["y"] = laneCap

        return patchedFigure, patchedCaseFigure
