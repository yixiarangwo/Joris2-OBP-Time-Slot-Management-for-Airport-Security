import dash_bootstrap_components as dbc

from importables.file_upload import fileUpload
from importables.service_input import serviceInput

# Combine importables tab components
importables = [
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(fileUpload),
                style = {"border": "none"}
            ), 
            width = 4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    serviceInput, 
                    style = {"paddingLeft": "1vw"}
                ),
                style = {"border": "none"}
            ), 
        width = 8)
    ], justify = "center")
]
