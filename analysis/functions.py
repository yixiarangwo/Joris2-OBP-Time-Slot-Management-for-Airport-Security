from importables.functions import latexToNumpy

import numpy as np

# Draw from given LaTeX function with Metropolis-Hastings algorithm for service times in simulation
def MHsamples(latexExpression, amountSamples, sigma, initial, lower, upper, lowerExpansion, upperExpansion):
	"""
	Implementing the Metropolis-Hastings algorithm to draw samples from random continuous function
	This function uses random walk where sigma is adjustable in case it is too small/large for the distribution

	latexExpression: inputted latex string which will be converted to usable function
	amountSamples: amount of samples that will outputted
	sigma: "step size" of jump distribution, here a normal distribution with mean of previous accepted candidate
	inital: the initial value used for the algorithm determined earlier by testing the parameters
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
	
	# Make lambda func for checking if candidate is within bounds
	if lower is not None and upper is not None:
		checkBounds = lambda x: x >= lower and x <= upper
	elif lower is not None:
		checkBounds = lambda x: x >= lower
	elif upper is not None:
		checkBounds = lambda x: x <= upper
	else:
		checkBounds = lambda x: True

	# Create samples
	samples = np.zeros(amountSamples)
	accepted = 0
	
	while accepted < amountSamples:
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
	
	# Shuffle and return
	samples = np.asarray(samples)
	np.random.shuffle(samples)
	return samples
