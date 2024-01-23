import io
import base64
import random
import numpy as np
import pandas as pd
import sympy as sp
from scipy.optimize import fmin
from latex2sympy2 import latex2sympy


# Function to parse content from csv-file to dataframe
def parseContents(contents, structure = "records"):#, fileName):
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


# Function to parse LaTeX expression to numpy function
def latexToNumpy(latexExpression, lower = None, upper = None, lowerExpansion = 0, upperExpansion = 0):
	try:
	    sympFunc = latex2sympy(latexExpression)
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
def metropolisHastings(latexExpression, amountSamples, sigma, burnIn = 1000, 
                       lower = None, upper = None, lowerExpansion = 0, upperExpansion = 0):
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
	densityFunc = latexToNumpy(latexExpression, lower, upper, lowerExpansion, upperExpansion)

	if densityFunc is None:
	    return None
	
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
	iterations = amountSamples + burnIn
	samples = np.zeros(iterations)
	accepted = 0
	
	while accepted < iterations:
		# Get candidate
		candidate = initial + np.random.normal(scale = sigma)
		
		# Calculate criterion from ratio (proportional) probs
		probInitial = densityFunc(initial)
		probCandidate = densityFunc(candidate)
    
		# Determine if candidate is accepted
		if np.random.uniform() < probCandidate / probInitial:
			if checkBounds(initial): 
			    samples[accepted] = initial
			    accepted += 1
			initial = candidate
	
	# Remove burn in samples, shuffle and return
	samples = np.asarray(samples)[burnIn:]
	np.random.shuffle(samples)
	return samples, initial
