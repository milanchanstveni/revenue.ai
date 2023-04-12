from dash import (
    html,
    dash_table,
    dcc,
    callback,
    Output,
    Input,
    State
)
from pathlib import Path

from dataset import (
    read_file,
    read_url
)


@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'), prevent_initial_call=True, suppress_callback_exceptions=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        file_content = read_file(Path(list_of_names))
        layout = []

        # layout.append(
        #     dcc.Graph(
        #         figure={
        #             "data": file_content.iterrows(),
        #             "layout": {"title": "Graph 1"}
        #         }
        #     )
        # )

        layout.extend([
            html.Br(),
            html.Hr(),
            html.Br(),
            dash_table.DataTable(
                file_content.to_dict('records'),
                [{'name': i, 'id': i} for i in file_content.columns],
            )
        ])

        return html.Div(layout)


@callback(Output("output-data-link", "children"), [Input("url", "value")])
def output_text(value):
    if value:
        file_content = read_url(value)
        layout = []

        layout.extend([
            html.Br(),
            html.Hr(),
            html.Br(),
            dash_table.DataTable(
                file_content.to_dict('records'),
                [{'name': i, 'id': i} for i in file_content.columns],
            )
        ])

        return html.Div(layout)