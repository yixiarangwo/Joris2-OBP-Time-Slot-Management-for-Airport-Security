﻿import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

# Load the provided CSV file to examine its structure
file_path = 'Data/flights.csv'
flights_data = pd.read_csv(file_path)

passenger_files = [f'Data/passengers_{i}.csv' for i in range(5)]
passengers_data = [pd.read_csv(file) for file in passenger_files]

file_path_security = 'Data/security.csv'
security_data = pd.read_csv(file_path_security)

# Initialize the Dash app with Bootstrap components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


#Globale variabele voor het opslaan van servicetijd
adjusted_service_time = 40

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Flight Dashboard", className="text-center"), className="mb-5 mt-5")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select a Flight Number:"),
            dcc.Dropdown(
                id="flight_dropdown",
                options=[{"label": number, "value": number} for number in flights_data['FlightNumber'].unique()],
                value=flights_data['FlightNumber'].unique()[0],
                clearable=False
            ),
        ], width=6),
        dbc.Col([
            html.Label("Adjust Service Time (Security Efficiency):"),
            dcc.Slider(
                id='service_time_slider',
                min=40,
                max=45,
                step=1,
                value=40,
                marks={i: str(i) for i in range(40, 46)},
            ),
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id="output_div"),  # add output_div
            html.Div(id="time_slot_div")
        ])
    ]),
    html.Div(id="hidden-div", style={'display': 'none'})  # add hidden-div
])




# Callback to update the output div based on the selected flight number
@app.callback(
    Output("output_div", "children"),
    [Input("flight_dropdown", "value")]
)

def update_output(flight_number):
    selected_flight = flights_data[flights_data['FlightNumber'] == flight_number]
    total_seconds = selected_flight['DepartureTime'].iloc[0]
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    departure_time_formatted = f"{int(hours):02d}:{int(minutes):02d}"
    output_string = f"For Flight {flight_number}, departure at {departure_time_formatted} with {selected_flight['Passengers'].iloc[0]} passengers."
    return output_string

# Maak callbacks om te reageren op schuifregelaarveranderingen
@app.callback(
    Output('hidden-div', 'children'), 
    [Input('service_time_slider', 'value')]
)

def update_service_time(value):
    global adjusted_service_time
    adjusted_service_time = value
    return ''  


# Functies om time slots te berekenen
def calculate_time_slots(departure_time):
    # omrekenen naar uren en minuten
    hours = departure_time // 3600
    minutes = (departure_time % 3600) // 60
    departure_datetime = pd.Timestamp.today().replace(hour=hours, minute=minutes, second=0, microsecond=0)

    #Bereken het begin en het einde van de tijdsperiode
    start_time = (departure_datetime - pd.Timedelta(minutes=75)).strftime("%H:%M")
    end_time = (departure_datetime - pd.Timedelta(minutes=15)).strftime("%H:%M")

    # Maak een time slots lijst 
    time_slots = pd.date_range(start=start_time, end=end_time, freq='30T').strftime("%H:%M")
    return time_slots

@app.callback(
    Output("time_slot_div", "children"),
    [Input("flight_dropdown", "value")]
)

#Functies om time slots te geven
def update_time_slots(flight_number):
    selected_flight = flights_data[flights_data['FlightNumber'] == flight_number]
    if selected_flight.empty:
        return ["No data available for selected flight."]
    departure_time = selected_flight['DepartureTime'].iloc[0]
    time_slots = calculate_time_slots(departure_time)

    time_slot_elements = [html.Div(f"Time Slot: {slot} - Average Waiting Time: 0, Service Level: 0, Expected Missed: 0") for slot in time_slots]
    return time_slot_elements

# Main function to run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)