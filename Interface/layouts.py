from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from app import app

menu_pathname = '/'



def make_header():
    """
    This function generates the header of the webpage
    """
    header = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.H1(children='Parallélisme //',
                            style={'textAlign': 'center'}),
                    width={'size': 8, 'offset': 2},
                    lg={'size': 3, 'offset': 4},
                    xl={'size': 4, 'offset': 4}
                ),
                dbc.Col(
                    html.Img(
                        src=app.get_asset_url('logo.png'),

                        style={"height": "10vh", },
                    ),
                    width={'size': 2, 'offset': 0},
                    md={'size': 2, 'offset': 0},
                    lg={'size': 1, 'offset': 3},
                    xl={'size': 1, 'offset': 1}
                ),

            ],
            align="center",
            className="h-75 bg-primary border border-light rounded-3"
        ),
    ],
        style={"height": "20vh", 'width': "100vw", 'zIndex': 999}  # 'margin-bottom': '2em'},
    )

    return header


Error_404 = html.Div(
    [
        html.H1("Error 404", className="text-danger"),
        html.Hr(className="my-2"),
        html.P(
            "The page you are trying to view doesn't exist.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        dbc.Button(
            'Back to home page',
            id='error404-button',
            color='primary',
            href=menu_pathname
        )
    ],
    className="h-100 p-5 bg-light border rounded-3",
)
####################################################################
# Page 1 Layout
####################################################################


def dashboard():
    """
    This function makes a dashboard controlling the figure
    :param longitudinal_dataframe:
    :return:
    """
    sensor_checklist = html.Div(
        [
            dbc.Label("Senseurs météo :"),
            dbc.Checklist(
                options=[
                    {"label": "Température", "value": 0},
                    {"label": "Vent", "value": 1},
                ],
                value=[],
                id="sensor-checklist-input",
                inline=True,
            ),
        ]
    )
    range_slider_days = html.Div(
        [
            dbc.Label("Jours affichés:"),
            dcc.RangeSlider(0, 30, marks=None, value=[10, 15],
                            tooltip={"placement": "bottom", "always_visible": True})
        ]
    )
    dashboard_card = dbc.Card([
        dbc.CardHeader(
            html.H5('Sélecteur de données', className="card-title")
        ),
        dbc.CardBody(
            [
                dbc.Row(sensor_checklist),
                html.Hr(),
                dbc.Row(range_slider_days)
            ],

        )
    ],
        color='secondary',
        # className="w-200"
    )
    return dashboard_card


def make_figure_and_dashboard():
    """
    This function generates the scatter plot and the dashboard controlling it
    :param trajectory: The trajectory object
    :return:
    """
    figure = go.Figure(
        go.Scatter(x=[0], y=[0])
    )
    figure_dashboard = dbc.Row(
        [
            dbc.Col(
                dashboard(),
                width={'offset': 0, 'size': 2},
            ),
            dbc.Col(
                dcc.Graph(figure=figure,
                          id="main-scatter",
                          # style={'height': '100%', 'width': '110%'}
                          ),
                width={'size': 10, 'offset': 0},
            )
            # style={'height': '60vh'}
        ],
        # style={
        #     "margin-left": "12rem",
        #     "margin-right": "2rem",
        #     # "margin-top": "-7rem",
        # },
        )
        # className="h-75"
    return figure_dashboard



page1 = html.Div([
    # Row 1
    dbc.Row(make_header()),
    # Row 2
    dbc.Row(make_figure_and_dashboard()),
    # # Row 3 loading state
    # dbc.Row(dbc.Col(make_loading_spinner(), width={'size': 2, 'offset': 5}), style={'margin-top': '1.5em'})
], )
