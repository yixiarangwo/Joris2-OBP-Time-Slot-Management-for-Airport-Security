import plotly.graph_objs as go
import numpy as np
from analysis.simulation import *



def input_data(passengers_data_json,security_data_json,flights_data_json):
    passengers_data = pd.DataFrame(passengers_data_json)
    security_data = pd.DataFrame(security_data_json)
    flights_data =pd.DataFrame(flights_data_json)
    passengers_data = pd.merge(passengers_data, flights_data, left_on='FlightNumber', right_on='FlightNumber', how='left')
    passengers_data = process_virtual_queue(passengers_data, virtual_queue).sort_values(by='new_ArrivalTime')
    return passengers_data,security_data

def calculate_average_waiting_time_str(simulation_result_df, column_name):
    non_zero_values = simulation_result_df[simulation_result_df[column_name] != 0]
    non_zero_count = non_zero_values[column_name].count()
    if non_zero_count == 0:
        return f"Average {column_name}: No data available"

    average_waiting_time = non_zero_values[column_name].sum() / non_zero_count
    average_waiting_time_minutes = average_waiting_time // 60
    average_waiting_time_seconds = average_waiting_time % 60
    return f"Average {column_name}: {int(average_waiting_time_minutes)} minutes and {average_waiting_time_seconds:.2f} seconds"

def  convert_to_minutes(simulation_result_df,passengers_data,waiting_time_intervals):    
    simulation_result_df['Average Waiting Time'] = simulation_result_df['Average Waiting Time']/60
    simulation_result_df['Average Virtual Queue Waiting Time'] = simulation_result_df['Average Virtual Queue Waiting Time']/60
    simulation_result_df['Average Normal Queue Waiting Time'] = simulation_result_df['Average Normal Queue Waiting Time']/60
    passengers_data["waitingTime"]=passengers_data["waitingTime"]/60
    waiting_time_intervals_minutes = [[time / 60 for time in interval] for interval in waiting_time_intervals]
    return simulation_result_df,passengers_data,waiting_time_intervals_minutes


def get_time_at_index(simulation_result_df, column_name, time_point):
    return simulation_result_df.loc[time_point, column_name]

def format_time_interval_message(data_type, time_value):
    if data_type not in ["Average Waiting Time", "Average Virtual Queue Waiting Time", "Average Normal Queue Waiting Time"]:
        return "Invalid data type selected."

    return f"{data_type} in this interval: {time_value} minutes."