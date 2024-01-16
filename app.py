from dash import Dash, dcc, html, Input, Output, callback
from inputs import *
#from graphs import *
from callbacks import *

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Tabs(id = "tabs", value = "tab-importables", children = [
            dcc.Tab(id = "tab-importables", label = "Importables", value = "tab-importables", children = importables),
            dcc.Tab(id = "tab-inputs",      label = "Inputs",      value = "tab-inputs",      children = inputs),
            dcc.Tab(id = "tab-analysis",    label = "Analysis",    value = "tab-analysis")#,  children = analysis)
        ]),

        # Intermediate values to store data and distribution
        dcc.Store(id = {"section": "intermediate", "type": "dataframe",     "index": "arrivals"},    storage_type = "session", data = ''),
        dcc.Store(id = {"section": "intermediate", "type": "dataframe",     "index": "flights"},     storage_type = "session", data = ''),
        dcc.Store(id = {"section": "intermediate", "type": "dataframe",     "index": "lanes"},       storage_type = "session", data = ''),
        dcc.Store(id = {"section": "intermediate", "type": "dataframe",     "index": "sim-service"}, storage_type = "session", data = '')
    ],
)

# For submit buttons, they only update initial data or parameters. 
# On analysis tab we have a "run" button from which simulation is started.

if __name__ == "__main__":
    app.run(debug = True)
