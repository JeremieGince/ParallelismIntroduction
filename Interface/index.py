from dash import dcc
from dash import html
import dash
from callbacks import *
from app import app
from app import server
from layouts import *

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='store-trajectory', storage_type='session'),
    # dcc.Store(id='store-trajectory-fig')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), State('store-trajectory', 'data')])
def display_page(pathname: str, trajectory: str):
    """
    This callback function allows the user to display different webpages based on the url.
    :param trajectory:
    :param pathname: A string for the relative url
    :return:
    """
    if pathname == menu_pathname:
        return page1
    else:
        return Error_404


if __name__ == '__main__':
    app.run_server(debug=True)