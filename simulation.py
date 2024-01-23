# Metropolis Hastings algorithm for sampling from random function
# Otherwise, rejection sampling is another possibility
import simpy
import numpy as np
import random
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output, callback

virtual_queue = [
    {"flights": "BM2616", "time_slots": [4*3600], "capacity":[30]}, #Depature 05:45
    {"flights": "XC6333", "time_slots": [5.25*3600, 5.5*3600, 5.75*3600],"capacity":[20,20,5]}, #Depature 06:00
    {"flights": "OO2037", "time_slots": [5.5*3600, 5.75*3600, 6*3600], "capacity":[20,20,5]}, #Depature 06:15
    {"flights": "HP4524", "time_slots": [5.5*3600, 5.75*3600, 6*3600, 6.25*3600],"capacity":[10,20,5,10]}, #Depature 06:30
    {"flights": "DN7022", "time_slots": [6.5*3600, 6.25*3600, 6*3600],"capacity":[30,20,10]}, #Depature 06:45

    {"flights": "QX7315", "time_slots": [7*3600], "capacity":[20]}, #Depature 09:30
    {"flights": "SS2446", "time_slots": [9.25*3600, 9.5*3600], "capacity":[20, 20]}, #Depature 09:45
    {"flights": "ZI1701", "time_slots": [9.75*3600, 9.5*3600], "capacity":[20, 20]}, #Depature 10:00
    {"flights": "HC1255", "time_slots": [10*3600, 9.75*3600, 9.5*3600], "capacity":[20,20, 20]}, #Depature 10:15
    {"flights": "HF1818", "time_slots": [10.25*3600, 10*3600, ], "capacity":[20, 20]}, #Depature 10:30
    {"flights": "IG2596", "time_slots": [10.5*3600], "capacity":[40]} #Depature 10:45
]

def process_virtual_queue(passengers_data, virtual_queue):
    #Peak period 1: 04:15 - 05:15
    peak_periods1_start = 4.25*60*60
    peak_periods1_end = 5.25*60*60

    #Peak period 2: 07:30 - 09:00
    peak_periods2_start = 7.5*60*60
    peak_periods2_end = 9*60*60

    passengers_data["new_ArrivalTime"] = passengers_data["ArrivalTime"]
    passengers_data['Priority'] = 0
    
    # Iterate over the virtual queue list
    for flight_info in virtual_queue:
        flight_code = flight_info["flights"]
        time_slots = flight_info["time_slots"]
        capacities = flight_info["capacity"]

        # Get eligible passengers
        eligible_passengers = passengers_data[((passengers_data['ArrivalTime'].between(peak_periods1_start, peak_periods1_end)) | 
                                           (passengers_data['ArrivalTime'].between(peak_periods2_start, peak_periods2_end))) & 
                                           (passengers_data['FlightNumber'] == flight_code)]

        # Passengers randomly selected and assigned to time slots
        for i, passenger in eligible_passengers.iterrows():
            # If all the time slots are used up,jump out of the loop here
            if not time_slots:
                break

            time_slot = random.choice(time_slots)
            capacity = capacities[time_slots.index(time_slot)]

            # Check if time slot capacity is exhausted
            if capacity == 0:
                continue

            # Generate random arrival times between time_slot and time_slot + 15 minutes
            random_arrival_time = random.uniform(time_slot, time_slot + 0.25 * 3600)

           # Process accordingly, e.g. update arrival times, set priorities, etc.
            passengers_data.loc[i, 'new_ArrivalTime'] = random_arrival_time
            passengers_data.loc[i, 'Priority'] = 1  

            
            capacities[time_slots.index(time_slot)] -= 1

            # If a time slot runs out of capacity,  remove that time slot here
            if capacities[time_slots.index(time_slot)] == 0:
                time_slots.remove(time_slot)
                
    passengers_data["new_ArrivalTime_formatted"] = passengers_data["new_ArrivalTime"].apply(lambda x: (datetime(1970, 1, 1) + timedelta(seconds=x)).strftime('%H:%M'))
    passengers_data["DepartureTime_formatted"] = passengers_data["DepartureTime"].apply(lambda x: (datetime(1970, 1, 1) + timedelta(seconds=x)).strftime('%H:%M'))

    return passengers_data


waiting_time_list = []
virtual_waiting_time_list = []
normal_waiting_time_list = []
waiting_time_intervals = []
average_waiting_times = []
time_intervals_start = []
average_virtual_waiting_times = []
average_normal_waiting_times = []
virtual_queue_empty = True
time_interval = 15 * 60
MAX_WAIT_TIME = 10 * 60

def generate_processing_time():
    return random.expovariate(1 / 20.0)

