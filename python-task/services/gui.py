from dash import Dash
from gui.callbacks import *
from gui.layout import LAYOUT


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = LAYOUT

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=5002
    )
