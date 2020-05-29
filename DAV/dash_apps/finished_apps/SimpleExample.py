import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import base64
import datetime
import os
import io
import dash_table
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import plotly.graph_objs as go
import plotly.express as px
import glob
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
server = Flask(__name__)
app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


data = os.listdir('./media/files/file/')
path = './media/files/file/'
df2 = pd.concat(map(pd.read_csv, glob.glob(path +'/*.csv')))

visualization_operation = ['Scatter','Histogram','Bubble','3D']
#Banner Creator
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Wadav"),
                    html.H4(data),
                ],
            ),
        ],
    )

app.layout = html.Div([
    build_banner(),
    html.Div(children=[
    	dcc.Tabs(
        	id="tabsID",
        	children=[
    		dcc.Tab(label='Your Data',
    					 children=[
                            html.Div(

                                dash_table.DataTable(
                                    data=df2.to_dict('records'),
                                    columns=[{'name': i, 'id': i} for i in df2.columns]
                                    ),
                                ),
                         ]),


    		dcc.Tab(label='Data Visualization',
    					 children=[
                            html.Div([
                                html.H5("Operation"),
                                dcc.Dropdown(id='operation',options=[{'label': i, 'value': i} for i in visualization_operation]),
                            ]),

                            html.Div([
                                html.H5("First Element"),
                                dcc.Dropdown(
                                    id='firstEnement',
                                    options=[{'label': i, 'value': i} for i in df2.columns],
                                ),
                                ],
                            style={'width': '33%', 'display': 'inline-block'}
                            ),
                            html.Div([
                                html.H5("Second Element"),
                                dcc.Dropdown(
                                    id='secondElement',
                                    options=[{'label': i, 'value': i} for i in df2.columns],
                                    multi=True
                                ),
                                #RadioItems ı tek bir tane olarak html div altında al
                            ],
                            style={'width': '33%', 'display': 'inline-block'}
                            ),
                            html.Div([
                                html.H5("Third Element"),
                                dcc.Dropdown(
                                    id='thirdElement',
                                    options=[{'label': i, 'value': i} for i in df2.columns],
                                ),
                                ],
                            style={'width': '33%', 'display': 'inline-block'}
                            ),
                            html.Div([
                                html.H5("Filter"),
                                dcc.Dropdown(id='filter',options=[{'label': i, 'value': i} for i in df2.columns]),
                            ]),

                            dcc.Graph(id='visualization_output'),

                            dcc.Slider(
                                id='my-slider',
                                min=0,
                                max=len(df2.index)-1,
                                step=1,
                                value=100
                            ),

                         ]),

    		],

    	)
    ]),

])




@app.callback(
    Output('visualization_output', 'figure'),
    [Input('operation', 'value'),
    Input('firstEnement', 'value'),
    Input('secondElement', 'value'),
    Input('thirdElement', 'value'),
    Input('filter', 'value'),
    Input('my-slider', 'value')
    ])
def update_output(operation,value,value2,value3,filter,range):
    dff = df2.iloc[:range:]
    traces = []
    if operation == 'Scatter':

        for i in value2:
            traces.append(dict(
                x=dff[value],
                y=dff[i],
                mode = "lines+markers",
                name = "{}".format(i),
                marker = dict(color = 'rgba(16* i.index(), 112* i.index(), 2* i.index(), 0.8)'),
                text= dff[filter].unique()
            ))


        return {
            'data':traces,
            'layout' : dict(
                xaxis={'type': 'log', 'title': value},
                yaxis={'title': value2},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition = {'duration': 500},
            )
        }
    elif operation == 'Histogram':
        for i in value2:
            traces.append(dict(
                x=dff[value],
                y=dff[i],
                type = 'bar',
                name = "{}".format(i),
                marker = dict(color = 'rgba(16* i.index(), 112* i.index(), 2* i.index(), 0.8)'),
                text= dff[filter].unique()
            ))
        return {
            'data':traces,
            'layout' : dict(
                xaxis={'title': value},
                yaxis={'title': value2},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition = {'duration': 500},
            )
        }
    elif operation == 'Bubble':
        for i in value2:
            traces.append(dict(
                x=dff[value],
                y=dff[i],
                mode = "markers",
                name = "{}".format(i),
                marker = {'color' : 'rgba(16* value.index(), 112* value.index(), 2* value.index(), 0.8)',
                          'size' : dff[value3],
                          'showscale' : True},
                text= dff[filter].unique()
            ))


        return {
            'data':traces,
            'layout' : dict(
                xaxis={'type': 'log', 'title': value},
                yaxis={'title': value2},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition = {'duration': 500},
            )
        }
    elif operation == '3D':
        for i in value2:
            trace = go.Scatter3d(
                x=dff[value],
                y=dff[i],
                z=dff[value3],
                mode="markers",
                marker=dict(
                    size=10,
                    symbol="circle",
                    color="rgb(255,0,0)",
                    opacity=0.8,
                ),
                text= dff[filter].unique())



            layout = go.Layout(
                margin = dict(
                l=0,
                r=0,
                b=0,
                t=0,
                ),

            )
            fig = go.Figure(data=[trace],layout=layout)

            return fig

    else:
        return {
            'data':traces,
            'layout' : dict(
                xaxis={'type': 'log', 'title': value},
                yaxis={'title': value2},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition = {'duration': 500},
            )
        }








if __name__ == '__main__':
    app.run_server(debug=True)
