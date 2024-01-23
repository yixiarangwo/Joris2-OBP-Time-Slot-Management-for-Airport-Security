from dash import Dash, dcc, html
from dash.long_callback import DiskcacheLongCallbackManager

import diskcache

from importables.importables import importables
from inputs.inputs import inputs
from analysis.analysis import analysis

from importables.callbacks import *
from inputs.callbacks import *
from analysis.callbacks import *

# Make long callback processes possible
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheLongCallbackManager(cache)

# Make app
app = Dash(__name__, background_callback_manager = background_callback_manager)

app.layout = html.Div(
    [
        dcc.Tabs(id = "tabs", value = "tab-importables", children = [
            dcc.Tab(id = "tab-importables", label = "Importables", value = "tab-importables", children = importables),
            dcc.Tab(id = "tab-inputs",      label = "Inputs",      value = "tab-inputs",      children = inputs),
            dcc.Tab(id = "tab-analysis",    label = "Analysis",    value = "tab-analysis",    children = analysis),
        ]),
        
        # For testing callbacks
        html.Div(id = "test", style = {"display": "none"})
    ],
)

if __name__ == "__main__":
    app.run(debug = True)
