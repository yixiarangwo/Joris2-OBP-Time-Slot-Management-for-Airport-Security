from dash import dcc, html

analysis = [
    html.Button(
        "Run",
        id = {"section": "analysis", "type": "button", "index": "start-simulation"},
    )
]
