from dash import dash, html, callback, Output, Input, State, Patch, MATCH, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from dash_iconify import DashIconify

from latex2sympy2 import latex2sympy
import numpy as np
import time

from importables.functions import *


# Store arrivals as json in list format
# Also changes interval component for temporary notification through text of upload component
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    Output({"section": "importables",  "type": "interval",  "index": "arrivals"}, "disabled",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "arrivals"}, "children",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "arrivals"}, "style",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "icon",      "index": "arrivals"}, "style"),
    
    Output({"section": "importables",  "type": "text",      "index": "file-check"}, "children",
           allow_duplicate = True),
    Output({"section": "importables", "type": "alert",      "index": "file-check"}, "is_open",
           allow_duplicate = True),
    
           
    Input({ "section": "importables",  "type": "upload",    "index": "arrivals"}, "contents"),
    prevent_initial_call = True
) 
def storeArrivals(contents):
    # Try to parse contents
    json, status = parseContents(contents)
    
    # Get patch of style for centering text and changing icon color
    patchedStyle = Patch()
    patchedStyle["textAlign"] = "center"

    # Get patch of style icon color, indicating file has been uploaded
    patchedIcon = Patch()

    # If parsed successfully, check for completeness of data, overwrite data and show succes notification
    if status:
        # Check for completeness of data by type of file upload
        if arrivalDataCheck(json):
            patchedIcon["color"] = "white"
            print(json)
            return json, False, ["Succes!"], patchedStyle, patchedIcon, "", False
        else:
            errorText = dbc.Row([
                html.H5(
                    "File contents incomplete", 
                    style = {
                        "text-align": "center",
                        "color": "white",
                        "marginBottom": 0
                    },
                    className = "fw-bold"
                )
            ])
            return no_update, False, ["Error!"],  patchedStyle, no_update, errorText, True

    # Make error text
    errorText = dbc.Row([
        html.H5(
            "Error while parsing file", 
            style = {
                "text-align": "center",
                "color": "white",
                "marginBottom": 0
            },
            className = "fw-bold"
        )
    ])

    # Else, do not change data and show fail notification
    return no_update, False, ["Error!"], patchedStyle, no_update, errorText, True



# Store flights as json in list format
# Also changes interval component for temporary notification through text of upload component
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "flights"}, "data"),
    Output({"section": "importables",  "type": "interval",  "index": "flights"}, "disabled",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "flights"}, "children",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "flights"}, "style",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "icon",      "index": "flights"}, "style"),
    
    Output({"section": "importables",  "type": "text",      "index": "file-check"}, "children",
           allow_duplicate = True),
    Output({"section": "importables", "type": "alert",      "index": "file-check"}, "is_open",
           allow_duplicate = True),
    
           
    Input({ "section": "importables",  "type": "upload",    "index": "flights"}, "contents"),
    prevent_initial_call = True
) 
def storeFlights(contents):
    # Try to parse contents
    json, status = parseContents(contents)
    
    # Get patch of style for centering text and changing icon color
    patchedStyle = Patch()
    patchedStyle["textAlign"] = "center"

    # Get patch of style icon color, indicating file has been uploaded
    patchedIcon = Patch()

    # If parsed successfully, check for completeness of data, overwrite data and show succes notification
    if status:
        # Check for completeness of data by type of file upload
        if flightDataCheck(json):
            patchedIcon["color"] = "white"
            print(json)
            return json, False, ["Succes!"], patchedStyle, patchedIcon, "", False
        else:
            errorText = dbc.Row([
                html.H5(
                    "File contents incomplete", 
                    style = {
                        "text-align": "center",
                        "color": "white",
                        "marginBottom": 0
                    },
                    className = "fw-bold"
                )
            ])
            return no_update, False, ["Error!"],  patchedStyle, no_update, errorText, True

    # Make error text
    errorText = dbc.Row([
        html.H5(
            "Error while parsing file", 
            style = {
                "text-align": "center",
                "color": "white",
                "marginBottom": 0
            },
            className = "fw-bold"
        )
    ])

    # Else, do not change data and show fail notification
    return no_update, False, ["Error!"], patchedStyle, no_update, errorText, True



