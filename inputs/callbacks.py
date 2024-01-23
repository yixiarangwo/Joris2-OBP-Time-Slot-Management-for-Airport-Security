from dash import callback, Output, Input, State, Patch, html, ALL, ctx
from dash.exceptions import PreventUpdate

from inputs.functions import *

# When flights data is updated, update dropdown options, make children for time slot inputs,
# and deselect selection in dropdown of input tab by setting its value to ""
@callback(
    Output({"section": "inputs",       "type": "dropdown",  "index": "flight-selection"}, "options"),
    Output({"section": "inputs",       "type": "dropdown",  "index": "flight-selection"}, "value"),
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"}, "children",
           allow_duplicate = True),
    
    Input({ "section": "intermediate", "type": "dataframe", "index": "flights"},          "data"),
    prevent_initial_call = True
)
def updateInputsFlights(flights):
    # Get new dropdown options
    options = [flight["FlightNumber"] for flight in flights]

    # For each flight create an html div with single time slot input
    divs = [
        html.Div(
            id = {"section": "inputs", "type": "div", "index": "time-slots-flight", "flight": flight},
            children = [timeSlotsDiv(flight, 0)],
            style = {"display": "none"}
        )
        for flight in options
    ]
    
    return options, "", divs


# Update view when flight is selected from dropdown
@callback(
    Output({"section": "inputs",       "type": "text",      "index": "flight-departure"},  "children"),
    Output({"section": "inputs",       "type": "text",      "index": "flight-passengers"}, "children"),
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"},  "children",
           allow_duplicate = True),
    
    Input({ "section": "inputs",       "type": "dropdown",  "index": "flight-selection"},  "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},           "data"),
    prevent_initial_call = True
)
def showTimeSlots(flight, flightData):
    # Make patch for changing previously shown
    patchedChildren = Patch()

    # First make all time slot divs hide
    for i in range(len(flightData)):
        patchedChildren[i]["props"]["style"]["display"] = "none"

    # If no flight is selected, empty flight stats
    if flight == "" or flight is None:
        return "", "", patchedChildren

    # Get flight dict of selected flight
    flightDict = [record for record in flightData if record["FlightNumber"] == flight][0]

    # Search for index of flight in children and show this div
    flightIndex = [i for i, record in enumerate(flightData) if record["FlightNumber"] == flight][0]
    patchedChildren[flightIndex]["props"]["style"]["display"] = "block"

    # Return data of flight
    return unixToTime24(flightDict["DepartureTime"]), flightDict["Passengers"], patchedChildren


# Make new time slot input option when button for this purpose is pressed
@callback(
    Output({"section": "inputs",       "type": "div",       "index": "time-slots-outer"}, "children",
           allow_duplicate = True),
    
    Input({ "section": "inputs",       "type": "button",    "index": "time-slots"},       "n_clicks"),
    State({ "section": "inputs",       "type": "dropdown",  "index": "flight-selection"}, "value"),
    State({ "section": "intermediate", "type": "dataframe", "index": "flights"},          "data"),
    State({ "section": "inputs",       "type": "div",       "index": "time-slots-outer"}, "children"),
    prevent_initial_call = True
)
def addTimeSlotInput(n_clicks, flight, flightData, children): # have to give flight for n_clicks property
    if flight == "" or flight is None:
        raise PreventUpdate

    # Determine the flight index in children
    flightIndex = [i for i, record in enumerate(flightData) if record["FlightNumber"] == flight][0]
    
    # Make patch so new component can be added
    patchedChildren = Patch()
    
    # Get the count of different time slots inputs for this flight
    count = len(children[flightIndex]["props"]["children"])
    
    # Add new component to front
    patchedChildren[flightIndex]["props"]["children"].insert(0, timeSlotsDiv(flight, count))
    return patchedChildren


# Save time slot parameters when submit button is clicked
@callback(
    Output({"section": "intermediate", "type": "parameters", "index": "time-slots"},                                                          "data"),
    Output({"section": "inputs",       "type": "text",       "index": "input-check"},                                                         "children"),
    
    Input({ "section": "inputs",       "type": "button",     "index": "submit-time-slots"},                                                   "n_clicks"),
    State({ "section": "inputs",       "type": "input",      "index": "time-slots", "flight": ALL, "info": "capacity",         "count": ALL}, "value"),
    State({ "section": "inputs",       "type": "input",      "index": "time-slots", "flight": ALL, "info": "start-time-hours", "count": ALL}, "value"),
    State({ "section": "inputs",       "type": "input",      "index": "time-slots", "flight": ALL, "info": "start-time-mins",  "count": ALL}, "value"),
    State({ "section": "inputs",       "type": "dropdown",   "index": "time-slot-duration"},                                                  "value"),

    State({ "section": "intermediate", "type": "parameters", "index": "time-slots"},                                                          "data"),
    prevent_initial_call = True
)
def saveTimeSlots(n_clicks, capacities, timeSlotsHours, timeSlotsMinutes, timeSlotDuration, prevTimeSlots):
    # Get all data from the states
    capacities, startHours, startMinutes = ctx.args_grouping[1:-2]

    # Save time slot info per flight, giving a list with {capacity, unix start time} dicts
    timeSlotInfo = {}

    [
        timeSlotInfo[capacity["id"]["flight"]].append(
            {
                "capacity": capacity["value"],
                "start": time24ToUnix(hours["value"], minutes["value"])
            }
        )
        if capacity["id"]["flight"] in timeSlotInfo
        else timeSlotInfo.update(
            {
                capacity["id"]["flight"]: [
                    {
                        "capacity": capacity["value"],
                        "start": time24ToUnix(hours["value"], minutes["value"])
                    }
                ]
            }
        )
        for capacity, hours, minutes in zip(capacities, startHours, startMinutes)
        if capacity["value"] != "" and int(capacity["value"]) > 0
    ]

    # Check for missing data: only one of capacity or start time given
    missing = [
        flightNumber
        for flightNumber in timeSlotInfo
        if any(
            [
                slot["capacity"] ==  "" and slot["start"] != -1
                or
                slot["capacity"] !=  "" and slot["start"] == -1
                for slot in timeSlotInfo[flightNumber]
            ]
        )
    ]

    # Check for missing data: no duration given
    timeSlotInfo.update({"slot-duration": timeSlotDuration})
    if timeSlotInfo["slot-duration"] is None or timeSlotInfo["slot-duration"] == "":
        missing += ["time slot duration"]

    # If missing data, prevent time slot update and give message where data is missing
    if len(missing) > 0:
        return prevTimeSlots, "Missing input in " + ", ".join(missing)

    return timeSlotInfo, ""
