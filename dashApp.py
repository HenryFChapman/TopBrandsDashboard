import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash

from graphMaker import getPostVolumeGraph, getSentimentGraph

#load entities
entities = pd.read_csv("entities.csv", encoding = 'utf-8')


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Infegy Top Brands' 

app.layout =  dbc.Container(children=[
	dbc.Row([
		dbc.Col(html.Img(src="assets/infegyLogo.png", style={'width':'100%', "float": "left"}), width=2),
		dbc.Col(dbc.Row([dbc.Col(html.H1(children=['Infegy Top Brands of 2022']), width=8),
				dbc.Row(html.H3(children=['Analyzing the Top US Companies'])) 
			]), align="center")
	], justify='start'),


	html.Label(['Pick a top brand:'],style={'font-weight': 'bold'}),
	dcc.Dropdown(entities['EntityName'].tolist(), value = 'Apple', id='dropdown',),

	dbc.Row([
		dbc.Col(dcc.Graph(id='postVolume')),
		#dbc.Col(dcc.Graph(figure=getPostVolumeGraph())),
		dbc.Col(dcc.Graph(id='sentimentGraph')),
		])

], fluid = True)

@app.callback(
	Output('postVolume', 'figure'),
    [Input(component_id='dropdown', component_property='value')]
	)

def select_graph(value):
	fig = getPostVolumeGraph(value)
	return fig


@app.callback(Output('sentimentGraph', 'figure'),
              Input(component_id='dropdown', component_property='value'))
def update_graph_b(value):
	fig = getSentimentGraph(value)
	return fig


if __name__ == '__main__':
	app.run_server(host="0.0.0.0", port="8050")
	#app.run_server(debug=True)