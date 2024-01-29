
from dash import Dash, dcc, html, Input, Output, State, callback, ctx,dash_table
import numpy as np
import json

from analysis.functions import *

from analysis.simulation import *

from analysis.graphs import *




############################################ Analysis tab ############################################


@callback(
    Output('average-waiting-time-output', 'children'),
    Output('average-Virtua-waiting-time-output', 'children'),
    Output('average-Normal-waiting-time-output', 'children'),
    Output('waiting-time-plot-output', 'figure'),
    Output('miss-flight-plot-output', 'figure'),
    Output('service_level_plot-output', 'figure'),    
    Output('service_level_plot_1-output', 'figure'), 
    Output('service_level_plot_0-output', 'figure'), 
    Output({"section": "intermediate", "type": "dataframe", "index": "simulation_results"}, "data",allow_duplicate = True),
    Output({"section": "intermediate", "type": "dataframe", "index": "waiting_time_intervals"}, "data",allow_duplicate = True), 
    Output('miss_fligh_table-container', 'children'),  

    Input('run-simulation-button', 'n_clicks'),
    
    State({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "flights"}, "data"),
    
    prevent_initial_call = True
)
def update_dashboard(n_clicks, passengers_data_json, security_data_json,flights_data_json):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    #input data use function input_data
    passengers_data,security_data = input_data(passengers_data_json,security_data_json,flights_data_json)
   
    #run simulation
    simulation_result_df,waiting_time_intervals =  multiple_run_simulation(5,40000, passengers_data, security_data) 
    simulation_result_df["Time in hour"] = simulation_result_df.index/3600
    
    # Use function calculate_average_waiting_time() to output the str
    average_waiting_time_str = calculate_average_waiting_time_str(simulation_result_df, 'Average Waiting Time')
    average_Virtual_waiting_time_str = calculate_average_waiting_time_str(simulation_result_df, 'Average Virtual Queue Waiting Time')
    average_Normal_waiting_time_str = calculate_average_waiting_time_str(simulation_result_df, 'Average Normal Queue Waiting Time')

    #convert_to_minutes
    simulation_result_df,passengers_data,waiting_time_intervals_minutes = convert_to_minutes(simulation_result_df,passengers_data,waiting_time_intervals)

    #draw plot
    plot_fig = create_time_interval_plot(simulation_result_df)
    plot_fit_miss = create_miss_flight_time_interval_plot(simulation_result_df)
    
    #select miss passengers and make summary
    passengers_data_miss = passengers_data[passengers_data["miss_flight"]==1]
    miss_summary = passengers_data_miss.groupby('FlightNumber').agg(
        MissFlightCount=('miss_flight', 'sum'), 
        DepartureTime=('DepartureTime_formatted', 'first'),  
        AverageWaitingTime=('waitingTime', 'mean'),  
        PriorityCount=('Priority', lambda x: (x == 1).sum()),  
        NormalCount=('Priority', lambda x: (x == 0).sum())  
    ).reset_index()
    miss_summary_dict = miss_summary.to_dict('records')
    
    #use tabel to show summary
    data_table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in miss_summary.columns],
    data=miss_summary_dict,
    style_table={'height': '300px', 'overflowY': 'auto'},
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    page_action="native",
    page_current=0,
    page_size=10,
)
    #save results and will use it for each time interval analysis
    simulation_results_json = simulation_result_df.to_json(date_format='iso', orient='split')
    waiting_time_intervals_minutes_json = json.dumps(waiting_time_intervals_minutes)
    
    plot_service_level =create_service_level_plot(passengers_data)
    plot_service_level_1 = create_service_level_priority_plot(passengers_data,1)
    plot_service_level_0 = create_service_level_priority_plot(passengers_data,0)

    return (
    average_waiting_time_str,
    average_Virtual_waiting_time_str,
    average_Normal_waiting_time_str,
    plot_fig,
    plot_fit_miss,
    plot_service_level,
    plot_service_level_1,
    plot_service_level_0,
    simulation_results_json,
    waiting_time_intervals_minutes_json,
    data_table
)


@callback(
    Output('time_interval-output', 'children'),
    Output('time_interval-plot', 'figure'),
    Input('run-interval-button', 'n_clicks'),
    State({"section": "intermediate", "type": "dataframe", "index": "simulation_results"},"data"),
    State({"section": "analysis", "type": "dropdown", "index": "data_type_selection"},'value'),
    State({"section": "analysis", "type": "slider", "index": "time_selection"}, 'value'),
    State({"section": "intermediate", "type": "dataframe", "index": "waiting_time_intervals"},"data"),
    prevent_initial_call=True
)
def select_time_interval_update(n_clicks,simulation_results,data_type_selection,time_selection,waiting_time_intervals):
    #input
    simulation_results_parsed = json.loads(simulation_results)
    simulation_results_df = pd.DataFrame(**simulation_results_parsed)
    #str show average waiting
    waiting_in_interval_minutes = get_time_at_index(simulation_results_df,data_type_selection,time_selection)
    waiting_in_interval_str = format_time_interval_message(data_type_selection, waiting_in_interval_minutes)
    
    #plot
    waiting_time_intervals_minutes = json.loads(waiting_time_intervals)
    waiting_time_intervals_minutes_tuples = [tuple(interval) for interval in waiting_time_intervals_minutes]
    waiting_in_interval_fig = select_waitingTime_interval(waiting_time_intervals_minutes_tuples,time_selection)
    
    return waiting_in_interval_str ,waiting_in_interval_fig
    