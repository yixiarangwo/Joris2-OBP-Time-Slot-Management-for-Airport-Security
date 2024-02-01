from dash import Dash, dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from analysis.graphs import *

from designs import *

analysis = [
    dbc.Offcanvas(
        children = [
            dbc.Spinner([
                dbc.Row([
                    html.H4(
                        "Security Waiting Time Simulation",
                        style = {
                            "margin": 0,
                            "padding": 0,
                            "text-align": "center",
                            "marginBottom": "1.5rem"
                        }
                    ),
                ], justify = "center", align = "center", style = {"margin": 0, "padding": 0}),
            
                dbc.Row([
                    # Alert for missing data
                    dbc.Alert(
                        dbc.Row([
                            dbc.Col([
                                html.I(DashIconify(icon = "ion:alert-circle-outline", width = 25))
                            ], width = 1, align = "center", style = {"paddingLeft": "0.5rem"}),
                            dbc.Col([
                                ""
                            ], width = 11, align = "center", id = {"section": "analysis", "type": "text", "index": "missing-data"})
                        ], justify = "center", align = "center"),
                        id = {"section": "analysis", "type": "alert", "index": "missing-data"},
                        color = "danger",
                        is_open = False,
                        style = {
                            "margin": 0,
                            "padding": 0,
                            "marginBottom": "1.5rem",
                            "text-align": "center",
                            "height": "2.5rem",
                            "width": "25rem",
                            "border": "2px black solid"
                        },
                        className = "fw-bold d-flex align-items-center justify-content-center border-2",
                    )
                ], justify = "center", align = "center"),
    
                # Input for amount of runs and button to start simulation
                dbc.Row([
                    dbc.Row([
                        dbc.Col([
                            html.Label(
                                "Amount of runs",
                                style = {
                                    "padding": 0,
                                    "text-align": "center"
                                }
                            ),
                        ], width = 5, align = "center", style = {"text-align": "end"}),
                        dbc.Col(width = 7, align = "center")
                    ], justify = "end", align = "center", style = {"margin": 0, "padding": 0}),

                    dbc.Row([
                        dbc.Col([
                            dmc.NumberInput(
                                id = {"section": "analysis", "type": "input", "index": "simulation-runs"},
                                style = {
                                    "margin": 0,
                                    "padding": 0,
                                    "marginRight": "1rem",
                                    "width": "6rem",
                                },
                                value = 5,
                                min = 1,
                                precision = 0,
                                className = "d-flex align-items-end",
                            )], 
                            width = 5, 
                            className = "d-flex justify-content-end align-items-center",
                            align = "center", 
                            style = {"margin": 0, "padding": 0}
                        ),
                        dbc.Col([
                            submitButton(
                                "Run simulation",
                                "ion:flame-outline",
                                {"section": "analysis", "type": "button", "index": "run-simulation"},
                                width = 35,
                                disabled = True,
                                buttonStyle = {"marginLeft": "1rem"}
                            )], 
                            width = 7, 
                            className = "d-flex justify-content-start align-items-center", 
                            align = "center", 
                            style = {"margin": 0, "padding": 0}
                    )], justify = "center", align = "center")
                ], justify = "center", align = "center", style = {"margin": 0, "padding": 0, "marginBottom": "3rem"}),
                
                # Overall statistsics: average waiting time per (combined) queue
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row([
                                    html.Label(
                                        children = [
                                            html.P("Average total", style = {"margin": 0, "padding": 0}),
                                            html.P("waiting time", style = {"margin": 0, "padding": 0}),
                                        ],
                                        style = {
                                            "font-size": "12px",
                                            "margin": 0,
                                            "padding": 0
                                        }
                                    ),
                                ], justify = "start", align = "start", style = {"padding": 0, "margin": 0}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-total-waiting-min"},
                                            style = {
                                                "margin": 0,
                                                "padding": 0,
                                                "marginLeft": "-0.5rem",
                                                "font-size": "40px",
                                                "text-align": "center",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "min",
                                            style = {
                                                "margin": 0, 
                                                "padding": 0, 
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        ),
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-total-waiting-sec"},
                                            style = {
                                                "margin": 0, 
                                                "padding": 0,
                                                "marginLeft": "0.2rem",
                                                "marginTop": "1.5rem",
                                                "font-size": "25px", 
                                                "text-align": "center",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "sec",
                                            style = {
                                                "margin": 0, 
                                                "padding": 0,
                                                "marginTop": "1.5rem",
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        )
                                    ], align = "center", style = {"margin": 0, "padding": 0})
                                ], justify = "center", align = "center", style = {"text-align": "end", "margin": 0, "padding": 0}),

                            ]),
                            style = {"height": "9rem"}
                        )
                    ], width = True, align = "center", style = {"padding": 0, "margin": 0}),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row([
                                    html.Label(
                                        children = [
                                            html.P("Average virtual queue", style = {"margin": 0, "padding": 0}),
                                            html.P("waiting time", style = {"margin": 0, "padding": 0}),
                                        ],
                                        style = {
                                            "font-size": "12px",
                                            "margin": 0,
                                            "padding": 0
                                        }
                                    ),
                                ], justify = "start", align = "start", style = {"padding": 0, "margin": 0}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-vq-waiting-min"},
                                            style = {
                                                "margin": 0, 
                                                "padding": 0, 
                                                "marginLeft": "-0.5rem", 
                                                "font-size": "40px", 
                                                "text-align": "center",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "min",
                                            style = {
                                                "margin": 0, 
                                                "padding": 0, 
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        ),
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-vq-waiting-sec"},
                                            style = {
                                                "margin": 0, 
                                                "padding": 0,
                                                "marginLeft": "0.2rem",
                                                "marginTop": "1.5rem",
                                                "font-size": "25px", 
                                                "text-align": "end",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "sec",
                                            style = {
                                                "margin": 0, 
                                                "padding": 0,
                                                "marginTop": "1.5rem",
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        )
                                    ], align = "center", style = {"margin": 0, "padding": 0})
                                ], justify = "center", align = "center", style = {"text-align": "end", "margin": 0, "padding": 0}),

                            ]),
                            style = {"height": "9rem"}
                        )], width = True, align = "center", style = {"padding": 0, "margin": 0}
                    ),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row([
                                    html.Label(
                                        children = [
                                            html.P("Average general queue", style = {"margin": 0, "padding": 0}),
                                            html.P("waiting time", style = {"margin": 0, "padding": 0}),
                                        ],
                                        style = {
                                            "font-size": "12px",
                                            "margin": 0,
                                            "padding": 0
                                        }
                                    ),
                                ], justify = "start", align = "start", style = {"padding": 0, "margin": 0}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-gq-waiting-min"},
                                            style = {
                                                "margin": 0, 
                                                "padding": 0, 
                                                "marginLeft": "-0.5rem",
                                                "font-size": "40px",
                                                "text-align": "end",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "min",
                                            style = {
                                                "margin": 0, 
                                                "padding": 0, 
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        ),
                                        html.Label(
                                            id = {"section": "analysis", "type": "text", "index": "sim-avg-gq-waiting-sec"},
                                            style = {
                                                "margin": 0, 
                                                "padding": 0,
                                                "marginLeft": "0.2rem",
                                                "marginTop": "1.5rem",
                                                "font-size": "25px", 
                                                "text-align": "end",
                                                "color": "white"
                                            }
                                        ),
                                        html.Label(
                                            "sec",
                                            style = {
                                                "margin": 0,
                                                "padding": 0,
                                                "marginTop": "1.5rem",
                                                "font-size": "15px", 
                                                "text-align": "end",
                                            }
                                        )
                                    ], align = "center")
                                ], justify = "center", align = "center", style = {"text-align": "end", "margin": 0, "padding": 0}),
                            ]),
                            style = {"height": "9rem"}
                        )], width = True, align = "center", style = {"padding": 0, "margin": 0}),
                    ],
                    justify = "center", 
                    align = "center",
                    className = "d-none",
                    id  = {"section": "analysis", "type": "div", "index": "sim-stats"},
                    style = {"padding": 0, "margin": 0}
                ),
            ], type = "grow", color = "primary", size = "5rem"),
        ],
        id = {"section": "analysis", "type": "panel", "index": "sim-selection"},
        is_open = False,
        style = {
            "background": "#333333",
            "margin": 0,
            "padding": 0,
            "width": "33rem"
        }
    ),

    # Action icon to open the selection panel
    dmc.ActionIcon(
        DashIconify(
            icon = "ion:ellipsis-horizontal", 
            width = 50,
            style = {
                "margin": 0,
                "padding": 0
            },
        ),
        id = {"section": "analysis", "type": "button", "index": "open-panel"},
        style = {
            "padding": 0,
            "margin": 0,
            "marginLeft": "1rem",
            "border": "none",
            "color": "white",
            "zIndex": 99,
        },
        size = "2rem",
        title = "Open selection panel",
        variant = "outline",
        className = "position-absolute top-0 start-0",
    ),

    # Panel of four figures
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id = {"section": "analysis", "type": "graph", "index": 0},
                        config = {"displayModeBar": False},
                        style = {
                            "display": "none",
                            "margin": 0, 
                            "padding": 0, 
                            "height": "100%",
                        },
                        responsive = True,
                    )
                ),
                style = {
                    "margin": 0, 
                    "padding": 0, 
                    "height": "100%",
                    "border": "1px white solid"
                },
            ),
            width = 6,
            align = "center",
            style = {
                "margin": 0, 
                "padding": 0,
                "height": "100%"
            },
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id = {"section": "analysis", "type": "graph", "index": 1},
                        config = {"displayModeBar": False},
                        style = {
                            "display": "none",
                            "margin": 0, 
                            "padding": 0, 
                            "height": "100%",
                        },
                        responsive = True,
                    )
                ),
                style = {
                    "margin": 0, 
                    "padding": 0, 
                    "height": "100%",
                    "border": "1px white solid"
                },
            ),
            width = 6,
            align = "center",
            style = {
                "margin": 0, 
                "padding": 0, 
                "height": "100%"
            },
        )],
        justify = "center",
        align = "center",
        style = {
            "margin": 0, 
            "padding": 0,
            "marginTop": "1rem", 
            "height": "50%"
        }
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id = {"section": "analysis", "type": "graph", "index": 2},
                        config = {"displayModeBar": False},
                        style = {
                            "display": "none",
                            "margin": 0, 
                            "padding": 0, 
                            "height": "100%",
                        },
                        responsive = True,
                    )
                ),
                style = {
                    "margin": 0, 
                    "padding": 0, 
                    "height": "100%",
                    "border": "1px white solid"
                },
            ),
            width = 6,
            align = "center",
            style = {
                "margin": 0, 
                "padding": 0, 
                "height": "100%"
            },
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id = {"section": "analysis", "type": "graph", "index": 3},
                        config = {"displayModeBar": False},
                        style = {
                            "display": "none",
                            "margin": 0, 
                            "padding": 0,
                            "paddingBottom": "-0.5rem", 
                            "height": "100%",
                        },
                        responsive = True,
                    )
                ),
                style = {
                    "margin": 0, 
                    "padding": 0, 
                    "height": "100%",
                    "border": "1px white solid"
                },
            ),
            width = 6,
            align = "center",
            style = {
                "margin": 0, 
                "padding": 0, 
                "height": "100%"
            },
        )],
        justify = "center",
        align = "center",
        style = {
            "margin": 0, 
            "padding": 0, 
            "height": "50%"
        }
    ),
]
