from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def cardUploadComponent(id):
    return dbc.CardGroup([
        dbc.Card(
            # Upload arrival data
            dcc.Upload(
                children = [
                    "Drag and Drop or ",
                    html.A("Select a File"),
                ],
                id = id,
                style = {"textAlign": "right", "color": "black"},
                multiple = False
            ),
            body = True,
            class_name = "justify-content-center border-0",
            style = {"height": "2.25rem"},
            color = "dark",
        ),
        
        dbc.Card(
            html.I(
                DashIconify(icon = "ion:push-outline", width = 25),
                id = {"section": id["section"], "type": "icon", "index": id["index"]},
                style = {"text-align": "left", "color": "black"},
            ),
            body = True,
            class_name = "justify-content-center border-0",
            style = {
                "height" : "2.25rem",
                "maxWidth": "20%",
            },
            color = "dark"
        )
    ], style = {"width": "21rem"})


fileUpload = [
    dbc.Row([
        html.H4(
            "Import files",
            className = "card-title",
            style = {"marginBottom": "-0.5rem"}
        ),
        
        # Arrival data input
        dbc.Card(
            children = [
                dbc.Row([
                    html.Label(
                        "Arrival data:",
                        className = "card-title"
                    ),
                    cardUploadComponent({ "section": "importables", "type": "upload", "index": "arrivals" })
                ], justify = "center")
            ],
            color = "secondary",
            style = {
                "width": "93%",
                "paddingBottom": "1rem",
                "paddingTop": "0.5rem",
                "margin": "1rem"
            }
        ),
    ], justify = "center"),

    
    # Flight schedule input
    dbc.Row([
        dbc.Card(
            children = [
                dbc.Row([
                    html.Label(
                        "Flight schedule:",
                        className = "card-title"
                    ),
                    cardUploadComponent({"section": "importables", "type": "upload", "index": "flights"})
                ], justify = "center")
            ],
            color = "secondary",
            style = {
                "width": "93%",
                "paddingBottom": "1rem",
                "paddingTop": "0.5rem",
                "margin": "1rem"
            }
        ),
    ], justify = "center"),
    
    # Arrival data input
    dbc.Row([
        dbc.Card(
            children = [
                dbc.Row([
                    html.Label(
                        "Security lane availability:",
                        className = "card-title",
                    ),
                    cardUploadComponent({"section": "importables", "type": "upload", "index": "lanes"})
                ], justify = "center")
            ],
            color = "secondary",
            style = {
                "width": "93%",
                "paddingBottom": "1rem",
                "paddingTop": "0.5rem",
                "margin": "1rem"
            }
        ),
    ], justify = "center"),

    # Alert when uploading has gone wrong
    dbc.Row([
        dbc.Alert(
            html.Div(
                "",
                id = {"section": "importables", "type": "text", "index": "file-check"},
                style = {
                    "text-align": "center",
                    "color": "black",
                },
            ),
            id = {"section": "importables", "type": "alert", "index": "file-check"},
            style = {
                "width": "93%",
                "marginTop": "1rem",
                "marginBottom": 0,
                "border":"2px black solid",
            },
            className = "fw-bold d-flex align-items-center justify-content-center border-2",
            color = "danger",
            is_open = False,
            fade = True
        ),
    ], justify = "center"),
]
