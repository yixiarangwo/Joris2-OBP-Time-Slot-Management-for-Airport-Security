from dash import Dash, dcc, html, Input, Output, State, callback, ctx,dash_table
from latex2sympy2 import latex2sympy
import plotly.figure_factory as ff
import numpy as np

from functions import *

from simulation import *

############################################ Importables tab ############################################
# Combined callback for preventing multiple outputs of simulated service times.
# Callback is called if arrival data is uploaded or if submit button for service dist is pressed.
# Available arrival data will be converted to pandas dataframe and stored.
# If both arrival data and service distribution are known, service times are sampled.
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "arrivals"},    "data"),
    Output({"section": "intermediate", "type": "dataframe", "index": "sim-service"}, "data"),
    
    Input({ "section": "importables",  "type": "upload",    "index": "arrivals"},    "contents"),
    Input({ "section": "importables",  "type": "button",    "index": "server-dist"}, "n_clicks"),
    State({ "section": "importables",  "type": "input",     "index": "server-dist",  "info": "formula"}, "value"),
    prevent_initial_call = True
)
def serviceTimes(contents, n_clicks, latexExpression):
    # Parse content to dataframe of arrivals if triggered by file upload
    trigger_id = ctx.triggered_id
    if contents is not None and trigger_id["index"] == "arrivals":
        arrivals = parseContents(contents)          # ADD SHOWING FILE NAME AS CONFIRMATION OF UPLOADING (in separate callback)
        
    # Sample from given distribution if server dist. and arrival data given
    simService = ''
    #if latexExpression != '' and arrivals is not None:
    #    samples = arrivals.shape[0]
    #    npFunc = latexToNumpy(latexExpression)
    #    simService = 0

    return arrivals, simService

# Uploading flight schedule and converting to pandas dataframe
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "flights"}, "data"),
    Input({ "section": "importables",  "type": "upload",    "index": "flights" }, "contents"),
    prevent_initial_call = True
) 
def storeFlights(contents):
    if contents is None:
        raise dash.exceptions.PreventUpdate
    return parseContents(contents, "records")   # ADD SHOWING FILE NAME AS CONFIRMATION OF UPLOADING

