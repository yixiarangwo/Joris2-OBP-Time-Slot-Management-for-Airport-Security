import simpy
import numpy as np
import random
import copy
from datetime import datetime, timedelta
import pandas as pd


from analysis.functions import *


def process_virtual_queue(passengers_data, virtual_queue, duration):
    #Peak period 1: 04:15 - 05:15
    peak_periods1_start = 4.25*60*60
    peak_periods1_end = 5.25*60*60

    #Peak period 2: 07:30 - 09:00
    peak_periods2_start = 7.5*60*60
    peak_periods2_end = 9*60*60

    passengers_data["new_ArrivalTime"] = passengers_data["ArrivalTime"]
    passengers_data['Priority'] = 0

    # Iterate over the virtual queue list
    for flight_code in virtual_queue:
        time_slots = virtual_queue[flight_code]["start"]
        capacities = virtual_queue[flight_code]["capacity"]

        # Get eligible passengers
        eligible_passengers = passengers_data[((passengers_data['ArrivalTime'].between(peak_periods1_start, peak_periods1_end)) | 
                                           (passengers_data['ArrivalTime'].between(peak_periods2_start, peak_periods2_end))) & 
                                           (passengers_data['FlightNumber'] == flight_code)]

        # Passengers randomly selected and assigned to time slots
        for i, passenger in eligible_passengers.iterrows():
            # If all the time slots are used up,jump out of the loop here
            if not time_slots:
                break

            choiceIdx = random.choice(range(len(time_slots)))
            time_slot = time_slots[choiceIdx]
            capacity = capacities[choiceIdx]

            # Generate random arrival times between time_slot and time_slot + duration of time slots
            random_arrival_time = random.uniform(time_slot, time_slot + duration)

           # Process accordingly, e.g. update arrival times, set priorities, etc.
            passengers_data.loc[i, 'new_ArrivalTime'] = random_arrival_time
            passengers_data.loc[i, 'Priority'] = 1  

            
            capacities[choiceIdx] -= 1

            # If a time slot runs out of capacity,  remove that time slot here
            if capacities[choiceIdx] == 0:
                del time_slots[choiceIdx]
                del capacities[choiceIdx]
                
    passengers_data["new_ArrivalTime_formatted"] = passengers_data["new_ArrivalTime"].apply(lambda x: (datetime(1970, 1, 1) + timedelta(seconds=x)).strftime('%H:%M'))
    passengers_data["DepartureTime_formatted"] = passengers_data["DepartureTime"].apply(lambda x: (datetime(1970, 1, 1) + timedelta(seconds=x)).strftime('%H:%M'))

    return passengers_data


def input_data(passengers_data_json,security_data_json,flights_data_json):
    passengers_data = pd.DataFrame(passengers_data_json)
    security_data = pd.DataFrame(security_data_json)
    flights_data =pd.DataFrame(flights_data_json)
    passengers_data = pd.merge(passengers_data, flights_data, left_on='FlightNumber', right_on='FlightNumber', how='left')
    return passengers_data,security_data


global time_interval 
time_interval= 15 * 60
global MAX_WAIT_TIME 
MAX_WAIT_TIME  = 10 * 60

def generate_processing_time():
    return random.expovariate(1 / 20.0)

def security_check(env, passengers_data, passenger_id, departureTime, security_lanes, priority, 
                    virtual_waiting_time_list, normal_waiting_time_list, 
                   waiting_time_intervals, aantal_miss, miss_list, new_waiting_time_intervals, metropolisGen):
    arrival_time = env.now

    if priority == 0:
        start_wait_time = env.now
        while len(security_lanes[0].queue) > 0 and (env.now - start_wait_time) < MAX_WAIT_TIME:
            yield env.timeout(1) 

    shortest_lane = min(security_lanes, key=lambda x: len(x.queue))
    with shortest_lane.request() as request:
        yield request
        yield env.timeout(next(metropolisGen))
        waiting_time = env.now - arrival_time

        if priority == 1:
            virtual_waiting_time_list.append(waiting_time)
        else:
            normal_waiting_time_list.append(waiting_time)    

        aantal_miss = 1 if env.now > departureTime else 0
        miss_list.append(aantal_miss)
        waiting_time_intervals[-1].append(waiting_time)
        new_waiting_time_intervals[-1].append(waiting_time)

        information_add(passengers_data, passenger_id, waiting_time, aantal_miss)

    #return new variabel
    return ( virtual_waiting_time_list, normal_waiting_time_list, 
            waiting_time_intervals, aantal_miss, miss_list, new_waiting_time_intervals)




