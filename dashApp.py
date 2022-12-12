import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash

from graphMaker import getPostVolumeGraph, getSentimentGraph

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout =  dbc.Container(children=[
	dbc.Row([
		dbc.Col(html.Img(src="assets/infegyLogo.png", style={'width':'100%', "float": "left"}), width=2),
		dbc.Col(dbc.Row([dbc.Col(html.H1(children=['Infegy Top Brands of 2022']), width=8),
				dbc.Row(html.H3(children=['Analyzing the Top US Companies'])) 
			]), align="center")
	], justify='start'),


	dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

	dbc.Row([
		dbc.Col(dcc.Graph(figure=getPostVolumeGraph())),
		dbc.Col(dcc.Graph(figure=getSentimentGraph())),
		])

], fluid = True)

app.title = 'Infegy Top Brands' 


if __name__ == '__main__':
	app.run_server(debug=True)