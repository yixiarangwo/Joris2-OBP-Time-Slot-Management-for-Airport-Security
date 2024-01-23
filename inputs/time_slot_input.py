from dash import dcc, html

from inputs.functions import *

# Time slot and capacity inputs on input tab
timeSlotsInput = [
    # Submit button
    html.Button(
        "Submit time slots", 
        id = {"section": "inputs", "type": "button", "index": "submit-time-slots"},
        style = {"display": "inline-block", "margin": "2%"}
    ),

    html.Div(
        id = {"section": "inputs", "type": "text", "index": "input-check"},
        style = {"display": "inline-block", "color": "red"}
    ),

    ### Picking flight for time slot input
    html.Center(
        children = [
            # Give option for setting time-slot duration
            dcc.Dropdown(
                id = {"section": "inputs", "type": "dropdown", "index": "time-slot-duration"},
                options = [
                    {"label": "5 min",  "value": 300},
                    {"label": "10 min", "value": 600},
                    {"label": "15 min", "value": 900}
                ],
                searchable = False,
                maxHeight = 600,
                optionHeight = 20,
                placeholder = "Select duration of time slots",
                style = {
                    "display": "inline-block", 
                    "width": "25vw", 
                    "marginRight": "5vw",
                    "text-align": "left",
                },
                value = ""
            ),
            
            # Dropdown with input for selecting flight
            dcc.Dropdown(
                id = {"section": "inputs", "type": "dropdown", "index": "flight-selection"},
                placeholder = "Select a flight",
                maxHeight = 600,
                optionHeight = 20,
                style = {
                    "display": "inline-block", 
                    "width": "25vw", 
                    "marginRight": "5vw",
                    "text-align": "left",
                },
                value = "",
            ),
            
            # Show stats for selected flight
            html.Div(
                id = {"section": "inputs", "type": "text", "index": "flight-stats"},
                children = [
                    html.Label(
                        "Departure time:",  
                        style = {"marginRight": "0.25vw"}
                    ),
                    html.Label(
                        "",
                        id = {"section": "inputs", "type": "text", "index": "flight-departure"},
                        style = {"marginRight": "2vw"}
                    ),
                    html.Label(
                        "Passengers booked:",  
                        style = {"marginRight": "0.25vw"}
                    ),
                    html.Label(
                        "",
                        id = {"section": "inputs", "type": "text", "index": "flight-passengers"},
                    ),
                ],
                style = {"display": "inline-block", "verticalAlign": "50%"},
            ),
        ],
    ),

    # Button to add option for inputting new time slot
    html.Button(
        "Add time-slot",
        id = {"section": "inputs", "type": "button", "index": "time-slots"},
        style = {"margin": "2%"}
    ),
    
    # Show input for selected flight
    html.Center(
        children = html.Div(
            id = {"section": "inputs", "type": "div", "index": "time-slots-outer"},
            children = [],
        ),
    )
]
