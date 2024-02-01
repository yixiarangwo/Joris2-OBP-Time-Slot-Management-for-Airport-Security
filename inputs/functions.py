from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from datetime import datetime, date

import numpy as np
from numba import njit

# Prevent repeating code for making new html divs for time slots input
# Count is used to separate the different time slots for data conversion later
def timeSlotsDiv(flight, count, time = None, cap = ""):
    return dmc.Group([
        dmc.TimeInput(
            value = time,
            id = {"section": "inputs", "type": "input", "index": "time-slots", "flight": flight, "info": "start-time", "count": count},
            style = {
                "width": "5rem",
                "height": "2rem",
                "padding": 0,
                "margin": 0
            }
        ),
        dmc.NumberInput(
            value = cap,
            id = {"section": "inputs", "type": "input", "index": "time-slots", "flight": flight, "info": "capacity", "count": count},
            style = {
                "width": "5rem",
                "height": "2rem",
                "margin": 0,
                "padding": 0,
                "marginLeft": "-0.5rem",
                "marginBottom": "0.5rem"
            },
            min = 0
        ),
        dmc.ActionIcon(
            DashIconify(icon = "ion:remove", width = 35),
            id = {"section": "inputs", "type": "button", "index": "time-slots", "flight": flight, "info": "remove-slot", "count": count},
            style = {
                "margin": 0, 
                "marginLeft": "-0.5rem",
                "marginRight": "-2rem",
                "padding": 0,
                "width": "2.25rem"
            },
            title = "Remove this time slot",
            size = "2.25rem",
        ),
    ], align = "start", style = {"margin": 0, "padding": 0, "marginLeft": "0.6rem", "marginBottom": "0.5rem"})


# Same as timeSlotsDiv but for time slot recommendations
def timeSlotsRecsDiv(flight, count, time, cap):
    return dmc.Group([
        dmc.TimeInput(
            time,
            id = {"section": "inputs", "type": "input", "index": "time-slots-recom", "flight": flight, "info": "start-time", "count": count},
            style = {
                "width": "5rem",
                "height": "2rem",
                "padding": 0,
                "margin": 0,
                "marginLeft": "-0.5rem",
                "marginBottom": "0.5rem"
            },
            disabled = True
        ),
        dmc.NumberInput(
            cap,
            id = {"section": "inputs", "type": "input", "index": "time-slots-recom", "flight": flight, "info": "capacity", "count": count},
            style = {
                "width": "5rem",
                "height": "2rem",
                "margin": 0, 
                "padding": 0,
                "marginLeft": "-0.5rem",
                "marginBottom": "0.5rem"
            },
            disabled = True
        )],
        className = "justify-contents-center justify-content-center align-items-center",
        align = "start", 
        style = {
            "margin": 0, 
            "padding": 0, 
            "marginLeft": "0.7rem"
        }
    )



# Function to extract the inputted time slots from a div
def timeSlotsFromDiv(capacities, startTimes):
    timeSlots = {}
    [
        (
            timeSlots[capacity["id"]["flight"]]["capacity"].append(capacity["value"]),
            timeSlots[capacity["id"]["flight"]]["start"].append(time24ToUnix(time["value"]))
        )
        if capacity["id"]["flight"] in timeSlots
        else timeSlots.update(
            {
                capacity["id"]["flight"]: {
                    "capacity": [capacity["value"]],
                    "start":    [time24ToUnix(time["value"])]
                }
            }
        )
        for capacity, time in zip(capacities, startTimes)
        if isinstance(capacity["value"], int) or isinstance(time["value"], str)
    ]
    return timeSlots
    


# Convert from Unix time to hours and minutes
def unixToTime24(unixTime):
    # Get hours and minutes
    hours = unixTime // 3600
    minutes = (unixTime % 3600) // 60

    # Format to 24-hour format
    return f"{hours:02d}:{minutes:02d}"

