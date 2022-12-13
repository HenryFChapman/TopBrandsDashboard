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
entities = pd.read_excel("entities.xlsx")
descriptionDict = dict(zip(entities.EntityName, entities.WikiDescrip))

app = dash.Dash(__name__,
	external_stylesheets=[dbc.themes.BOOTSTRAP],
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)
app.title = 'Infegy Top Brands' 

app.layout =  dbc.Container(children=[
	#Header
	dbc.Row([
		dbc.Col(html.Img(src="assets/infegyLogo.png", style={'width':'100%', "float": "left", 'margin' : '5px',}), width=2),
		dbc.Col(dbc.Row([dbc.Col(dbc.Row(html.H2(children=["Infegy's Top Brands of 2022"])), width=10),
									dbc.Row(html.H3(children=["Analyzing the World's Top Companies"])) 
			]), align="center", style={'margin' : '15px',})
	], justify='start'),

	dbc.Row([
		dcc.Dropdown(entities['EntityName'].tolist(), value = 'Apple', id='dropdown', clearable=False, style={'margin-bottom':'5px'})
	]),

	dbc.Row([
		dbc.Col([

				dbc.Row(html.H4(children=['Sample Text'], id='textTitle')),
				dbc.Row(html.P(children=["sample text"], id='paragraph')),
				dbc.Row(html.Img(src="assets/logos/Apple.png",style={'height':'40%', 'width':'40%', 'margin' : '10px',}, id='corporateLogo')),

				]
			),
		dbc.Col(dcc.Graph(id='postVolume'), lg=6, width=12),
		]),

	dbc.Row([
		dbc.Col(dcc.Graph(id='sentimentGraph')),
		]),
])

@app.callback(
	Output('postVolume', 'figure'),
    [Input(component_id='dropdown', component_property='value')]
	)
def select_graph(value):
	fig = getPostVolumeGraph(value)
	return fig

@app.callback(
	Output('sentimentGraph', 'figure'),
	Input(component_id='dropdown', component_property='value'))
def update_graph_b(value):
	fig = getSentimentGraph(value)
	return fig

@app.callback(
	Output('textTitle', 'children'),
	Input(component_id='dropdown', component_property='value'))
def update_ticker_header(value):
    return [html.H4(value)]

@app.callback(
	Output('paragraph', 'children'),
	Input(component_id='dropdown', component_property='value'))
def update_ticker_header(value):
    return [html.P(descriptionDict.get(value))]

@app.callback(
	Output('corporateLogo', 'src'),
	Input(component_id='dropdown', component_property='value')
	)
def update_ticker_header(value):
	return "assets/logos/" + value + ".png"

if __name__ == '__main__':
	app.run_server(host="0.0.0.0", port="8050", debug = True)
	#app.run_server(debug=True)