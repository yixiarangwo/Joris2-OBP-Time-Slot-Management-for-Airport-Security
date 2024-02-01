import numpy as np
from scipy.optimize import fmin

from importables.functions import latexToNumpy

def calculate_average_waiting_time_int(simulation_result_df, column_name):
    non_zero_values = simulation_result_df[simulation_result_df[column_name] != 0]
    non_zero_count = non_zero_values[column_name].count()
    if non_zero_count == 0:
        return (0, 0)

    average_waiting_time = non_zero_values[column_name].sum() / non_zero_count
    average_waiting_time_minutes = average_waiting_time // 60
    average_waiting_time_seconds = average_waiting_time % 60
    return (int(average_waiting_time_minutes), int(average_waiting_time_seconds))



def convert_to_minutes(simulation_result_df,passengers_data,waiting_time_intervals):    
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



# Draw from given LaTeX function with Metropolis-Hastings algorithm for service times in simulation
def metropolisHastings(latex, amountSamples, sigma, lower, upper, 
                       lowerExpansion, upperExpansion, initial):
    """
    Same as other metropolis hastings algorith but now with a yield for simpy.
    """
    # Convert latexExpression to vectorized numpy function with bounds extended by boundSpace
    densityFunc = latexToNumpy(latex, lower, upper, lowerExpansion, upperExpansion)
    
    # Determine good initial if not yet determined
    if initial == "":
        # Rough estimation for maximum value as initial value algorithm and
        if lower is not None and upper is not None:
            initial = (lower + upper) / 2
        elif lower is not None:
            initial = lower
        elif upper is not None:
            initial = upper
        else:
            initial = 0

        # More accurate estimation for maximum value using scipy
        initial = fmin(lambda x: -densityFunc(x), initial, disp = 0)[0]
    
    # Make lambda func for checking if candidate within bounds
    if lower is not None and upper is not None:
        checkBounds = lambda x: x >= lower and x <= upper
    elif lower is not None:
        checkBounds = lambda x: x >= lower
    elif upper is not None:
        checkBounds = lambda x: x <= upper
    else:
        checkBounds = lambda x: True

    # Perform algorithm using initial value
    samples = np.zeros(amountSamples)
    accepted = 0
    
    while accepted < amountSamples:
        nRands = np.random.normal(scale = sigma, size = (amountSamples - accepted) * 3)
        uRands = np.random.uniform(size = (amountSamples - accepted) * 3)
        
        for uRand, nRand in zip(uRands, nRands):
            # Get candidate
            candidate = initial + nRand
            
            # Calculate criterion from ratio (proportional) probs
            probInitial = densityFunc(initial)
            probCandidate = densityFunc(candidate)
            
            # Determine if candidate is accepted
            if uRand < (probCandidate / probInitial):
                initial = candidate
                if checkBounds(candidate):
                    samples[accepted] = candidate
                    accepted += 1
                    if accepted >= amountSamples:
                        break
        if accepted >= amountSamples:
            break
    
    # Remove burn in samples, shuffle and yield
    samples = np.asarray(samples)
    np.random.shuffle(samples)
    for sample in samples:
        yield sample
