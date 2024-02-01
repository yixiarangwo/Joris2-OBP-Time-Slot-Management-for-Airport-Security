import random
import pandas as pd
import numpy as np
import copy

def generate_time_slots(start_time, end_time, duration):
    """
    Generate avalaible time slots based on start time, end time and duration of time slots.
    """    
    time_interval_seconds = int(duration * 60)
    return list(range(int(start_time), int(end_time), int(time_interval_seconds)))

def adjust_peak_period_start_end(duration):
    """
    Generate start and end times for peak periods
    """    
    #Peak period 1: 04:15 - 05:15
    peak_periods1_start = 4.25 * 60 * 60  
    peak_periods1_end = 5.25 * 60 * 60    
    
    #Peak period 2: 07:30 - 09:15
    peak_periods2_start = 7.5 * 60 * 60  
    peak_periods2_end = 9.25 * 60 * 60    
    
    if duration == 10:
        #Peak period 1: 04:10 - 05:20
        peak_periods1_start = (4 + 1/6) * 60 * 60
        peak_periods1_end = (5 + 1/3) * 60 * 60
        
        #Peak period 2: 07:30 - 09:20
        peak_periods2_start = 7.5 * 60 * 60  
        peak_periods2_end = (9 + 1/3) * 60 * 60
        
    return peak_periods1_start, peak_periods1_end, peak_periods2_start, peak_periods2_end        

def recommendedTimeSlots(passengers_dict, security_dict, flights_dict, duration, lane_capacity):
    """
    Get the number of passenger arrivals for each time period, the number of people exceeding the security capacity,
    and the idle capacity security.
    
    """
    passengers_data = pd.DataFrame.from_dict(passengers_dict)
    security_data = pd.DataFrame.from_dict(security_dict)
    flights_data = pd.DataFrame.from_dict(flights_dict)
    
    time_interval_seconds = duration
    time_range = range(0, 12 * 3600 + 1, time_interval_seconds)

    duration /= 60
    lane_capacity /= 15
   
    # ArrivalCount
    passengers_data['AlignedArrivalTime'] = passengers_data['ArrivalTime'] - (passengers_data['ArrivalTime'] % time_interval_seconds)
    arrival_counts = passengers_data['AlignedArrivalTime'].value_counts().sort_index()
    
    arrival_df = pd.DataFrame({'ArrivalCount': [0] * len(time_range)}, index=time_range)
    arrival_df.index.name = 'Time'
    arrival_df.reset_index(inplace=True)
    arrival_df.loc[arrival_df['Time'].isin(arrival_counts.index), 'ArrivalCount'] = arrival_counts.values
    
    # Merge security_data and arrival_df 
    merged_data =  arrival_df
    merged_data['Lanes'] = 1  # Initially set to 1

    # Iterate over security_data to update Lanes
    for _, row in security_data.iterrows():
        start_time = row['Time']
        lanes = row['Lanes']
        # Assuming that security_data is logged every 15 minutes, so each record covers 15 minutes
        end_time = start_time + 15 * 60

        # Update Lanes in arrival_df
        arrival_df.loc[(arrival_df['Time'] >= start_time) & (arrival_df['Time'] < end_time), 'Lanes'] = lanes
    
    # Calculate ExcessPassengers and IdleCapacity
    merged_data['SecurityCapacity'] = merged_data['Lanes'] * lane_capacity * duration
    merged_data['ExcessPassengers'] = merged_data.apply(lambda row: max(row['ArrivalCount'] - row['SecurityCapacity'], 0), axis=1)
    merged_data['IdleCapacity'] = merged_data.apply(lambda row: max(row['SecurityCapacity'] - row['ArrivalCount'], 0), axis=1)
    
    arrival_data = merged_data[["Time", 'ArrivalCount', "Lanes", "SecurityCapacity", "ExcessPassengers", "IdleCapacity"]]
    
    # Initialize the virtual queue with capacity allocations
    virtual_queue = {}
    
    peak_periods1_start, peak_periods1_end, peak_periods2_start, peak_periods2_end = adjust_peak_period_start_end(duration)
    
    flight_time_slots = {
        "BM2616": generate_time_slots(4*3600, peak_periods1_start, duration) + generate_time_slots(peak_periods1_end, 5.25*3600+1, duration),#Depature 05:45
        "XC6333": generate_time_slots(peak_periods1_end, 5.5*3600+1, duration), #Depature 06:00
        "OO2037": generate_time_slots(peak_periods1_end, 5.75*3600+1, duration), #Depature 06:15
        "HP4524": generate_time_slots(peak_periods1_end, 6*3600+1, duration), #Depature 06:30
        "DN7022": generate_time_slots(peak_periods1_end, 6.25*3600+1, duration), #Depature 06:45
    
        "QX7315": generate_time_slots(7*3600, peak_periods2_start, duration),#Depature 09:30
        "SS2446": generate_time_slots(peak_periods2_end, 9.25*3600+1, duration), #Depature 09:45
        "ZI1701": generate_time_slots(peak_periods2_end, 9.5*3600+1, duration), #Depature 10:00
        "HC1255": generate_time_slots(peak_periods2_end, 9.75*3600+1, duration), #Depature 10:15
        "HF1818": generate_time_slots(peak_periods2_end, 10*3600+1, duration), #Depature 10:30
        "IG2596": generate_time_slots(peak_periods2_end, 10.25*3600+1, duration) #Depature 10:45
    }
    
    # Process each flight
    for flight, time_slots in flight_time_slots.items():

        """
        The capacity of the time slots is allocated based on the available time slots for each flight, 
        and the idle capacity for that time period. 
        """
        allocations = {slot: 0 for slot in time_slots}  # Initialize allocations

        for slot in time_slots:
            available_capacity = arrival_data.loc[arrival_data['Time'] == slot, 'IdleCapacity'].values[0]

            for _, row in arrival_data.iterrows():
                if row['Time'] == slot:
                    continue

                if available_capacity > 0:
                    passengers_to_allocate = available_capacity
                    allocations[slot] += passengers_to_allocate
                    available_capacity -= passengers_to_allocate
                    arrival_data.loc[arrival_data['Time'] == slot, 'IdleCapacity'] = 0
                    
                    if available_capacity <= 0:
                        break


        # Add to virtual queue
        virtual_queue[flight] = {"start": time_slots, "capacity": list(allocations.values())}
        
    return virtual_queue
