from dash import (
    Dash,
    html,
    dash_table,
    dcc,
    callback,
    Output,
    Input
)
import pandas as pd
import plotly.express as px


LAYOUT = html.Div([
    html.H1(className='row', children='Revenue.AI RAI homework task.',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files'),
                '(CSV, XLSX, XLS)'
            ]),
            style={
                'width': '80%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'margin-left': '10%'
            },
            multiple=False,
            accept="text/csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
        html.Div(id='output-data-upload'),
    ]),
])