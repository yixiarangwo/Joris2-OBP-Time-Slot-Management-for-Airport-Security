from dash import Dash, dcc, html, Input, Output, callback, dash_table

# Importables on importable tab
importables = [
    ### Importing files
    html.Div([
        html.H3("Import files"),
        
        # Arrival data input
        html.Label("Arrival data:"),
        dcc.Upload(
            id = { "section": "importables", "type": "upload", "index": "arrivals" },
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

    ### Service time distribution
    html.Div([
        # Latex input
        html.H3("Server distribution"),
        html.Label("Give server distribution in terms of x", style = {"marginRight": "16%"}),
        html.Label("Lower bound", style = {"marginRight": "2%"}),
        html.Label("Upper bound"),
        html.Br(),
        dcc.Textarea(
            id = {"section": "importables", "type": "input", "index": "server-dist", "info": "formula"},
            placeholder = "Enter service distribution in LaTeX format here",
            style = {"width": "60%", "height": "20%", "marginRight": "2%"},
            value = ''
        ),

        # Input for upper and lower limit of function, , ADD LOWER AND UPPER LIMIT OF DISTRIBUTION
        dcc.Input(
            id = {"section": "importables", "type": "input", "index": "server-dist", "info": "lower-bound"},
            style = {"width": "15%", "vertical-align": "85%", "marginRight": "2%"},
            type = "text"
        ),
        dcc.Input(
            id = {"section": "importables", "type": "input", "index": "server-dist", "info": "upper-bound"},
            style = {"width": "15%", "vertical-align": "85%"},
            type = "text"
        ),
        
        # Show function from LaTeX
        html.Br(),
        dcc.Markdown(
            id = {"section": "importables", "type": "text", "index": "server-dist"},
            children = [], mathjax = True, style = {"font-size": "125%"}
        ),
        
        # Submit button
        html.Button(
            "Submit distribution",
            id = {"section": "importables", "type": "button", "index": "server-dist"},
            n_clicks = 0
        ),

        # Show graph of sampled service times
        #dcc.Graph(id = {"section": "importables", "type": "graph", "index": "sim-service"})
        
    ], style = {"float": "left", "margin": "auto", "marginLeft": "0%", "marginRight": "0%"})
]


# Time slot and capacity inputs on input tab
inputs = [
    # Submit button
    html.Button(
        "Submit time slots", 
        id = {"section": "inputs", "type": "button", "index": "time-slots"},
        style = {"margin": "2%"}
    ),

    # Flight info and time slot input displayed in rows
    dash_table.DataTable(
        id = {"section": "inputs", "type": "table", "index": "time-slots"},
        columns = [
            {"name": "Flight Number",       "id": "FlightNumber",      "editable": False},
            {"name": "Departure Time",      "id": "DepartureTime",     "editable": False},
            {"name": "Passengers",          "id": "Passengers",        "editable": False},
            {"name": "Time Slot Capacity",  "id": "TimeSlotCapacity",  "editable": True},
            {"name": "Time Slot Intervals", "id": "TimeSlotIntervals", "editable": True}
        ],
        data = [
            {"FlightNumber": "", "DepartureTime": "", "Passengers": "",
             "TimeSlotCapacity": "", "TimeSlotIntervals": ""}
        ],
        editable = False,  # Editable once the data has been uploaded
        style_cell = {"textAlign": "center"},
        style_cell_conditional = [
            {"if": {"column_id": "FlightNumber"},  "width": "5%"},
            {"if": {"column_id": "DepartureTime"}, "width": "5%"},
            {"if": {"column_id": "Passengers"},    "width": "2%"},
            {"if": {"column_id": "TimeSlotCapacity"},    "width": "4%"}
        ],
        style_table = {"width": "80%", "marginLeft": "10%"}
    )
]
