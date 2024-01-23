from dash import dcc, html
from importables.graphs import *

serviceInput = [
    ### Service time distribution
    html.Div(
        children = [
            # Title
            html.H3("Service time distribution"),

            html.Div(
                children = [
                    # Latex input
                    html.Div(
                        children = [
                            html.Label("Give (proportional) distribution in terms of x"),
                            dcc.Textarea(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "formula"},
                                placeholder = "Enter service distribution in LaTeX format here",
                                style = {"display": "block", "width": "22.5vw", "height": "2.5vw"},
                                value = r"\exp(-x)"
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "float": "left",
                            "marginRight": "1vw"
                        }
                    ),
                    
                    # Lower bound distribution input
                    html.Div(
                        children = [
                            html.Label("Lower bound"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bound"},
                                style = {"display": "block", "width": "6vw"},
                                type = "number",
                                value = 0
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "float": "left",
                            "marginRight": "1vw"
                        }
                    ),
            
                    # Upper bound distribution input
                    html.Div(
                        children = [
                            html.Label("Upper bound"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bound"},
                                style = {"display": "block", "width": "6vw"},
                                type = "number"
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "float": "left",
                        }
                    ),
                ],
                style = {"display": "block"}
            ),
            

            html.Div(
                children = [
                    ## Other info for sample test
                    # Input amount test samples
                    html.Div(
                        children = [
                            html.Label("Test sample size"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "amount-test-samples"},
                                style = {"display": "block", "alignItems": "center", "width": "6vw"},
                                type = "number",
                                value = 3000
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "textAlign": "center", 
                            "alignItems": "center",
                            "float": "left",
                            "marginRight": "1vw"
                        }
                    ),
            
                    # Input sigma
                    html.Div(
                        children = [
                            html.Label("Step size (sigma)"),
                            
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "sigma"},
                                style = {"display": "block", "width": "6vw"},
                                type = "number",
                                value = 1
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "textAlign": "center", 
                            "alignItems": "center",
                            "marginRight": "1vw"
                        }
                    ),
            
                    # Input burn in steps
                    html.Div(
                        children = [
                            html.Label("Burn in steps"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "burn-in"},
                                style = {"display": "block", "width": "6vw"},
                                type = "number",
                                value = 1000
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "textAlign": "center", 
                            "alignItems": "center",
                            "marginRight": "1vw"
                        }
                    ),
            
                    # Input lower bound expansion
                    html.Div(
                        children = [
                            html.Label("Lower expansion"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bounds-expansion"},
                                style = {"display": "block", "width": "6vw"},
                                type = "number",
                                value = 3
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "textAlign": "center", 
                            "alignItems": "center",
                            "marginRight": "1vw"
                        }
                    ),
            
                    # Input upper bound expansion
                    html.Div(
                        children = [
                            html.Label("Upper expansion"),
                            dcc.Input(
                                id = {"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bounds-expansion"},
                                style = {
                                    "display": "block", 
                                    "width": "6vw", 
                                    "verticalAlign": "middle", 
                                    "horizontalAlign": "middle"
                                },
                                type = "number",
                                value = 3
                            ),
                        ],
                        style = {
                            "display": "inline-block",
                            "textAlign": "center",
                            "alignItems": "center",
                        }
                    ),
                ],
                style = {
                    "display": "inline-block",
                    "textAlign": "center",
                    "alignItems": "center",
                    "marginTop": "1vw"
                }
            ),
            
            
            ## Output of importables tab
            # Show function from LaTeX
            dcc.Markdown(
                id = {"section": "importables", "type": "text", "index": "server-dist"},
                children = [], 
                mathjax = True, 
                style = {"font-size": "125%"}
            ),
            
            # Submit button
            html.Button(
                "Submit distribution",
                id = {"section": "importables", "type": "button", "index": "server-dist"}, 
            ),
    
            # Show graph of sampled service times
            dcc.Graph(
                figure = serviceTestFig,
                id = {"section": "importables", "type": "graph", "index": "sim-service"},
                style = {"display": "none", "width": "40vw", "height": "40vh", "marginTop": "3%"},
                config = {"displayModeBar": False}
            )
            
        ], 
        style = {
            "float": "left", 
            "margin": "auto", 
            "marginLeft": "0%", 
            "marginRight": "0%",
            "width": "50vw",
        }
    )
]
