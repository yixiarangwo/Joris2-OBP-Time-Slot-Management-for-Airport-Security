import plotly.graph_objs as go
import numpy as np

def create_plotly_histogram(arrival_df):
    # Convert ArrivalTime from seconds to hours
    arrival_times_in_hours = arrival_df['ArrivalTime'] / 3600

    # Create histograms
    hist_data = go.Histogram(
        x=arrival_times_in_hours,
        nbinsx=24, 
        name='Histogram',
        marker=dict(
            color='blue',
            line=dict(
                color='black',
                width=2
            )
        ),
        opacity=0.75
    )

    # Create chart objects
    fig = go.Figure(data=[hist_data])

    # Update the chart layout
    fig.update_layout(
        title_text='Distribution of Passenger Arrival Times',  
        xaxis_title_text='Time of Day (Hours)',  
        yaxis_title_text='Number of Passengers',  
        bargap=0.2, 
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,  
        ),
        plot_bgcolor='white'  
    )

    
<<<<<<< HEAD
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

    return fig

import plotly.graph_objs as go

import plotly.graph_objs as go

def create_time_interval_plot(df):
    fig = go.Figure()

    
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Waiting Time'],
        mode='markers+lines',
        name='Average Waiting Time', 
        marker=dict(color='blue', size=7)
    ))

    
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Virtual Queue Waiting Time'],
        mode='markers+lines',
        name='Average Virtual Queue Waiting Time',
        marker=dict(color='red', size=7)
    ))

    
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Normal Queue Waiting Time'],
        mode='markers+lines',
        name='Average Normal Queue Waiting Time',
        marker=dict(color='green', size=7)
    ))

    
    fig.update_layout(
        title='Average Waiting Time at Security Check (per 15-minute Interval)',
        xaxis_title='Time Interval',
        yaxis_title='Average Waiting Time (second)',
        xaxis=dict(tickangle=45),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        showlegend=True  
    )

    return fig

def create_time_interval_without_plot(df):
    fig = go.Figure(data=go.Scatter(
        x=df['Time in hour'],
        y=df['Average Waiting Time'],
        mode='markers+lines',  
        marker=dict(color='blue', size=7)  
    ))
    fig.update_layout(
        title='Average Waiting Time at Security Check (per 15-minute Interval)',
        xaxis_title='Time Interval',
        yaxis_title='Average Waiting Time (second)',
        xaxis=dict(tickangle=45),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        showlegend=False
    )
    return fig
=======
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

# Draw from given LaTeX function with Metropolis-Hastings algorithm for service times in simulation
def MHgenerator(latexExpression, amountSamples, sigma, initial, lower, upper, lowerExpansion, upperExpansion):
	"""
	Same function as in ./importables/functions.py but made as a generator.
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
	
	# Shuffle samples
	samples = np.asarray(samples)
	np.random.shuffle(samples)

	# Yield shuffled samples
	for i in range(amountSamples):
	    yield samples[i]
>>>>>>> 137bfe79c5e68be04e44f4b48729feecf7e97afd