def passenger_generator(env, security_lanes, passengers_data,virtual_waiting_time_list, normal_waiting_time_list, 
                        waiting_time_intervals, aantal_miss, miss_list, new_waiting_time_intervals, metropolisGen):
    for _, passenger in passengers_data.iterrows():
        passenger_id = passenger['Id']
        priority = passenger['Priority']
        departureTime = passenger['DepartureTime']
        arrival_time = passenger['new_ArrivalTime']
        yield env.timeout(max(0, arrival_time - env.now)) 
        env.process(security_check(env, passengers_data, passenger_id, departureTime, security_lanes, priority, 
                    virtual_waiting_time_list, normal_waiting_time_list, 
                   waiting_time_intervals, aantal_miss, miss_list, new_waiting_time_intervals, metropolisGen))

def adjust_security_lanes(env, security_lanes, security_data):
    for _, row in security_data.iterrows():
        time, lanes = row['Time'], row['Lanes']
        yield env.timeout(time - env.now)
        while len(security_lanes) < lanes:
            security_lanes.append(simpy.Resource(env, capacity=1))
        while len(security_lanes) > lanes:
            security_lanes.pop()

def calculate_average_waiting_time(env, time_interval, waiting_time_intervals, average_waiting_times, average_virtual_waiting_times, average_normal_waiting_times,aantal_miss,
                                  aantal_miss_interval_list,virtual_waiting_time_list, normal_waiting_time_list, miss_list, new_waiting_time_intervals,time_intervals_start):
    current_time = 0
    while True:
        yield env.timeout(time_interval)
        current_time += time_interval

        if waiting_time_intervals[-1]:
            avg_waiting_time = sum(waiting_time_intervals[-1]) / len(waiting_time_intervals[-1])
        else:
            avg_waiting_time = 0
        average_waiting_times.append(avg_waiting_time)

        if virtual_waiting_time_list:
            avg_virtual_waiting_time = sum(virtual_waiting_time_list) / len(virtual_waiting_time_list)
        else:
            avg_virtual_waiting_time = 0
        average_virtual_waiting_times.append(avg_virtual_waiting_time)

        if normal_waiting_time_list:
            avg_normal_waiting_time = sum(normal_waiting_time_list) / len(normal_waiting_time_list)
        else:
            avg_normal_waiting_time = 0
        average_normal_waiting_times.append(avg_normal_waiting_time)
        
        if miss_list:
            aantal_miss_interval = sum(miss_list)
        else:
            aantal_miss_interval = 0
        aantal_miss_interval_list.append(aantal_miss_interval)

        # Update the time_intervals_start and waiting_time_intervals for the next interval
        time_intervals_start.append(current_time - time_interval)
        waiting_time_intervals.append([])
        new_waiting_time_intervals.append([])
        virtual_waiting_time_list.clear()
        normal_waiting_time_list.clear()
        miss_list.clear()

    # Return the modified lists
    return  (waiting_time_intervals, average_waiting_times, average_virtual_waiting_times, average_normal_waiting_times,aantal_miss, 
             aantal_miss_interval_list,virtual_waiting_time_list, normal_waiting_time_list, miss_list, new_waiting_time_intervals,time_intervals_start)


def reset_variables():
    virtual_waiting_time_list = []
    normal_waiting_time_list = []
    waiting_time_intervals = [[]]
    average_waiting_times = []
    time_intervals_start = []
    average_virtual_waiting_times = []
    average_normal_waiting_times = []
    aantal_miss = 0
    miss_list = []
    aantal_miss_interval_list = []
    new_waiting_time_intervals = []

    return (virtual_waiting_time_list, normal_waiting_time_list, 
            waiting_time_intervals, average_waiting_times, time_intervals_start,
            average_virtual_waiting_times, average_normal_waiting_times, 
            aantal_miss, miss_list, aantal_miss_interval_list, new_waiting_time_intervals)