def security_check(env, passenger_id, security_lanes, priority):
    global waiting_time_list, virtual_waiting_time_list, normal_waiting_time_list, waiting_time_intervals

    arrival_time = env.now

    if priority == 0:
        # Wait until the queue is empty or the maximum wait time is reached
        start_wait_time = env.now
        while len(security_lanes[0].queue) > 0 and (env.now - start_wait_time) < MAX_WAIT_TIME:
            yield env.timeout(1)  # Check the queue again after a short wait

    shortest_lane = min(security_lanes, key=lambda x: len(x.queue))
    with shortest_lane.request() as request:
        yield request
        yield env.timeout(generate_processing_time())
        waiting_time = env.now - arrival_time
        waiting_time_list.append(waiting_time)
        if priority == 1:
            virtual_waiting_time_list.append(waiting_time)
        else:
            normal_waiting_time_list.append(waiting_time)
        waiting_time_intervals[-1].append(waiting_time)
        print(f"Passenger {passenger_id} arrived at {arrival_time}, priority: {priority}")
        print(f"Passenger {passenger_id} completed security check on {env.now} (wait time: {waiting_time} seconds)")



def passenger_generator(env, security_lanes, passengers_data):
    for _, passenger in passengers_data.iterrows():
        passenger_id = passenger['Id']
        priority = passenger['Priority']
        arrival_time = passenger['new_ArrivalTime']
        yield env.timeout(max(0, arrival_time - env.now))
        env.process(security_check(env, passenger_id, security_lanes, priority))

def adjust_security_lanes(env, security_lanes, security_data):
    for _, row in security_data.iterrows():
        time, lanes = row['Time'], row['Lanes']
        yield env.timeout(time - env.now)
        while len(security_lanes) < lanes:
            security_lanes.append(simpy.Resource(env, capacity=1))
        while len(security_lanes) > lanes:
            security_lanes.pop()

def calculate_average_waiting_time(env):
    global time_intervals_start, average_waiting_times
    global average_virtual_waiting_times, average_normal_waiting_times
    current_time = 0
    while True:
        yield env.timeout(time_interval)
        current_time += time_interval

        # Calculate overall average wait time
        if waiting_time_intervals[-1]:
            avg_waiting_time = sum(waiting_time_intervals[-1]) / len(waiting_time_intervals[-1])
        else:
            avg_waiting_time = 0
        average_waiting_times.append(avg_waiting_time)

        # Calculate the average wait time for virtual queues
        if virtual_waiting_time_list:
            avg_virtual_waiting_time = sum(virtual_waiting_time_list) / len(virtual_waiting_time_list)
        else:
            avg_virtual_waiting_time = 0
        average_virtual_waiting_times.append(avg_virtual_waiting_time)

        # Calculate the average wait time for a normal queue
        if normal_waiting_time_list:
            avg_normal_waiting_time = sum(normal_waiting_time_list) / len(normal_waiting_time_list)
        else:
            avg_normal_waiting_time = 0
        average_normal_waiting_times.append(avg_normal_waiting_time)

        # Prepare for the next interval
        time_intervals_start.append(current_time - time_interval)
        waiting_time_intervals.append([])
        virtual_waiting_time_list.clear()
        normal_waiting_time_list.clear()

def reset_globals():
    global waiting_time_list, virtual_waiting_time_list, normal_waiting_time_list
    global waiting_time_intervals, average_waiting_times, time_intervals_start
    global average_virtual_waiting_times, average_normal_waiting_times, virtual_queue_empty
    
    waiting_time_list = []
    virtual_waiting_time_list = []
    normal_waiting_time_list = []
    waiting_time_intervals = [[]]
    average_waiting_times = []
    average_virtual_waiting_times = []
    average_normal_waiting_times = []
    time_intervals_start = []
    virtual_queue_empty = True

def run_simulation(sim_time, passengers_data, security_data):
    reset_globals()

    env = simpy.Environment()
    initial_lanes = security_data['Lanes'].iloc[0]
    security_lanes = [simpy.Resource(env, capacity=1) for _ in range(initial_lanes)]
    
    waiting_time_intervals.append([])

    env.process(passenger_generator(env, security_lanes, passengers_data))
    env.process(adjust_security_lanes(env, security_lanes, security_data))
    env.process(calculate_average_waiting_time(env))

    env.run(until=sim_time)
    df_avg_waiting_times = pd.DataFrame({
        'Average Waiting Time': average_waiting_times,
        'Average Virtual Queue Waiting Time': average_virtual_waiting_times,
        'Average Normal Queue Waiting Time': average_normal_waiting_times
    }, index=time_intervals_start)
    return df_avg_waiting_times

def multiple_run_simulation(runs, sim_time, passengers_data, security_data):
    total_avg_waiting_times = None
    for i in range(runs):
        print(f"Running simulation {i+1}/{runs}")
        average_waiting_time_df = run_simulation(sim_time, passengers_data, security_data)
        if total_avg_waiting_times is None:
            total_avg_waiting_times = average_waiting_time_df
        else:
            total_avg_waiting_times = total_avg_waiting_times.add(average_waiting_time_df, fill_value=0)

    overall_average = total_avg_waiting_times / runs
    return overall_average


