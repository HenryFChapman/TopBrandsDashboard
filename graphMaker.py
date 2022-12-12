import plotly.express as px
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def hoverLabel():
    hoverLabelDict = dict(bgcolor="white",
        font_color="darkslategrey",
        font_family="Roboto",
        font_size=13,
        bordercolor= 'rgb(255,0,0, 0)',
        )

    return hoverLabelDict

def xaxisLayout(df):
    xAxisDict = dict(
          title = ' ',
          showgrid = True,
          zeroline = True,
          showline = True,
          showticklabels = True,
          showspikes= True,
          spikemode= 'across+toaxis',
          spikedash= "solid",
          spikecolor="#65A2CC",
          spikethickness= 2,
          gridwidth = 1,
          linecolor='#C2C8D6',
          tickvals=[df['Date'].tolist()[0], df['Date'].tolist()[-1]],
          fixedrange = True,
          )
    return xAxisDict

def getGraphLayout(fig, graphTitle, df):

    fig.update_layout(
        font_family="Roboto",
        font_color="darkslategrey",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_text=graphTitle, 
        title_x=0.5,
        font=dict(size=18),
        xaxis = xaxisLayout(df),
        hovermode='x',
        hoverlabel=hoverLabel()
        )

    return fig

    #fig.update_layout()


def getSentimentGraph():

    df = pd.read_excel("House Of The Dragon - sentiment.xlsx")
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Net Sentiment'],
        line_shape='spline',
        line_color="#75C1B3",
        showlegend = False
        ))

    fig.add_hline(y=0, line_dash="dot",
              annotation_text="Negative Sentiment", 
              annotation_position="bottom right")
    fig.add_hline(y=0, line_dash="dot",
              annotation_text="Positive Sentiment", 
              annotation_position="top right")

    fig.add_hrect(y0=0, y1=-.25, line_width=0, fillcolor="red", opacity=0.1)
    fig.add_hrect(y0=0, y1=1, line_width=0, fillcolor="green", opacity=0.1)

    fig = getGraphLayout(fig, "Net Sentiment", df)

    fig.update_yaxes(title_text="Net Sentiment", secondary_y=False)

    return fig


def getPostVolumeGraph():
    df = pd.read_excel("Inflation - volume.xlsx")
    df = df[df['Date']> "1/1/2022"]

    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Universe"],
        line_shape='spline', 
        mode='lines+markers', 
        marker_symbol='circle',
        marker_color = 'white',
        marker = dict(line = dict(color= "#75C1B3", width = 2))), secondary_y=False,)
    fig.data[0].line.color = "#75C1B3"

    fig = getGraphLayout(fig, "Post Volume", df)

    fig.update_yaxes(title_text="Post Volume", secondary_y=False)

    return fig
