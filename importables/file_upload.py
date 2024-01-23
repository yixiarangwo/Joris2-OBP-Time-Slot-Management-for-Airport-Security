from dash import dcc, html

fileUpload = [
    ### Importing files
    html.Div([
        html.H3("Import files"),
        
        # Arrival data input
        html.Label("Arrival data:"),
        dcc.Upload(
            id = { "section": "importables", "type": "upload", "index": "arrivals" },
            children = [
                "Drag and Drop or ",
                html.A("Select a File")
            ],
            style = {
                "width": "300px",
                "height": "40px",
                "lineHeight": "40px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px"
            },
            multiple = True
        ),
        
        # Flight schedule input
        html.Label("Flight schedule:"),
        dcc.Upload(
            id = { "section": "importables", "type": "upload", "index": "flights" },
            children = html.Div([
                "Drag and Drop or ",
                html.A("Select a File")
            ]),
            style = {
                "width": "300px",
                "height": "40px",
                "lineHeight": "40px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px"
            },
            multiple = False
        ),
        
        # Security lane availability input
        html.Label("Security lane availability:"),
        dcc.Upload(
            id = {"section": "importables", "type": "upload", "index": "lanes"},
            children = html.Div([
                "Drag and Drop or ",
                html.A("Select a File")
            ]),
            style = {
                "width": "300px",
                "height": "40px",
                "lineHeight": "40px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px"
            },
            multiple = False
        )
    ], style = {"float": "left", "margin": "auto", "marginLeft": "10%", "marginRight": "10%"}),
]