def run_simulation(sim_time, passengers_data, security_data, metropolisGen):
    #reset all variable
    (virtual_waiting_time_list, normal_waiting_time_list, 
     waiting_time_intervals, average_waiting_times, time_intervals_start, 
     average_virtual_waiting_times, average_normal_waiting_times, 
     aantal_miss, miss_list, aantal_miss_interval_list, new_waiting_time_intervals) = reset_variables()

    env = simpy.Environment()
    initial_lanes = security_data['Lanes'].iloc[0]
    security_lanes = [simpy.Resource(env, capacity=1) for _ in range(initial_lanes)]
    
    waiting_time_intervals.append([])

    env.process(passenger_generator(env, security_lanes, passengers_data,virtual_waiting_time_list, normal_waiting_time_list, 
                   waiting_time_intervals, aantal_miss, miss_list, new_waiting_time_intervals, metropolisGen))
    env.process(adjust_security_lanes(env, security_lanes, security_data))
    env.process (calculate_average_waiting_time(env, time_interval, waiting_time_intervals, average_waiting_times, average_virtual_waiting_times, average_normal_waiting_times,aantal_miss,
                                  aantal_miss_interval_list,virtual_waiting_time_list, normal_waiting_time_list, miss_list, new_waiting_time_intervals,time_intervals_start))
    env.run(until=sim_time)
    
    df_stats = pd.DataFrame({
        'Average Waiting Time': average_waiting_times,
        'Average Virtual Queue Waiting Time': average_virtual_waiting_times,
        'Average Normal Queue Waiting Time': average_normal_waiting_times,
        'Aantal miss flight': aantal_miss_interval_list
    }, index=time_intervals_start)

    new_passengers_data = passengers_data
    return df_stats, new_waiting_time_intervals, new_passengers_data


def multiple_run_simulation(runs, sim_time, passengers_data, flights_data, security_data, time_slots, duration, lane_capacity, distInfo):
    # Amount of samples to take
    amountSamples = len(passengers_data["ArrivalTime"])
    
    # Covert data to right format
    passengers_data, security_data = input_data(passengers_data,security_data,flights_data)
    duration /= 60
    lane_capacity /= 15

    # Run simulations
    total_avg_waiting_times = None
    for i in range(runs):
        metropolisGen = metropolisHastings(amountSamples = amountSamples, **distInfo)
        # Set new arrival times
        passengers_data = process_virtual_queue(passengers_data, time_slots.copy(), duration * 60).sort_values(by='new_ArrivalTime')

        average_waiting_time_df,waiting_time_intervals,new_passengers_data = run_simulation(sim_time, passengers_data, security_data, metropolisGen)
        if total_avg_waiting_times is None:
            total_avg_waiting_times = average_waiting_time_df
            combined_intervals= waiting_time_intervals
        else:
            total_avg_waiting_times = total_avg_waiting_times.add(average_waiting_time_df, fill_value=0)
            combined_intervals = [a + b for a, b in zip(combined_intervals, waiting_time_intervals)]
    overall_average = total_avg_waiting_times / runs

    # Use function calculate_average_waiting_time() to output the str
    overall_average["Time in hour"] = overall_average.index / 3600
    average_waiting_time_min = calculate_average_waiting_time_int(overall_average, 'Average Waiting Time')
    average_Virtual_waiting_time_min = calculate_average_waiting_time_int(overall_average, 'Average Virtual Queue Waiting Time')
    average_Normal_waiting_time_min = calculate_average_waiting_time_int(overall_average, 'Average Normal Queue Waiting Time')

    #convert_to_minutes
    simulation_result_df,passengers_data,waiting_time_intervals_minutes = convert_to_minutes(overall_average,passengers_data,waiting_time_intervals)

    #select miss passengers
    passengers_data_miss = passengers_data[passengers_data["miss_flight"]==1]
    print("miss_flight_information",passengers_data_miss)
    # Convert to dictionaries of structure list per column
    simulation_result_df = simulation_result_df.to_dict(orient = "list")
    passengers_data_miss = passengers_data_miss.to_dict(orient = "list")
    
    return (simulation_result_df, combined_intervals,passengers_data_miss,waiting_time_intervals_minutes,
    average_waiting_time_min,average_Virtual_waiting_time_min,average_Normal_waiting_time_min)



def information_add(passengers_data, passenger_id, waiting_time, miss_flight):
    if passenger_id in passengers_data['Id'].values:
        passengers_data.loc[passengers_data['Id'] == passenger_id, 'waitingTime'] = waiting_time
        passengers_data.loc[passengers_data['Id'] == passenger_id, 'miss_flight'] = miss_flight

