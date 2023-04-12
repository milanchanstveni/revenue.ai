from dash import (
    html,
    dash_table,
    dcc,
    callback,
    Output,
    Input,
    State
)
import pandas as pd
import plotly.express as px
from pathlib import Path

from core.logging import LOG
from core.dataset import (
    read_file,
    validate_dataset
)


@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        file_content = read_file(Path(list_of_names))
        data = validate_dataset(file_content)
        layout = [html.H5(f'File: {list_of_names}')]

        layout.append(
            dash_table.DataTable(
                #file_content.to_dict('records'),
                data[0].to_dict('records'),
                [{'name': i, 'id': i} for i in file_content.columns]
            )
        )

        if len(data[1]) > 0:
            layout.append(html.Hr())
            layout.append(html.H4('Errors:', style={'color': 'red'}))
            layout.extend([html.P(error, style={'color': 'red'}) for error in data[1]])
        
        return layout
