from dash import (
    html,
    dcc
)
import dash_bootstrap_components as dbc


tab1 = html.Div([
    html.Br(),
    html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files'),
            '(CSV, XLSX, XLS)'
        ]),
        style={
            'width': '120%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'margin-left': '40%'
        },
        multiple=False,
        accept="text/csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ),
    html.Div(id='output-data-upload'),
])


tab2 = html.Div([
    html.Br(),
    html.Br(),
    dbc.Input(
        type='url',
        id='url',
        placeholder='Insert URL of dataset.',
        style={'width': '120%', 'margin-left': '40%'}
    ),
    html.Div(id='output-data-link'),
])


LAYOUT = html.Div([
    html.H1(className='text-center', children='Revenue.AI Plotly-Dash task.'),
    
    html.Div([
        html.H6('Choose a way to import dataset.', className='text-center'),

        dbc.Tabs([
            dbc.Tab(tab1, label='Upload File', style={'width': '50%'}),
            dbc.Tab(tab2, label='Provide Link', style={'width': '50%'})
        ]),
        #], style={'margin-left': '40%', 'width': '100%'})
    ], style={'margin-left': '10%', 'width': '80%'},),

    # html.Div(className='row', children=[
    #     dcc.Upload(
    #         id='upload-data',
    #         children=html.Div([
    #             'Drag and Drop or ',
    #             html.A('Select Files'),
    #             '(CSV, XLSX, XLS)'
    #         ]),
    #         style={
    #             'width': '80%',
    #             'height': '60px',
    #             'lineHeight': '60px',
    #             'borderWidth': '1px',
    #             'borderStyle': 'dashed',
    #             'borderRadius': '5px',
    #             'textAlign': 'center',
    #             'margin': '10px',
    #             'margin-left': '10%'
    #         },
    #         multiple=False,
    #         accept="text/csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     ),
    #     html.Div(id='output-data-upload'),
    ])