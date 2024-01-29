import plotly.graph_objs as go
import numpy as np
import plotly.express as px

def create_time_interval_plot(df):
    # Create a line plot with markers using plotly express
    fig = px.line(
        df, 
        x='Time in hour', 
        y=['Average Waiting Time', 'Average Virtual Queue Waiting Time', 'Average Normal Queue Waiting Time'],
        markers=True
    )

    # Update the layout of the plot
    fig.update_layout(
        title='Average Waiting Time at Security Check (per 15-minute Interval)',
        xaxis_title='Time Interval',
        yaxis_title='Average Waiting Time (minutes)',
        xaxis=dict(tickangle=45),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        showlegend=True
    )

    # Update traces for style
    fig.for_each_trace(
        lambda trace: trace.update(marker=dict(size=7)) if trace.name == 'Average Waiting Time' else (),
    )
    fig.for_each_trace(
        lambda trace: trace.update(marker=dict(color='red', size=7)) if trace.name == 'Average Virtual Queue Waiting Time' else (),
    )
    fig.for_each_trace(
        lambda trace: trace.update(marker=dict(color='green', size=7)) if trace.name == 'Average Normal Queue Waiting Time' else (),
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


def create_miss_flight_time_interval_plot(df):
    # Create a line and marker plot using plotly express
    fig = px.line(
        df, 
        x='Time in hour', 
        y='Aantal miss flight', 
        title='Number of passengers who missed flights',
        markers=True
    )

    # Update the layout of the plot
    fig.update_layout(
        xaxis_title='Time Interval',
        yaxis_title='Aantal miss flight',
        xaxis=dict(tickangle=45),
        plot_bgcolor='white',
        showlegend=True
    )

    # Update the traces for style
    fig.update_traces(
        name='Aantal miss flight',
        marker=dict(color='blue', size=7)
    )

    # Update grid style
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

    return fig


def create_service_level_plot(df):
    # Calculate the 95th and 80th percentiles for the 'waitingTime' column
    percentile_95 = np.percentile(df['waitingTime'], 95)
    percentile_80 = np.percentile(df['waitingTime'], 80)

    # Create a histogram using plotly express
    fig = px.histogram(
        df, 
        x='waitingTime', 
        nbins=24, 
        title='Waiting Time Distribution for all passengers with Service Levels',
        labels={'waitingTime': 'Waiting Time (minutes)'},
        opacity=0.7
    )

    # Update the layout of the plot
    fig.update_layout(
        yaxis_title='Number of Passengers',
        legend=dict(
            itemsizing='constant',
            orientation='h',
            xanchor='center',
            x=0.5,
            y=-0.3
        ),
        bargap=0.2
    )

    # Update the traces for histogram style
    fig.update_traces(
        marker=dict(color='blue', line=dict(color='black', width=1)),
        name='Waiting Time Distribution'
    )

    # Calculate the maximum height of the histogram
    hist_data = np.histogram(df['waitingTime'], bins=24)
    max_hist_height = max(hist_data[0])

    # Add a line trace for 95% service level
    fig.add_trace(
        go.Scatter(
            x=[percentile_95, percentile_95],
            y=[0, max_hist_height],
            mode="lines",
            line=dict(color="Red", width=2, dash="dash"),
            name='95% Service Level'
        )
    )

    # Add a line trace for 80% service level
    fig.add_trace(
        go.Scatter(
            x=[percentile_80, percentile_80],
            y=[0, max_hist_height],
            mode="lines",
            line=dict(color="Green", width=2, dash="dash"),
            name='80% Service Level'
        )
    )

    return fig

def create_service_level_priority_plot(df, priority):
    priority_passengers = df[df['Priority'] == priority]

    percentile_95 = np.percentile(priority_passengers['waitingTime'], 95)
    percentile_80 = np.percentile(priority_passengers['waitingTime'], 80)

    # Create a histogram using plotly express
    fig = px.histogram(
        priority_passengers, 
        x='waitingTime', 
        nbins=24, 
        opacity=0.7,
        title='Passenger Waiting Time Distribution with Service Levels' if priority == 1 else 'Normal Passenger Waiting Time Distribution with Service Levels',
        labels={'waitingTime': 'Waiting Time (minutes)'}
    )

    # Update the histogram's marker style
    fig.update_traces(marker=dict(color='blue', line=dict(color='black', width=1)), name='Waiting Time Distribution')

    # Calculate the maximum height of the histogram for percentile lines
    hist_data = np.histogram(priority_passengers['waitingTime'], bins=24)
    max_hist_height = max(hist_data[0])

    # Add a line trace for 95% service level
    fig.add_trace(go.Scatter(
        x=[percentile_95, percentile_95],
        y=[0, max_hist_height],
        mode="lines",
        line=dict(color="Red", width=2, dash="dash"),
        name='95% Service Level'
    ))

    # Add a line trace for 80% service level
    fig.add_trace(go.Scatter(
        x=[percentile_80, percentile_80],
        y=[0, max_hist_height],
        mode="lines",
        line=dict(color="Green", width=2, dash="dash"),
        name='80% Service Level'
    ))

    # Update layout
    fig.update_layout(
        yaxis_title='Number of Passengers',
        legend=dict(
            itemsizing='constant',
            orientation='h',
            xanchor='center',
            x=0.5,
            y=-0.3
        ),
        bargap=0.2
    )

    return fig

def select_waitingTime_interval(waiting_time_intervals, hours):
    index = int(hours / 900)
    select_interval = waiting_time_intervals[index]

    percentile_95 = np.percentile(select_interval, 95)
    percentile_80 = np.percentile(select_interval, 80)

    # Create a histogram using plotly express
    fig = px.histogram(
        x=select_interval,
        opacity=0.7,
        title='Waiting Time Distribution with Service Levels',
        labels={'x': 'Waiting Time (minutes)'}
    )

    # Update the histogram's marker style
    fig.update_traces(marker=dict(color='blue', line=dict(color='black', width=1)), name='Waiting Time Distribution')

    # Add shapes for percentile lines
    fig.add_shape(type='line',
                  x0=percentile_95, y0=0, x1=percentile_95, y1=1,
                  line=dict(color='Red', width=2, dash='dash'),
                  xref='x', yref='paper')

    fig.add_shape(type='line',
                  x0=percentile_80, y0=0, x1=percentile_80, y1=1,
                  line=dict(color='Green', width=2, dash='dash'),
                  xref='x', yref='paper')

    # Update layout
    fig.update_layout(
        yaxis_title='Number of Passengers',
        legend=dict(itemsizing='constant',
                    orientation='h',
                    xanchor='center',
                    x=0.5,
                    y=-0.3),
        plot_bgcolor='white',
        bargap=0.2
    )

    return fig