# Store security lane data as json in list format
# Also changes interval component for temporary notification through text of upload component
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    Output({"section": "importables",  "type": "interval",  "index": "lanes"}, "disabled",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "lanes"}, "children",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": "lanes"}, "style",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "icon",      "index": "lanes"}, "style"),
    
    Output({"section": "importables",  "type": "text",      "index": "file-check"}, "children"),
    Output({"section": "importables", "type": "alert",      "index": "file-check"}, "is_open"),
    
           
    Input({ "section": "importables",  "type": "upload",    "index": "lanes"}, "contents"),
    prevent_initial_call = True
) 
def storeLanes(contents):
    # Try to parse contents
    json, status = parseContents(contents)
    
    # Get patch of style for centering text and changing icon color
    patchedStyle = Patch()
    patchedStyle["textAlign"] = "center"

    # Get patch of style icon color, indicating file has been uploaded
    patchedIcon = Patch()

    # If parsed successfully, check for completeness of data, overwrite data and show succes notification
    if status:
        if laneDataCheck(json):
            patchedIcon["color"] = "white"
            print(json)
            return json, False, ["Succes!"], patchedStyle, patchedIcon, "", False
        else:
            errorText = dbc.Row([
                html.H5(
                    "File contents incomplete", 
                    style = {
                        "text-align": "center",
                        "color": "white",
                        "marginBottom": 0
                    },
                    className = "fw-bold"
                )
            ])
            return no_update, False, ["Error!"],  patchedStyle, no_update, errorText, True

    # Make error text
    errorText = dbc.Row([
        html.H5(
            "Error while parsing file", 
            style = {
                "text-align": "center",
                "color": "white",
                "marginBottom": 0
            },
            className = "fw-bold"
        )
    ])

    # Else, do not change data and show fail notification
    return no_update, False, ["Error!"], patchedStyle, no_update, errorText, True



# After interval time update the text back to original for new file upload
@callback(
    Output({"section": "importables",  "type": "interval",  "index": MATCH}, "disabled"),
    Output({"section": "importables",  "type": "upload",    "index": MATCH}, "children"),
    Output({"section": "importables",  "type": "upload",    "index": MATCH}, "style"),
    Input({ "section": "importables",  "type": "interval",  "index": MATCH}, "n_intervals"),
    prevent_initial_call = True
)
def notifyImportFile(n_intervals):
    # Get patch of style for aligning text to right
    stylePatch = Patch()
    stylePatch["textAlign"] = "right"

    return True, ["Drag and Drop or ", html.A("Select a File ")], stylePatch



# Store inputted info about distribution
@callback(
    Output({"section": "intermediate", "type": "parameters", "index": "sample-info"},                    "data",
           allow_duplicate = True),
    Output({"section": "intermediate", "type": "parameters", "index": "test-info"},                      "data"),
    Output({"section": "importables",  "type": "input",      "index": "server-dist", "info": "formula"}, "valid",
           allow_duplicate = True),
    Output({"section": "importables", "type": "alert",  "index": "serivce-input"},                       "children"),
    Output({"section": "importables", "type": "alert",  "index": "serivce-input"},                       "style"),
    Output({"section": "importables", "type": "graph",  "index": "sim-service"},                         "style",
           allow_duplicate = True),
    Output({"section": "importables", "type": "button", "index": "server-dist"},                         "loading",
           allow_duplicate = True),
    Output({"section": "importables", "type": "input", "index": "server-dist", "info": "sigma"},         "invalid"),
    
    Input({"section": "importables", "type": "button", "index": "server-dist"}, "n_clicks"),
    
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "formula"},     "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bound"}, "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bound"}, "value"),

    State({"section": "importables", "type": "input", "index": "server-dist", "info": "amount-test-samples"},    "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "sigma"},                  "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "burn-in"},                "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bounds-expansion"}, "value"),
    State({"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bounds-expansion"}, "value"),
    
    prevent_initial_call = True
)
def storeServiceDistInfo(n_clicks, latex, lower, upper, amountSamples, sigma, burnIn, lowerExpansion, upperExpansion):    
    ## Check whether inputs are given and if valid
    invalid = False
    errorText = []
    if latexToNumpy(latex) is None:
        errorText += [
            html.Label(
                "LaTeX expression is not valid.",
                style = {
                    "text-align": "center",
                    "color": "white",
                },
                className = "fw-bold"
            )
        ]
    if not isinstance(sigma, float) and not isinstance(sigma, int):
        invalid = True
        errorText += [
            html.Label(
                "The step size must be positive.",
                style = {
                    "text-align": "center",
                    "color": "white"
                },
                className = "fw-bold"
            )
        ]

    # If missing crucial info, return
    if invalid:
        errorDiv = dbc.Row([html.H5(
            "Invalid input", 
            style = {
                "text-align": "center",
                "color": "white",
                "marginBottom": "0.1rem"
            },
            className = "fw-bold"
        )] + [error for error in errorText], justify = "center", align = "center"),

        # Show error
        patchedErrorDiv = Patch()
        patchedErrorDiv["display"] = "block"

        # Hide figure
        patchedFigure = Patch()
        patchedFigure["display"] = "none"

        return no_update, no_update, False, errorDiv, patchedErrorDiv, patchedFigure, False, True

    # Set correct format if not
    lower = lower if isinstance(lower, int) else None
    upper = upper if isinstance(upper, int) else None
    
    lowerExpansion = lowerExpansion if isinstance(lowerExpansion, int) else None
    upperExpansion = upperExpansion if isinstance(upperExpansion, int) else None
    
    amountSamples = amountSamples if isinstance(amountSamples, int) else 0
    
    burnIn = burnIn if isinstance(burnIn, int) else 0
    
    lowerExpansion = lowerExpansion if isinstance(lowerExpansion, int) else None
    upperExpansion = upperExpansion if isinstance(upperExpansion, int) else None

    # Store info for sampling
    sampleInfo = {
        "latex":          latex,
        "lower":          lower,
        "upper":          upper,
        "sigma":          sigma,
        "lowerExpansion": lowerExpansion,
        "upperExpansion": upperExpansion,
        "initial":        ""
    }

    # Store info for testing sampling info
    testInfo = {
        "amountSamples": amountSamples,
        "burnIn":        burnIn,
    }

    # Hide error
    patchedErrorDiv = Patch()
    patchedErrorDiv["display"] = "none"

    # Hide figure if no samples to be displayed
    patchedFigure = Patch()
    if amountSamples <= 0:
        patchedFigure["display"] = "none"
    
    return sampleInfo, testInfo, True, [], patchedErrorDiv, patchedFigure, True, False 


