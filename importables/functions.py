import io
import base64
import random
import numpy as np
import pandas as pd
import sympy as sp
from numba import jit
from scipy.optimize import fmin
from latex2sympy2 import latex2sympy


# Function to parse content from csv-file to dataframe
def parseContents(contents, structure = "list"):
    # Assure input format
    if not isinstance(contents, list):
        contents = [contents]
    
    # Parse files separately and concatenate
    df = pd.DataFrame()
    for content in contents:
        # Assume that the user uploaded a CSV file and concat
        try:
            # Decode contents
            contents_type, contents_string = content.split(',')
            decoded = base64.b64decode(contents_string)

            # Add data to dataframe
            df = pd.concat([df, pd.read_csv(io.StringIO(decoded.decode("utf-8")))],
                           ignore_index = True)
        except Exception as e:
            return '', False

    # Convert df to json-like structure
    json = df.to_dict(orient = structure)
    return json, True



# Check if needed data from arrivals are complete
def arrivalDataCheck(arrivalData):
    # Check if needed columns names exist
    times = arrivalData.get("ArrivalTime", None)
    flights = arrivalData.get("FlightNumber", None)
    if times is None or flights is None:
        return False

    # Check if columns are lists
    if not (isinstance(times, list) and isinstance(flights, list)):
        return False
    
    # Check if there are an equal amount of elements in both lists
    if len(times) != len(flights):
        return False

    # Check if all elements are floats or integers and strings
    elemCheckTimes = all(isinstance(time, int) or isinstance(time, float) for time in times)
    elemCheckFlights = all(isinstance(flights, str) for flight in flights)
    if not (elemCheckTimes or elemCheckFlights):
        return False

    # Check if for all 0 <= time < 24 * 3600
    maxTime = 24 * 3600
    if not all(0 <= time < maxTime for time in times):
        return False

    # Passed tests
    return True
    


# Check if needed data from flight schedule are complete
def flightDataCheck(flightData):
    # Check if needed columns names exist
    flights = flightData.get("FlightNumber", None)
    passengers = flightData.get("Passengers", None)
    if flights is None or passengers is None:
        return False

    # Check if columns are lists
    if not (isinstance(flights, list) and isinstance(passengers, list)):
        return False

    # Check if there are an equal amount of elements in both lists
    if len(flights) != len(passengers):
        return False

    # Check if all elements are strings and integers
    elemCheckFlights = all(isinstance(flight, str) for flight in flights)
    elemCheckPassengers = all(isinstance(cap, int)  for cap in passengers)
    if not (elemCheckFlights and elemCheckPassengers):
        return False

    # Check if passengers > 0
    if not all(cap > 0 for cap in passengers):
        return False

    # Passed tests
    return True
    


# Check if needed data from security lanes are complete
def laneDataCheck(laneData):
    # Check if needed columns names exist
    times = laneData.get("Time", None)
    openLanes = laneData.get("Lanes", None)
    if times is None or openLanes is None:
        return False

    # Check if columns are lists
    if not (isinstance(times, list) and isinstance(openLanes, list)):
        return False

    # Check if there are an equal amount of elements in both lists
    if len(times) != len(openLanes):
        return False

    # Check if all elements are (floats or) integers
    elemCheckTime = all(isinstance(time, int) or isinstance(time, float) for time in times)
    elemCheckLane = all(isinstance(lane, int) for lane in openLanes)
    if not (elemCheckTime and elemCheckLane):
        return False

    # Check if for all 0 <= time < 24 * 3600 and amount of lanes >= 0
    maxTime = 24 * 3600
    if not (all(0 <= time < maxTime for time in times) and 
            all(lane > 0 for lane in openLanes)):
        return False

    # Passed tests
    return True



# Function to parse LaTeX expression to numpy function
def latexToNumpy(latex, lower = None, upper = None, 
                 lowerExpansion = 0, upperExpansion = 0, **kwargs):
    try:
        sympFunc = latex2sympy(latex)
        numpFunc = sp.lambdify('x', sympFunc, "numpy")

        # Add lower and upper bound to function
        if lower is not None and upper is not None:
            lower -= lowerExpansion
            upper += upperExpansion
            distFunc = lambda x: numpFunc(x) if x >= lower and x <= upper else 0
        elif lower is not None:
            lower -= lowerExpansion
            distFunc = lambda x: numpFunc(x) if x >= lower else 0
        elif upper is not None:
            upper += upperExpansion
            distFunc = lambda x: numpFunc(x) if x <= upper else 0
        else:
            distFunc = lambda x: numpFunc(x)

        return np.vectorize(distFunc)

    except Exception as e:
        return None


# Draw from given LaTeX function with Metropolis-Hastings algorithm for service times in simulation
def metropolisHastings(latex, amountSamples, sigma, lower, upper, 
                       lowerExpansion, upperExpansion, burnIn = 0, **kwargs):
	"""
	Implementing the Metropolis-Hastings algorithm to draw samples from random continuous function
	This function uses random walk where sigma is adjustable in case it is too small/large for the distribution

	latexExpression: inputted latex string which will be converted to usable function
	amountSamples: amount of samples that will outputted
	sigma: "step size" of jump distribution, here a normal distribution with mean of previous accepted candidate
	burnIn: the amount of steps before saving samples
	lower: lower bound of given distribution. If None, lower bound is 'minus infinity'
	upper: upper bound of given distribution. If None, upper bound is 'infinity'
	lowerExpansion: the amount lower bound is extended for candidates but not for samples
	upperExpansion: the amount upper bound is extended for candidates but not for samples

	There are three downsides of this sampling method:
	- The algorithm needs a "burn in" period when the initial value is in a region of low probability
	- When a distribution has bounds, less samples will be drawn from the edges
	- Samples are autocorrelated
	
	Therefore, three extra steps are added to the original algorithm, each respectively alleviating the problems from above:
	- Get an estimate of local/global maximum priorly and use this as initial value, reducing the burn in period
	- Accepted candidates can be outside of bounds (to a given degree) but these are not outputted in sample list
	- Shuffle the samples posteriorly to (hopefully) reduce the impact of autocorrelation
	"""

	# Convert latexExpression to vectorized numpy function with bounds extended by boundSpace
	densityFunc = latexToNumpy(latex, lower, upper, lowerExpansion, upperExpansion)

	if densityFunc is None:
	    return None, ""
	
	# Rough estimation for maximum value as initial value algorithm and
	# make lambda func for checking if candidate within bounds
	if lower is not None and upper is not None:
	    initial = (lower + upper) / 2
	    checkBounds = lambda x: x >= lower and x <= upper
	elif lower is not None:
	    initial = lower
	    checkBounds = lambda x: x >= lower
	elif upper is not None:
	    initial = upper
	    checkBounds = lambda x: x <= upper
	else:
	    initial = 0
	    checkBounds = lambda x: True

	# More accurate estimation for maximum value using scipy
	initial = fmin(lambda x: -densityFunc(x), initial, disp = 0)[0]

	# Perform algorithm using initial value
	totalSamples = amountSamples + burnIn
	samples = np.zeros(totalSamples)
	accepted = 0

	while accepted < totalSamples:
	    nRands = np.random.normal(scale = sigma, size = (totalSamples - accepted) * 3)
	    uRands = np.random.uniform(size = (totalSamples - accepted) * 3)

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

	                if accepted >= totalSamples:
	                    # Remove burn in samples, shuffle and return
	                    samples = np.asarray(samples)[burnIn:]
	                    np.random.shuffle(samples)
	                    return samples, initial
