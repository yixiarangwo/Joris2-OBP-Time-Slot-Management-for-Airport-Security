from dash import dcc, html

import dash_bootstrap_components as dbc

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from inputs.functions import *
from inputs.graphs import *
from designs import *

# Time slot and capacity inputs on input tab
timeSlotsInput = [
    dbc.Row([
        # Submit button for time slots
        dbc.Col([
            submitButton(
                "Submit time slots",
                "ion:options-outline",
                {"section": "inputs", "type": "button", "index": "submit-time-slots"},
                {"marginLeft": "0.8rem"}
            )
        ], width = 2),

        # Error message for incomplete input
        dbc.Col([
            dbc.Alert(
                html.Div(
                    "",
                    id = {"section": "inputs", "type": "text", "index": "input-check"},
                    style = {
                        "text-align": "center",
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                        "white-space": "nowrap",
                        "color": "black",
                        "padding": 0,
                        "margin": 0
                    }
                ),
                id = {"section": "inputs", "type": "alert", "index": "input-check"},
                style = {
                    "height": "2.5rem",
                    "width": "34.8rem",
                    "border":"2px black solid",
                    "padding": 0,
                    "margin": 0,
                    "marginLeft": "2.2rem",
                    "marginRight": "-0.4rem"
                },
                className = "fw-bold d-flex align-items-center justify-content-center border-2",
                color = "danger",
                fade = True,
                is_open = False,
            ),
        ], width = 6),

        # Warning message for no uploaded arrivals
        dbc.Col([
            dbc.Alert(
                html.Div(
                    id = {"section": "inputs", "type": "text", "index": "arrival-check"},
                    style = {
                        "text-align": "center",
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                        "white-space": "nowrap",
                        "color": "black",
                    }
                ),
                id = {"section": "inputs", "type": "alert", "index": "arrival-check"},
                style = {
                    "height": "2.5rem",
                    "width": "23.3rem",
                    "border":"2px black solid",
                    "margin": 0,
                    "padding": 0,
                    "marginLeft": "-0.5rem",
                },
                className = "fw-bold d-flex align-items-center justify-content-center",
                color = "warning",
                fade = True,
                is_open = False
            ),
        ], width = 4),
    ], justify = "center", align = "center"),
    
    
    ### Picking flight for time slot input
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                # Dropdown for setting time-slot duration
                dbc.Card(
                    children = [
                        dcc.Dropdown(
                            id = {"section": "inputs", "type": "dropdown", "index": "time-slot-duration"},
                            options = [
                                {"label": "5 min",  "value": 300},
                                {"label": "10 min", "value": 600},
                                {"label": "15 min", "value": 900}
                            ],
                            searchable = False,
                            placeholder = "Select time slot duration",
                            style = {
                                "width": "13rem",
                                "text-align": "left",
                            },
                            value = ""
                        ),
                    ],
                    body = True,
                    style = {
                        "width": "6rem", 
                        "maxWidth": "40%",
                        "height": "3.5rem"
                    },
                    color = "secondary",
                    className = "justify-content-center align-items-center",
                ),
    
                # Dropdown with input for selecting flight
                dbc.Card(                                                                                   # Utility: Display
                    children = [                                                                            # Or try fixed-left/fixed-right (from fixed-bottom/fixed-top)
                        dcc.Dropdown(
                            id = {"section": "inputs", "type": "dropdown", "index": "flight-selection"},
                            placeholder = "Select a flight",
                            optionHeight = 25,
                            style = {"width": "20rem"},
                            value = "",
                        ),
                    ], 
                    body = True,
                    style = {
                        "width": "6rem",
                        "height": "3.5rem"
                    },
                    color = "secondary",
                    className = "justify-content-center align-items-center",
                )
            ], style = {"width": "36rem"})
        ], width = True),

        ## Alert when no flight is selected, which then gets converted to a button to get time slot recoms.
        dbc.Col([
            dbc.Button(
                dbc.Row([
                    dbc.Col([
                        html.I(DashIconify(icon = "ion:information-circle-outline", width = 35))
                    ], width = 2, align = "center", style = {"paddingLeft": "0.5rem"}),
                    dbc.Col([
                        "Select a flight to show time slots"
                    ], width = 10, align = "center")
                ], justify = "center", align = "center"),
                id = {"section": "inputs", "type": "button", "index": "suggest-time-slots"},
                style = {
                    "width": "12.5rem",
                    "height": "3.45rem",
                    "paddingTop": 0,
                    "paddingBottom": 0,
                    "textAlign": "center",
                    "font-size": "16px",
                    "font-weight": "bold",
                    "color": "black",
                },
                className = "justify-content-center",
                disabled = True,
                color = "primary"
            ),
        ], width = True, align = "center"),

        ## Upload and button for loading and saving time-slots
        dbc.Col([
            dbc.Card(
                # Upload saved time slots
                dcc.Upload(
                    children = dbc.Row([
                        dbc.Col([
                            html.A(
                                "Upload time slots",
                                id = { "section": "inputs", "type": "text", "index": "load-time-slots" }
                            )
                        ], width = 10, align = "center", style = {"padding": 0, "margin": 0, "text-align": "center"}),
                        dbc.Col([
                            DashIconify(icon = "ion:push-outline", width = 25)
                        ], width = 2, align = "center", style = {"padding": 0, "margin": 0, "text-align": "left"})
                    ]),
                    id = { "section": "inputs", "type": "upload", "index": "load-time-slots" },
                    style = {
                        "font-size": "16px",
                        "font-weight": "bold",
                        "color": "black"
                    },
                    multiple = False
                ),
                body = True,
                className = "justify-content-center",
                style = {
                    "height": "2.5rem",
                    "width": "11rem"
                },
                color = "dark",
            )
            
        ], width = True),
         dbc.Col([
            # Save time slots button            
            dbc.Button(
                children = dbc.Row([
                    dbc.Col([
                        html.Label(
                            "Save time slots",
                            id = {"section": "inputs", "type": "text", "index": "save-time-slots"}
                        )
                    ], width = 10, align = "center", style = {"padding": 0, "margin": 0, "text-align": "center"}),
                    dbc.Col([
                        DashIconify(icon = "ion:download-outline", width = 25)
                    ], width = 2, align = "center", style = {"padding": 0, "margin": 0, "text-align": "left"})
                ]),
                id = {"section": "inputs", "type": "button", "index": "save-time-slots"},
                style = {
                    "height": "2.5rem",
                    "width": "10rem",
                    "textAlign": "center",
                    "font-size": "16px",
                    "font-weight": "bold",
                    "color": "black"
                },
                color = "dark"
            ),
        ], width = True),
    ], justify = "center", align = "center", style = {"marginTop": "1rem", "marginBottom": "1rem"}),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    children = [
                        html.H5(
                            "Time slot input", 
                            style = {
                                "text-align": "center",
                                "marginBottom": 0
                            }
                        ),
        
                        # Column names
                        dbc.Row([
                            dbc.Col([
                                html.Label(
                                    "Start time",
                                    style = {
                                        "marginTop": "0.5rem",
                                        "marginBottom": "0.5rem",
                                        "font-size": "1.1rem"
                                    }
                                ),
                            ], width = 6, style = {"text-align": "right"}),
                            dbc.Col([
                                html.Label(
                                    "Capacity",
                                    style = {
                                        "marginTop": "0.5rem",
                                        "marginBottom": "0.5rem",
                                        "marginLeft": "-0.6rem",
                                        "font-size": "1.1rem"
                                    }
                                )
                            ], width = 6, style = {"text-align": "left"})
                        ], justify = "center", align = "center"),
            
                        # Time slots input
                        dbc.Row([
                            # Button to add option for inputting new time slot
                            dbc.Col([
                                dbc.Row([
                                    dmc.ActionIcon(
                                        DashIconify(icon = "ion:add", width = 35),
                                        id = {"section": "inputs", "type": "button", "index": "time-slots", "info": "add-time-slot"},
                                        style = {
                                            "margin": 0,
                                            "padding": 0,
                                            "width": "2.25rem",
                                        },
                                        title = "Add time slot",
                                        size = "2.25rem",
                                        mb = "2.25rem",
                                        n_clicks = 0,
                                    ),  
                                ], justify = "start", align = "start")
                            ], width = 1, align = "start", style = {"padding": 0, "margin": 0, "marginRight": "-0.8rem"}),
                
                            # Show input for selected flight
                            dbc.Col([
                                dbc.Row(
                                    id = {"section": "inputs", "type": "div", "index": "time-slots-outer"},
                                    align = "start",
                                    justify = "center",
                                    style = {
                                        "overflowY": "auto",
                                        "width": "15.7rem",
                                        "height": "15rem",
                                        "margin": 0,
                                        "padding": 0,
                                    }
                                ),
                            ], width = 11, align = "start", style = {"width": "16rem", "padding": 0, "margin": 0, "marginLeft": "-0.7rem", "paddingLeft": "0.9rem"}),
                        ], justify = "center", style = {"padding": 0, "margin": 0}),
                    ], 
                    id = {"section": "inputs", "type": "div", "index": "time-slot-inputs"},
                    style = {"display": "none"},
                ),
                style = {"height": "24.5rem"},
                color = "secondary"
            ),
            width = 3
        ),

        dbc.Col([
            # Max arrival capacity input
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        html.Label(
                            "Security capacity (15 min)",
                            style = {
                                "tex-align": "center",
                                "width": "50rem",
                                "padding": 0,
                                "margin": 0
                            }
                        ),
                    ], justify = "center", align = "end", style = {"padding": 0, "margin": 0, "text-align": "center", "marginLeft": "-0.8rem", "width": "8rem"}),
                        
                    # Input for security lane capacity
                    dbc.Row([
                        dmc.NumberInput(
                            id = {"section": "inputs", "type": "input", "index": "lane-cap"},
                            style = {
                                "height": "2rem",
                                "width": "5rem",
                                "margin": 0,
                                "padding": 0,
                            },
                            value = 40,
                            precision = 0,
                            min = 1
                        ),
                    ], justify = "center", align = "start", style = {"padding": 0, "margin": 0}),
                ], style = {"padding": 0, "margin": 0})
            ], justify = "center", align = "center", style = {"padding": 0, "margin": 0, "height": f"{1/3:%}"}),
        
            dbc.Row([
                # Button to copy time slot recommendatations to inputs
                dmc.ActionIcon(
                    DashIconify(icon = "ion:arrow-back", width = 35),
                    id = {"section": "inputs", "type": "button", "index": "copy-recom-time-slots"},
                    style = {
                        "display": "none",
                        "margin": 0, 
                        "padding": 0,
                        "width": "2.25rem"
                    },
                    title = "Take over recommended time slots",
                    size = "2.25rem",                
                ),
            ], justify = "center", align = "center", style = {"padding": 0, "margin": 0, "height": f"{1/3:%}"}),
            
            dbc.Row([
                # Button to delete time slot inputs
                dmc.ActionIcon(
                    DashIconify(icon = "ion:trash-outline", width = 35),
                    id = {"section": "inputs", "type": "button", "index": "delete-time-slots"},
                    style = {
                        "margin": 0, 
                        "padding": 0,
                        "width": "2.25rem",
                    },
                    title = "Delete all inputted time slots",
                    size = "2.25rem",
                    disabled = True
                ),
            ], justify = "center", align = "center", style = {"padding": 0, "margin": 0, "height": f"{1/3:%}"})
        ], style = {"height": "24.5rem", "padding": 0, "margin": 0}, align = "center", width = 1),

        ## Time slot recommendations
        dbc.Col(
            dbc.Card(
                children = dbc.CardBody(
                    children = [
                        html.H5(
                            "Time slot recommendations", 
                            style = {
                                "text-align": "center",
                                "marginBottom": 0
                            }
                        ),
        
                        # Column names
                        dbc.Row([
                            dbc.Col([
                                html.Label(
                                    "Start time",
                                    style = {
                                        "marginTop": "0.5rem",
                                        "marginBottom": "0.5rem",
                                        "font-size": "1.1rem"
                                    }
                                ),
                            ], width = 6, style = {"text-align": "right"}),
                            dbc.Col([
                                html.Label(
                                    "Capacity",
                                    style = {
                                        "marginTop": "0.5rem",
                                        "marginBottom": "0.5rem",
                                        "font-size": "1.1rem"
                                    }
                                )
                            ], width = 6, style = {"text-align": "left"})
                        ], justify = "center", align = "center"),
                        # Show recommendations for selected flight    
                        dbc.Row(
                        
                            id = {"section": "inputs", "type": "div", "index": "time-slot-recom"},
                            align = "start",
                            justify = "center",
                            style = {
                                "overflowY": "auto",
                                "height": "15rem",
                                "margin": 0,
                                "padding": 0,
                            }
                        ),
                    ], 
                    id = {"section": "inputs", "type": "div", "index": "time-slot-recom-outer"},
                    style = {"display": "none"},
                ),
                style = {"height": "24.5rem"},
                color = "secondary"
            ),
            align = "center",
            width = 3,
        ),
        
        dbc.Col([
            dbc.Card(
                children = dbc.CardBody([
                    # Histogram for showing total arrivals
                    dbc.Row([
                        dcc.Graph(
                            figure = totalArrivalsHistogram,
                            id = {"section": "inputs", "type": "graph", "index": "total-arrivals"},
                            config = {"displayModeBar": False},
                            style = {
                                "margin": 0,
                                "padding": 0,
                                "height": "100%",
                            },
                            responsive = True
                        ),
                    ], align = "start", style = {"margin": 0, "padding": 0, "height": "50%"}),
                    
                    # Histogram for showing arrivals per flight
                    dbc.Row([
                        dcc.Graph(
                            figure = caseArrivalsHistogram,
                            id = {"section": "inputs", "type": "graph", "index": "case-arrivals"},
                            config = {"displayModeBar": False},
                            style = {
                                "margin": 0,
                                "padding": 0,
                                "height": "100%",
                            },
                            responsive = True
                        ),
                    ], align = "end", style = {"margin": 0, "padding": 0, "height": "50%"})
                ], 
                    id = {"section": "inputs", "type": "div", "index": "arrivals-graphs"},
                    style = {"margin": 0, "padding": 0, "paddingRight": "0.75rem", "display": "none"}
                ),
                style = {
                    "margin": 0,
                    "padding": 0,
                    "height": "24.5rem",
                    "border": "none"
                },
            )
        ], width = 5, align = "center", style = {"padding": 0, "margin": 0}),
    ], justify = "center", align = "center", style = {"marginLeft": "-0.8rem", "marginRight": "0.7 rem", "height": "24.5rem"})
]