# Uploading lane availability data and converting to pandas dataframe
@callback(
    Output({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    Input({ "section": "importables",  "type": "upload",    "index": "lanes"}, "contents"),
    prevent_initial_call = True
) 
def storeLanes(contents):
    if contents is None:
        raise dash.exceptions.PreventUpdate
    return parseContents(contents)          # ADD SHOWING FILE NAME AS CONFIRMATION OF UPLOADING

# Update LaTeX version of inputted distribution live
@callback(
    Output({"section": "importables", "type": "text",  "index": "server-dist"}, "children"),
    Input({ "section": "importables", "type": "input", "index": "server-dist", "info": "formula"}, "value"),
    State({ "section": "importables", "type": "text",  "index": "server-dist"}, "children")
)
def showLaTeX(latexExpression, prevExpression):
    # Check if no expression
    if latexExpression == '':
        return ''
    
    # Make complete LaTeX math expression
    latexMath = "$$f_S(x) = " + latexExpression + "$$"

    # Check if correct LaTeX:
    try:
        latex2sympy(latexExpression)
        return latexMath
    except Exception as e:
        return prevExpression

# Update plot of sampled service times when dataframe changed
#@callback(
    #Output({"section": "importables",  "type": "graph",     "index": "sim-service"}, "figure"),
#    Input({ "section": "intermediate", "type": "dataframe", "index": "sim-service"}, "data"),
#    prevent_initial_call = True
#)
#def plotServiceTimes(simService):
    # Set times in proper form
    #if len(simService.shape) == 1:
    #    simService = simService[:, np.newaxis]

    # Get fig data
    #fig = ff.create_distplot([simService], ["Security Times"])

    # Set layout of plot
  
    #return None #fig


############################################ Inputs tab ############################################
@callback(
    Output({"section": "inputs",       "type": "table",     "index": "time-slots"}, "data"),
    Output({"section": "inputs",       "type": "table",     "index": "time-slots"}, "editable"),
    Input({ "section": "intermediate", "type": "dataframe", "index": "flights"},    "data"),
    prevent_initial_call = True
)
def timeSlotRows(flights):
    data = [record.copy() for record in flights]
    [record.update({"TimeSlotCapacity": "", "TimeSlotIntervals": ""}) for record in data]
    return data, True


# use MATCH (or the other one) to get all time slots in one go upon callback when submit button is pressed


############################################ Analysis tab ############################################
@callback(
    Output('average-waiting-time-output', 'children'),
    Output('average-Virtua-waiting-time-output', 'children'),
    Output('average-Normal-waiting-time-output', 'children'),
    Output('waiting-time-plot-output', 'figure'),
    Input('run-simulation-button', 'n_clicks'),
    State({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "lanes"}, "data"),
    State({"section": "intermediate", "type": "dataframe", "index": "flights"}, "data"),
    prevent_initial_call = True
)
def update_dashboard(n_clicks, passengers_data_json, security_data_json,flights_data_json):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    
    passengers_data = pd.DataFrame(passengers_data_json)
    security_data = pd.DataFrame(security_data_json)
    flights_data =pd.DataFrame(flights_data_json)
    passengers_data = pd.merge(passengers_data, flights_data, left_on='FlightNumber', right_on='FlightNumber', how='left')
    passengers_data = process_virtual_queue(passengers_data, virtual_queue).sort_values(by='new_ArrivalTime')
    
    #run simulation
    simulation_result_df = multiple_run_simulation(5,40000, passengers_data, security_data)
    print(simulation_result_df)
    simulation_result_df["Time in hour"] = simulation_result_df.index/3600
    non_zero_values = simulation_result_df[simulation_result_df['Average Waiting Time'] != 0]
    non_zero_count = non_zero_values['Average Waiting Time'].count()
    average_waiting_time = non_zero_values['Average Waiting Time'].sum() / non_zero_count
    average_waiting_time_str = f"Average Waiting Time: {average_waiting_time:.2f} seconds"
    
    non_zero_values_Virtual = simulation_result_df[simulation_result_df['Average Virtual Queue Waiting Time'] != 0]
    non_zero_count_Virtual = non_zero_values['Average Virtual Queue Waiting Time'].count()
    average_Virtual_waiting_time= simulation_result_df['Average Virtual Queue Waiting Time'].sum()/non_zero_count
    average_Virtual_waiting_time_str = f"Average Virtual Waiting Time: {average_Virtual_waiting_time:.2f} seconds"
    
    non_zero_values_Normal = simulation_result_df[simulation_result_df['Average Normal Queue Waiting Time'] != 0]
    non_zero_count_Normal = non_zero_values['Average Normal Queue Waiting Time'].count()
    average_Normal_waiting_time=simulation_result_df['Average Normal Queue Waiting Time'].sum()/non_zero_count
    average_Normal_waiting_time_str =  f"Average Normal Waiting Time: {average_Normal_waiting_time:.2f} seconds"
    
    plot_fig = create_time_interval_plot(simulation_result_df)

    return average_waiting_time_str,average_Virtual_waiting_time_str,average_Normal_waiting_time_str,plot_fig


@callback(
    Output('arrival-time-distribution-plot', 'figure'),
    Input({"section": "intermediate", "type": "dataframe", "index": "arrivals"}, "data"),
    prevent_initial_call=True
)
def update_arrival_time_plot(arrival_data):
    try:
        if not arrival_data:
            return {}

        arrival_df = pd.DataFrame(arrival_data)
        
        fig = create_plotly_histogram(arrival_df)
        return fig
    except Exception as e:
        print(f"Error in update_arrival_time_plot: {e}")
        return {}

    
