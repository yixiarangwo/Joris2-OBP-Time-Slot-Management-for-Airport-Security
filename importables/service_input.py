from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from importables.graphs import *
from designs import *

def inputWithTitle(name, id, width = True, value = "", textStyle = {}, colStyle = {}, **kwargs):
    return dbc.Col([
        dbc.Row([
            html.Label(
                name,
                style = {"text-align": "center"} | textStyle
            ),
            dbc.Input(
                **kwargs,
                id = id,
                style = {"width": "6rem"},
                type = "number",
                value = value,
            ),
        ], justify = "center"),
    ], width = width, align = "center", style = colStyle)


distributionInput = [
    dbc.Col([
        dbc.Row([
            html.Label(
                "Give (unscaled) distribution w.r.t. x",
                style = {"text-align": "center"}
            ),
            html.Div([
                dbc.Select(
                    options = [
                        {"label": "Exponential",     "value": r"\exp{-\left| x \right|}"},
                        {"label": "Uniform",         "value": r"1"},
                        {"label": "Normal",          "value": r"\exp{- \frac{1}{2} (\frac{x-\mu}{\sigma})^2}"},
                        {"label": "Standard Normal", "value": r"\exp{- \frac{x^2}{2}}"},
                    ],
                    id = {"section": "importables", "type": "dropdown", "index": "formula-selection"},
                    placeholder = "Distributions",
                    style = {
                        "width": "24.5rem",
                        "border":"1px black solid",
                        "marginRight": "0.35rem",
                        "height": "2.5rem",
                    },
                    value = "",
                ),
                dbc.Textarea(
                    id = {"section": "importables", "type": "input", "index": "server-dist", "info": "formula"},
                    placeholder = "Enter service distribution in LaTeX format here",
                    style = {
                        "width": "21.5rem", 
                        "height": "2.5rem",
                        "border":"1px black solid",
                        "marginTop": "-2.5rem",
                        "position": "absolute",
                        "zIndex": "1"
                    },
                    value = r"\exp(-\frac{\left| x \right|}{20})",
                    invalid = False,
                    valid = False
                ),
            ])
        ], justify = "center", align = "center", style = {"margin": 0, "padding": 0}),
    ], width = True),
    
    inputWithTitle(
        "Lower bound", 
        {"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bound"},
        value = 0,
        colStyle = {"margin": 0, "padding": 0}
    ),
    
    inputWithTitle(
        "Upper bound",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bound"},
        colStyle = {"marginLeft": 0, "padding": 0}
    ),
]


sampleInput = [
    # Input amount test samples
    inputWithTitle(
        "Test sample size",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "amount-test-samples"},
        value = 3000,
        colStyle = {"margin": 0, "padding": 0},
        min = 1
    ),
    
    # Input sigma
    inputWithTitle(
        "Step size (sigma)",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "sigma"},
        value = 10,
        colStyle = {"margin": 0, "padding": 0},
        min = 0.00001
    ),
    
    # Input burn in steps
    inputWithTitle(
        "Burn in steps",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "burn-in"},
        value = 1000,
        colStyle = {"margin": 0, "padding": 0},
        min = 0
    ),
    
    # Input lower bound expansion
    inputWithTitle(
        "Lower expansion",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bounds-expansion"},
        value = 20,
        colStyle = {"margin": 0, "padding": 0},
        min = 0
    ),
    
    # Input upper bound expansion
    inputWithTitle(
        "Upper expansion",
        {"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bounds-expansion"},
        value = 2,
        textStyle = {"width": "150%"},
        colStyle = {"margin": 0, "padding": 0},
        min = 0
    )
]


serviceInput = [
    html.H4(
        "Service time distribution",
        className = "card-title",
    ),

    dbc.Row([
        dbc.Card(
            children = [
                # Distribution service times info
                dbc.Row(
                    children = distributionInput,
                    style = {
                        "paddingLeft": "1rem", 
                        "paddingRight": "1rem", 
                        "paddingTop": "0.5rem",
                        "paddingBottom": "0.5rem"
                    }
                ),

                # Other info for sample test
                dbc.Row(
                    children = sampleInput,
                    style = {
                        "paddingLeft": "1rem", 
                        "paddingRight": "1rem", 
                        "paddingBottom": "1rem"
                    }
                )
            ],
            style = {"width": "97%"},
            color = "secondary",
            class_name = "justify-content-center"
        ),
    ], justify = "center"),
    
    ## Output of importables tab
    # Show function from LaTeX
    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                id = {"section": "importables", "type": "text", "index": "server-dist"},
                style = {
                    "font-size": "125%", 
                    "text-align": "center",
                    "paddingTop": "1rem",
                },
                children = [],
                className ="h-50",
                mathjax = True,
            ),  
        ], width = 8, align = "center"),

        # Submit distribution button
        dbc.Col([
            submitButton(
                "Submit distribution",
                "ion:speedometer-outline",
                {"section": "importables", "type": "button", "index": "server-dist"},
                {"margin-top": "1rem", "margin-bottom": "1rem"}
            ),
        ], width = 4, align = "center"),
    ], justify = "center", align = "center", style = {"margin-top": "0.25rem", "margin-bottom": "0.25rem", "max-width": "97%"}),
    
    dbc.Row([
        dbc.Spinner([
            dbc.Row([
                # Error message input service info
                dbc.Alert(
                    children = [],
                    id = {"section": "importables", "type": "alert", "index": "serivce-input"},
                    style = {
                        "display": "none",
                        "flex-direction": "column",
                        "width": "31rem",
                        "margin": 0,
                        "padding": "0.25rem",
                        "border":"2px black solid",
                    },
                    color = "danger",
                    className = "justify-content-center"
                ),
                # Show graph of sampled service times
                dcc.Graph(
                    figure = serviceTestFig,
                    id = {"section": "importables", "type": "graph", "index": "sim-service"},
                    style = {
                        "display": "none",
                        "width": "31rem", 
                        "height": "12.5rem",
                        "marginRight": 0,
                        "marginBottom": 0
                    },
                    config = {"displayModeBar": False}
                ),
            ], justify = "center", align = "center")
        ], type = "grow", color = "primary", size = "5rem"),
    ], justify = "center", align = "center", style = {"height": "12.5rem"})
]
