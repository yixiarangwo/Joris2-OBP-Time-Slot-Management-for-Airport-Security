from dash import dash, html, callback, Output, Input, State, Patch, MATCH
from dash.exceptions import PreventUpdate

from latex2sympy2 import latex2sympy
import numpy as np
import time

from importables.functions import *

# When uploading an importable save it as json in records format
# Also changes interval component for temporary notification through text of upload component
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": MATCH}, "data"),
    Output({"section": "importables",  "type": "interval",  "index": MATCH}, "disabled",
           allow_duplicate = True),
    Output({"section": "importables",  "type": "upload",    "index": MATCH}, "children",
           allow_duplicate = True),
    Input({ "section": "importables",  "type": "upload",    "index": MATCH}, "contents"),
    State({ "section": "intermediate", "type": "dataframe", "index": MATCH}, "data"),
    prevent_initial_call = True
) 
def storeImportables(contents, prevData):
    # Try to parse contents
    json, status = parseContents(contents)

    # If parsed successfully, overwrite data and show succes notification
    if status:
        return json, False, ["Succes!"]

    # Else, do not change data and show fail notification
    return prevData, False, ["Error!"]


# After interval time update the text back to original for new file upload
@callback(
    Output({"section": "importables",  "type": "interval",  "index": MATCH}, "disabled"),
    Output({"section": "importables",  "type": "upload",    "index": MATCH}, "children"),
    Input({ "section": "importables",  "type": "interval",  "index": MATCH}, "n_intervals"),
)
def notifyImportFile(n_intervals):
    return True, ["Drag and Drop or ", html.A("Select a File")]


# Store inputted info about distribution
@callback(
    Output({"section": "intermediate", "type": "parameters", "index": "sample-info"}, "data",
           allow_duplicate = True),
    Output({"section": "intermediate", "type": "parameters", "index": "test-info"},    "data"),
    
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
    
    return sampleInfo, testInfo


# Update LaTeX version of inputted distribution live
@callback(
    Output({"section": "importables", "type": "text",  "index": "server-dist"},                    "children"),
    Input({ "section": "importables", "type": "input", "index": "server-dist", "info": "formula"}, "value"),
    State({ "section": "importables", "type": "text",  "index": "server-dist"},                    "children")
)
def showLaTeX(latex, prevLatex):
    # Check if no expression
    if latex == '':
        return ''
    
    # Make complete LaTeX math expression
    latexMath = "$$f_S(x) = " + latex + "$$"

    # Check if correct LaTeX
    correctLatex = latexToNumpy(latex)
    if correctLatex is not None:
        return latexMath
    else:
        if isinstance(prevLatex, list):
            return "(not valid)"
        elif "(not valid)" in prevLatex:
            return prevLatex
        else:
            return prevLatex + " (not valid)"


# Update plot of sampled service times if distribution changed
@callback(
    Output({"section": "importables",  "type": "graph",      "index": "sim-service"}, "figure"),
    Output({"section": "importables",  "type": "graph",      "index": "sim-service"}, "style"),
    Output({"section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),

    Input({ "section": "intermediate", "type": "parameters", "index": "sample-info"}, "data"),
    Input({ "section": "intermediate", "type": "parameters", "index": "test-info"},   "data"),
    
    State({"section": "importables", "type": "graph", "index": "sim-service"}, "style"),
    background = True,
    prevent_initial_call = True
)
def plotServiceTimes(sampleInfo, testInfo, style):
    # Sample service times for testing
    testSample, initial = metropolisHastings(**sampleInfo, **testInfo)

    # Use Patch so we don't need to create a complete figure but just update the data
    patchedFigure = Patch()

    # Make plot of test sample
    if testSample is not None:
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

    return patchedFigure, style, sampleInfo