# Convert from Unix time to datetime object
def unixToDateTime(unixTime):
    # Error check
    if unixTime is None:
        return None

    # Get hours and minutes
    hours = int(unixTime // 3600)
    minutes = int((unixTime % 3600) // 60)

    now = date.today()

    # Format to 24-hour format
    return datetime(now.year, now.month, now.day, hours, minutes)


# Convert from hours and minutes to Unix
def time24ToUnix(strTime, fill = None):
    # Check if no time given
    if strTime is None:
        return fill

    # Get hours and minutes
    hours, minutes = strTime.split('T')[-1].split(':')[:-1]
    
    # Convert to unix
    return int(hours) * 3600 + int(minutes) * 60



# Given inputted time slots, adjust arrivals by moving them to the time slots.
# Three cases are done: 
#    1. Always picking top bar from histogram, 
#    2. Always picking lowerst (above 0) bar from histogram,
#    3. Always picking the bar closest to the average bar count.
@njit(cache = True)
def timeSlotCases(arrivalTimes, capacities, unixSlots, histBinStarts, binSlotIndices):#flights, capacities, unixSlots, histBinStarts, binSlotIndices):#arrivalFlights, capacities, unixSlots, histBinStarts, binSlotIndices):#flights, capacities, unixSlots, histBinStarts, binSlotIndices):
    # Make histogram of arrivals manually
    binArrivalIndices = [
        max([
            i if arrival > time or np.isclose(arrival, time) else -1
            for i, time in enumerate(histBinStarts)
        ])
        if arrival is not None else -1
        for arrival in arrivalTimes
    ]
    binArrivals = [
        [
            arrivalTimes[i]
            for i, index in enumerate(binArrivalIndices)
            if index > -1 and index == binIdx
        ]
        for binIdx in range(len(histBinStarts))
    ]

    """
    binFLights = [
        [
            arrivalFlights, Times[i]
            for i, index in enumerate(binArrivalIndices)
            if index > -1 and index == binIdx
        ]
        for binIdx in range(len(histBinStarts))
    ]
    """

    # Make copies
    topBinArrivals =  binArrivals
    bottomBinArrivals = binArrivals.copy()
    avgBinArrivals =   binArrivals.copy()

    # Loop and treat each scenario separately
    for i, capacity in enumerate(capacities):
        if (capacity < 0) or (unixSlots[i] < 0) or (binArrivalIndices[i] < 0):
            pass
        else:        
            for _ in range(capacity):
                # Get counts per bin (not including bins without counts)
                topBinCounts =  [len(binCount) for idx, binCount in enumerate(topBinArrivals)]
                                  
                bottomBinCounts = [len(binCount) for idx, binCount in enumerate(bottomBinArrivals)]
                                  
                avgBinCounts =   [len(binCount) for idx, binCount in enumerate(avgBinArrivals)]

                # Get boolean lists with whether there is a passenger belonging to time slot flight of bin
                # and list whether there are any passengers in that list
                #flightInBin = []
                #notZero = 
                
                # Find bin with most counts if there is a passenger in that bin
                maxTopCount = max(topBinCounts)
                #max(index for i, index in enumerate(topBinCounts) if flightInBin[i] and notZero[i])
                mostIdx = [idx for idx, binCount in enumerate(topBinCounts) if maxTopCount == binCount][0]
                
                # Find bin with least counts
                minBottomCount = min(bottomBinCounts)
                leastIdx = [idx for idx, binCount in enumerate(bottomBinCounts) if minBottomCount == binCount][0]
        
                # Find bin closest to average bin count
                avgCount = sum(avgBinCounts) / len(avgBinCounts)
                avgDiffCounts = [abs(binCount - avgCount) for binCount in avgBinCounts]
                minAvgDiff = min(avgDiffCounts)
                avgIdx = [idx for idx, diffCount in enumerate(avgDiffCounts) if minAvgDiff == diffCount][0]

                # Adjust for empty bins
                for j, (bottomBinCount, avgBinCount) in enumerate(zip(bottomBinArrivals, avgBinArrivals)):
                    if j <= leastIdx and len(bottomBinCount) == 0:
                        leastIdx += 1
                    if j <= avgIdx and len(avgBinCount) == 0:
                        avgIdx += 1
                
                ### Change arrival times of single passengers for each scenario
                ## Top pick case: pick from top bin count and change to start of time slot
                # Set new arrival time
                topBinArrivals[mostIdx][0] = histBinStarts[binSlotIndices[i]] + 1
                
                # Copy the arrival to right bin
                topBinArrivals[binSlotIndices[i]].append(topBinArrivals[mostIdx][0])
                
                # Remove the arrival from top bin
                topBinArrivals[mostIdx].pop(0)
    
                
                ## Bottom pick case: pick from bottom bin count and change to start of time slot
                # Set new arrival time
                bottomBinArrivals[leastIdx][0] = histBinStarts[binSlotIndices[i]] + 1
    
                # Copy the arrival to right bin
                bottomBinArrivals[binSlotIndices[i]].append(bottomBinArrivals[leastIdx][0])
    
                # Remove the arrival from top bin
                bottomBinArrivals[leastIdx].pop(0)
    
    
                ## Average case: pick from bin closest to average bin count and change arrival to start of time slot
                # Set new arrival time
                avgBinArrivals[avgIdx][0] = histBinStarts[binSlotIndices[i]] + 1
    
                # Copy the arrival to right bin
                avgBinArrivals[binSlotIndices[i]].append(avgBinArrivals[avgIdx][0])
    
                # Remove the arrival from top bin
                avgBinArrivals[avgIdx].pop(0)
    
    # Make datasets from each case
    topArrivalData =  [time for bin in topBinArrivals for time in bin]
    bottomArrivalData = [time for bin in bottomBinArrivals for time in bin]
    avgArrivalData =   [time for bin in avgBinArrivals for time in bin]

    return topArrivalData, bottomArrivalData, avgArrivalData
