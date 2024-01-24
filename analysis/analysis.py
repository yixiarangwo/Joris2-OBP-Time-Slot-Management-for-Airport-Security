from dash import Dash, dcc, html

analysis = [
            dcc.Graph(id='arrival-time-distribution-plot'),
            html.Button('Run Simulation without time slot', id='run-simulation-without-button'),
            html.Div(id='average-waiting-without-time-output'),
            dcc.Graph(id='waiting-time-without-plot-output'),
            html.Button('Run Simulation', id='run-simulation-button'),
            html.Div(id='average-waiting-time-output'),
            html.Div(id='average-Virtua-waiting-time-output'),
            html.Div(id='average-Normal-waiting-time-output'),
            dcc.Graph(id='waiting-time-plot-output')
        ]
