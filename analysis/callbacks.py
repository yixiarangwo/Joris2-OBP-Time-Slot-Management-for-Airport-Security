from dash import Dash, dcc, html, Input, Output, State, callback, ctx,dash_table
import numpy as np

from analysis.functions import *

from analysis.simulation import *

from analysis.simulation_without import *




############################################ Analysis tab ############################################
@callback(
    Output('average-waiting-time-output', 'children'),
    Output('average-Virtua-waiting-time-output', 'children'),
    Output('average-Normal-waiting-time-output', 'children'),
    Output('waiting-time-plot-output', 'figure'),
    Input('run-simulation-button', 'n_clicks'),
    State({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "flights"}, "data"),
    prevent_initial_call = True
)
def update_dashboard(n_clicks, passengers_data_json, security_data_json,flights_data_json):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    
    passengers_data = pd.DataFrame(passengers_data_json)
    security_data = pd.DataFrame(security_data_json)
    flights_data =pd.DataFrame(flights_data_json)
    passengers_data = pd.merge(passengers_data, flights_data, left_on='FlightNumber', right_on='FlightNumber', how='left')
    passengers_data = process_virtual_queue(passengers_data, virtual_queue).sort_values(by='new_ArrivalTime')
    
    #run simulation
    simulation_result_df = multiple_run_simulation(5,40000, passengers_data, security_data)
    print(simulation_result_df)
    simulation_result_df["Time in hour"] = simulation_result_df.index/3600
    non_zero_values = simulation_result_df[simulation_result_df['Average Waiting Time'] != 0]
    non_zero_count = non_zero_values['Average Waiting Time'].count()
    average_waiting_time = non_zero_values['Average Waiting Time'].sum() / non_zero_count
    average_waiting_time_minutes = average_waiting_time // 60
    average_waiting_time_seconds = average_waiting_time % 60
    average_waiting_time_str = f"Average Waiting Time: {int(average_waiting_time_minutes)} minutes and {average_waiting_time_seconds:.2f} seconds"
    
    non_zero_values_Virtual = simulation_result_df[simulation_result_df['Average Virtual Queue Waiting Time'] != 0]
    non_zero_count_Virtual = non_zero_values['Average Virtual Queue Waiting Time'].count()
    average_Virtual_waiting_time= simulation_result_df['Average Virtual Queue Waiting Time'].sum()/non_zero_count
    average_Virtual_waiting_time_minutes = average_Virtual_waiting_time // 60
    average_Virtual_waiting_time_seconds = average_Virtual_waiting_time % 60
    average_Virtual_waiting_time_str = f"Average Virtual Waiting Time: {int(average_Virtual_waiting_time_minutes)} minutes and {average_Virtual_waiting_time_seconds:.2f} seconds"
    
    non_zero_values_Normal = simulation_result_df[simulation_result_df['Average Normal Queue Waiting Time'] != 0]
    non_zero_count_Normal = non_zero_values['Average Normal Queue Waiting Time'].count()
    average_Normal_waiting_time=simulation_result_df['Average Normal Queue Waiting Time'].sum()/non_zero_count
    average_Normal_waiting_time_minutes = average_Normal_waiting_time // 60
    average_Normal_waiting_time_seconds = average_Normal_waiting_time % 60
    average_Normal_waiting_time_str = f"Average Normal Waiting Time: {int(average_Normal_waiting_time_minutes)} minutes and {average_Normal_waiting_time_seconds:.2f} seconds"
    
    plot_fig = create_time_interval_plot(simulation_result_df)

    return average_waiting_time_str,average_Virtual_waiting_time_str,average_Normal_waiting_time_str,plot_fig


@callback(
    Output('arrival-time-distribution-plot', 'figure'),
    Input({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    prevent_initial_call=True
)
def update_arrival_time_plot(arrival_data):
    try:
        if not arrival_data:
            return {}

        arrival_df = pd.DataFrame(arrival_data)
        
        fig = create_plotly_histogram(arrival_df)
        return fig
    except Exception as e:
        print(f"Error in update_arrival_time_plot: {e}")
        return {}
    
@callback(
    Output('average-waiting-without-time-output', 'children'),
    Output('waiting-time-without-plot-output', 'figure'),
    Input('run-simulation-without-button', 'n_clicks'),
    State({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    prevent_initial_call = True
)
def update_dashboard_without(n_clicks, passengers_data_json, security_data_json):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    
    passengers_data = pd.DataFrame(passengers_data_json).sort_values(by='ArrivalTime')
    security_data = pd.DataFrame(security_data_json)

    #run simulation
    simulation_result_without_df = multiple_run_simulation_without(5,40000, passengers_data, security_data)
    print(simulation_result_without_df)
    simulation_result_without_df["Time in hour"] = simulation_result_without_df.index/3600
    non_zero_values_without = simulation_result_without_df[simulation_result_without_df['Average Waiting Time'] != 0]
    non_zero_count_without = non_zero_values_without['Average Waiting Time'].count()
    average_waiting_time_without = non_zero_values_without['Average Waiting Time'].sum() / non_zero_count_without
    average_waiting_time_without_minutes = average_waiting_time_without // 60
    average_waiting_time_without_seconds = average_waiting_time_without % 60
    average_waiting_time_without_str = f"Average Normal Waiting Time: {int(average_waiting_time_without_minutes)} minutes and {average_waiting_time_without_seconds:.2f} seconds"
    plot_fig_without = create_time_interval_without_plot(simulation_result_without_df)

    return average_waiting_time_without_str,plot_fig_without
