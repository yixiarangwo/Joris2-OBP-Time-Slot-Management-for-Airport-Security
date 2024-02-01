from dash import Dash, dcc, html
from dash.long_callback import DiskcacheLongCallbackManager
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

# Load theming for figures (needs to be loaded before import of components)
load_figure_template(["cyborg"])

from importables.importables import importables
from inputs.inputs import inputs
from analysis.analysis import analysis

from importables.stored import stored as storedImportables
from inputs.stored import stored as storedInputs

from importables.callbacks import *
from inputs.callbacks import *
from analysis.callbacks import *

# Make app
app = Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])

app.layout = dbc.Container(
    [
        dbc.Tabs(
            children = [
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(importables),
                        style = {
                            "marginBottom": 0, 
                            "paddingBottom": 0,
                        },
                        class_name = "rounded-bottom rounded-0",
                    ),
                    active_label_style = {"background-color": "#2A9FD6"},
                    label_style = {
                        "background-color": "#282828",
                        "border": "4px black",
                        "hover": {"background-color": "white"}
                    },
                    tab_id = "tab-importables",
                    label = "Uploading files",
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(inputs),
                        style = {
                            "marginBottom": 0,
                            "paddingBottom": 0,
                        },
                        class_name = "rounded-bottom rounded-0"
                    ),
                    active_label_style = {"background-color": "#2A9FD6"},
                    label_style = {
                        "background-color": "#282828",
                        "border": "4px black",
                    },
                    tab_id = "tab-inputs",
                    label = "Time slot inputs"
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(analysis),
                        style = {
                            "marginBottom": 0,
                            "paddingBottom": 0,
                            "height": "34.5rem"
                        },
                        class_name = "rounded-bottom rounded-0"
                    ),
                    active_label_style = {"background-color": "#2A9FD6"},
                    label_style = {
                        "background-color": "#282828",
                        "border": "4px black",
                    },
                    tab_id = "tab-analysis",
                    label = "Simulation"
                ),
            ],
            id = {"section": "app", "type": "tabs"},
            active_tab = "tab-analysis"                               # remove, just convenient right now
        ),
        
        # For testing callbacks
        html.Div(id = "test", style = {"display": "none"})
    ] + storedImportables + storedInputs,
    fluid = True,   
)

if __name__ == "__main__":
    app.run(debug = True)
