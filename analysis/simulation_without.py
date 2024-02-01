import simpy
import numpy as np
import random
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output, callback

waiting_time_list_without = []
waiting_passengers_without = 0
time_interval_without = 15 * 60
waiting_time_intervals_without = []
average_waiting_times_without = []
time_intervals_start_without = []

from analysis.functions import *

def generate_processing_time_without():
    return random.expovariate(1 / 20.0)

def security_check_without(env, passenger_id, security_lanes):
    global waiting_passengers_without, waiting_time_intervals_without

    arrival_time = env.now
    waiting_passengers_without += 1

    shortest_lane = min(security_lanes, key=lambda x: len(x.queue))
    with shortest_lane.request() as request:
        yield request
        processing_start = env.now
        yield env.timeout(generate_processing_time_without())
        waiting_time = env.now - arrival_time
        waiting_time_list_without.append(waiting_time)
        waiting_passengers_without -= 1
        waiting_time_intervals_without[-1].append(waiting_time)

def passenger_generator_without(env, security_lanes, passengers_data):
    for _, passenger in passengers_data.iterrows():
        passenger_id = passenger['Id']
        arrival_time = passenger['ArrivalTime']
        yield env.timeout(arrival_time - env.now)
        env.process(security_check_without(env, passenger_id, security_lanes))

def adjust_security_lanes(env, security_lanes, security_data):
    for _, row in security_data.iterrows():
        time, lanes = row['Time'], row['Lanes']
        yield env.timeout(time - env.now)
        while len(security_lanes) < lanes:
            security_lanes.append(simpy.Resource(env, capacity=1))
        while len(security_lanes) > lanes:
            security_lanes.pop()

def calculate_average_waiting_time_without(env):
    global time_intervals_start_without
    current_time = 0
    while True:
        yield env.timeout(time_interval_without)
        current_time += time_interval_without
        if waiting_time_intervals_without[-1]:
            avg_waiting_time = sum(waiting_time_intervals_without[-1]) / len(waiting_time_intervals_without[-1])
            average_waiting_times_without.append(avg_waiting_time)
        else:
            average_waiting_times_without.append(0)
        time_intervals_start_without.append(current_time - time_interval_without)
        waiting_time_intervals_without.append([])
        
def reset_globals_without():
    global waiting_time_list_without, waiting_passengers_without, waiting_time_intervals_without, average_waiting_times_without, time_intervals_start_without
    waiting_time_list_without = []
    waiting_passengers_without = 0
    waiting_time_intervals_without = [[]]
    average_waiting_times_without = []
    time_intervals_start_without = []
    
def run_simulation_without(sim_time, passengers_data, security_data):
    reset_globals_without()

    env = simpy.Environment()
    initial_lanes = security_data['Lanes'].iloc[0]
    security_lanes = [simpy.Resource(env, capacity=1) for _ in range(initial_lanes)]
    waiting_time_intervals_without.append([])

    env.process(passenger_generator_without(env, security_lanes, passengers_data))
    env.process(adjust_security_lanes(env, security_lanes, security_data))
    env.process(calculate_average_waiting_time_without(env))
    
    env.run(until=sim_time)
    df_avg_waiting_times = pd.DataFrame({'Average Waiting Time': average_waiting_times_without}, index=time_intervals_start_without)
    return df_avg_waiting_times

def multiple_run_simulation_without(runs, sim_time, passengers_data, security_data):
    total_avg_waiting_times_without = None
    for i in range(runs):
        average_waiting_time_df = run_simulation_without(sim_time, passengers_data, security_data)
        if total_avg_waiting_times_without is None:
            total_avg_waiting_times_without = average_waiting_time_df
        else:
            total_avg_waiting_times_without = total_avg_waiting_times_without.add(average_waiting_time_df, fill_value=0)

    overall_average = total_avg_waiting_times_without / runs
    return overall_average
