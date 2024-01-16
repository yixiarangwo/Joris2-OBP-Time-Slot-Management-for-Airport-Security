import io
import base64
import numpy as np
import pandas as pd
import sympy as sp
from latex2sympy2 import latex2sympy
from dash import Dash, dcc, html, Input, Output, callback

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
