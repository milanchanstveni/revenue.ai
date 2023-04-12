from dash import Dash
import dash_bootstrap_components as dbc
from layout import LAYOUT
from callbacks import *


app = Dash(external_stylesheets=[dbc.themes.MORPH])


app.layout = LAYOUT

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=5002
    )
