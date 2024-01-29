from dash import Dash, dcc, html



time_marks = {i * 3600: {'label': f'{i:02d}:00'} for i in range(0, 13)}
for hour in range(0, 13):
    for minute in [15, 30, 45]:
        time_value = hour * 3600 + minute * 60
        time_marks[time_value] = {'label': f'{hour:02d}:{minute:02d}'}

time_slider = html.Div(
    children=[
        html.H3("Select Time Interval", style={"marginBottom": "1em"}),
        dcc.Slider(
            id={"section": "analysis", "type": "slider", "index": "time_selection"},
            min=2*3600 + 15*60,
            max=10 * 3600 + 45 * 60,
            step=15 * 60, 
            marks=time_marks,
            value=0, 
        ),
    ],
    style={"width": "75%", "padding": "20px"}
)

data_column_options = [
    {'label': 'Average Waiting Time', 'value': 'Average Waiting Time'},
    {'label': 'Average Virtual Queue Waiting Time', 'value': 'Average Virtual Queue Waiting Time'},
    {'label': 'Average Normal Queue Waiting Time', 'value': 'Average Normal Queue Waiting Time'}
]

data_type_dropdown = html.Div(
    children=[
        html.H3("Select Data Type", style={"marginBottom": "1em", "marginTop": "1em"}),
        dcc.Dropdown(
            id={"section": "analysis", "type": "dropdown", "index": "data_type_selection"},
            options=data_column_options,
            searchable=False,
            placeholder="Select data type",
            style={"width": "50%", "text-align": "left"},
            value=""
        ),
    ],
    style={"width": "75%", "padding": "20px"}
)

timeDataSelectionFeature = html.Div(
    children=[time_slider, data_type_dropdown],
    style={"padding": "2%"}
)


analysis = [
    html.Button('Run Simulation', id='run-simulation-button'),
    html.Div(id='average-waiting-time-output'),
    html.Div(id='average-Virtua-waiting-time-output'),
    html.Div(id='average-Normal-waiting-time-output'),
    dcc.Graph(id='waiting-time-plot-output'),
    dcc.Graph(id='miss-flight-plot-output'),
    html.Div(id='miss_fligh_table-container'),
    
    dcc.Graph(id='service_level_plot-output'),
    dcc.Graph(id='service_level_plot_1-output'),
    dcc.Graph(id='service_level_plot_0-output'),
    dcc.Store(id={"section": "intermediate", "type": "dataframe", "index": "simulation_results"}, storage_type="session"),
    dcc.Store(id={"section": "intermediate", "type": "dataframe", "index": "waiting_time_intervals"}, storage_type="session"),
    
    html.Button('Check each time interval', id='run-interval-button'),
    dcc.Graph(id='time_interval-plot'),
    timeDataSelectionFeature,
    html.Div(id='time_interval-output')
    
]

