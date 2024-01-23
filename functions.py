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
    # 将 ArrivalTime 从秒转换为小时
    arrival_times_in_hours = arrival_df['ArrivalTime'] / 3600

    # 创建直方图
    hist_data = go.Histogram(
        x=arrival_times_in_hours,
        nbinsx=24,  # 将一天分为24个小时
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

    # 创建图表对象
    fig = go.Figure(data=[hist_data])

    # 更新图表布局
    fig.update_layout(
        title_text='Distribution of Passenger Arrival Times',  # 标题
        xaxis_title_text='Time of Day (Hours)',  # X轴标题
        yaxis_title_text='Number of Passengers',  # Y轴标题
        bargap=0.2,  # 直方图条间距
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,  # 每1小时一个刻度
        ),
        plot_bgcolor='white'  # 背景颜色
    )

    # 添加网格线
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

    return fig

import plotly.graph_objs as go

import plotly.graph_objs as go

def create_time_interval_plot(df):
    fig = go.Figure()

    # 添加第一个时间序列
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Waiting Time'],
        mode='markers+lines',
        name='Average Waiting Time',  # 用于图例的标签
        marker=dict(color='blue', size=7)
    ))

    # 添加第二个时间序列
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Virtual Queue Waiting Time'],
        mode='markers+lines',
        name='Average Virtual Queue Waiting Time',
        marker=dict(color='red', size=7)
    ))

    # 添加第三个时间序列
    fig.add_trace(go.Scatter(
        x=df['Time in hour'],
        y=df['Average Normal Queue Waiting Time'],
        mode='markers+lines',
        name='Average Normal Queue Waiting Time',
        marker=dict(color='green', size=7)
    ))

    # 更新图表布局
    fig.update_layout(
        title='Average Waiting Time at Security Check (per 15-minute Interval)',
        xaxis_title='Time Interval',
        yaxis_title='Average Waiting Time (second)',
        xaxis=dict(tickangle=45),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        showlegend=True  # 显示图例
    )

    return fig
