from dash import callback, Input, State, Output
from dash.exceptions import PreventUpdate

from analysis.functions import *

@callback(
    Output("test", "children"),            #switch to graphs, this is just for test
    
    Input({ "section": "analysis",     "type": "button",       "index": "start-simulation"}, "n_clicks"),
    
    State({ "section": "intermediate", "type": "distribution", "index": "formula-info"},    "data"),
    State({ "section": "intermediate", "type": "parameters",   "index": "sample-info"},     "data"),
    State({ "section": "intermediate", "type": "dataframe",    "index": "arrivals"},        "data"),
    State({ "section": "intermediate", "type": "dataframe",    "index": "lanes"},           "data"),
    State({ "section": "intermediate", "type": "parameters",   "index": "time-slots"},      "data"),
    background = True,
    prevent_initial_call = True
)
def runSimulation(n_clicks, formulaInfo, sampleInfo, arrivalData, laneData, timeSlotData):
    ### Sampling service times
    # Extract distribution and sampling info
    latex, lower, upper, initial = formulaInfo.values()
    sigma, lowerExpansion, upperExpansion = sampleInfo.values()

    # Determine how many samples are needed
    amountSamples = len(arrivalData) # * (times) amount of runs

    # Get service times
    serviceTimes = MHsamples(latex, amountSamples, sigma, initial,
                             lower, upper, lowerExpansion, upperExpansion)
    
    ### Run simulation
    raise PreventUpdate


    ### Make graphs

    # Show other statistics
    
