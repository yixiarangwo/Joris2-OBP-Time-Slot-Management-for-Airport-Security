import io
import base64
import numpy as np
import pandas as pd
import sympy as sp
from latex2sympy2 import latex2sympy
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.tools as tls
import plotly.graph_objs as go
############################################ Importables tab ############################################
# Function to parse content from csv-file to dataframe
def parseContents(contents, structure = "list"):#, fileName):
    # Decode content
    contents_type, contents_string = contents.split(',')
    decoded = base64.b64decode(contents_string)
    
    # Assume that the user uploaded a CSV file
    try:
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        json = df.to_dict(orient = structure)
        return json#, fileName
    except Exception as e:
        print(e)
        return ''#, "Error!"

# Function to parse LaTeX expression to numpy function, ADD LOWER AND UPPER BOUND
def latexToNumpy(latexExpression):
	try:
		sympFunc = latex2sympy(latexExpression)
		numpFunc = sp.lambdify('x', sympFunc, "numpy")
		return np.vectorize(numpFunc)
	except Exception as e:
		print(e)
		return html.Div(["There was an error processing the LaTeX equation"])


############################################ Inputs tab ############################################

############################################Analysis tab##########################################

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