# Update LaTeX version of inputted distribution live, show in textarea if invalid input
@callback(
    Output({"section": "importables", "type": "text",  "index": "server-dist"},                    "children"),
    Output({"section": "importables", "type": "input", "index": "server-dist", "info": "formula"}, "invalid"),
    Output({"section": "importables", "type": "input", "index": "server-dist", "info": "formula"}, "valid"),
    Input({ "section": "importables", "type": "input", "index": "server-dist", "info": "formula"}, "value"),
)
def showLaTeX(latex):
    # Check if no expression
    if latex == '':
        return '', False, False
    
    # Make complete LaTeX math expression
    latexMath = "$$f_S(x) = " + latex + "$$"

    # Check if correct LaTeX
    correctLatex = latexToNumpy(latex)
    if correctLatex is not None:
        return latexMath, False, False
    else:
        return no_update, True, False



# Update textarea when option from dropdown is chosen
@callback(
    Output({"section": "importables", "type": "input",    "index": "server-dist", "info": "formula"}, "value"),
    Input({ "section": "importables", "type": "dropdown", "index": "formula-selection"},              "value"),
    prevent_initial_call = True
)
def replaceLaTeXDropdown(chosen):
    return chosen



# Update plot of sampled service times if distribution changed
@callback(
    Output({"section": "importables",  "type": "graph",      "index": "sim-service"}, "figure"),
    Output({"section": "importables",  "type": "graph",      "index": "sim-service"}, "style"),
    Output({"section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),
    Output({"section": "importables",  "type": "button",     "index": "server-dist"}, "loading"),

    Input({ "section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),
    Input({ "section": "intermediate", "type": "parameters", "index": "test-info"},   "data"),
    
    State({"section": "importables", "type": "graph", "index": "sim-service"}, "style"),
    prevent_initial_call = True
)
def plotServiceTimes(sampleInfo, testInfo, style):
    # Sample service times for testing
    testSample, initial = metropolisHastings(**sampleInfo, **testInfo)

    # Use Patch so we don't need to create a complete figure but just update the data
    patchedFigure = Patch()

    # Make plot of test sample if test sample is wanted
    if (testSample is not None) and (testInfo["amountSamples"] > 0):
        # Evenly spread points for plotting inputted function
        minX = sampleInfo["lower"] if sampleInfo["lower"] is not None else testSample.min()
        maxX = sampleInfo["upper"] if sampleInfo["upper"] is not None else testSample.max()
        xPoints = np.linspace(minX, maxX, 100)
        yPoints = latexToNumpy(**sampleInfo)(xPoints)

        # Set data for figure
        patchedFigure["data"][0]["xbins"] = {"start": minX, "end": maxX}
        patchedFigure["data"][0]["x"] = testSample
        patchedFigure["data"][1]["x"] = xPoints
        patchedFigure["data"][1]["y"] = yPoints

        # Set x-axis domain
        patchedFigure["layout"]["xaxis"]["domain"] = [minX, maxX]

        # Show figure
        style["display"] = "block"

        # Add initial value for simulation, preventing another burn in
        sampleInfo["initial"] = initial
        
    else:
        # Free memory from figure
        patchedFigure["data"][0]["x"] = []
        patchedFigure["data"][1]["x"] = []
        patchedFigure["data"][1]["y"] = []
        
        # Hide figure
        style["display"] = "none"

    return patchedFigure, style, sampleInfo, False
    
