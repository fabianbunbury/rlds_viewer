# layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from datasets import RL_data_sets

# Define options for the Data Set Dropdown
data_set_options = [
    {'label': key, 'value': value}
    for key, value in RL_data_sets.items()
]

# Define options for the Episode Dropdown
episode_options = [
    {'label': 'Set A', 'value': 1},
    {'label': 'Set B', 'value': 2},
    {'label': 'Set C', 'value': 3},
    {'label': 'Set D', 'value': 4},
    {'label': 'Set E', 'value': 5},
]

# Define the sidebar layout
sidebar = dbc.Col(
    [
        html.H2("Toolbar", className="display-6", style={'color': 'white'}),
        html.Hr(),
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Episode", style={'color': 'white'}),
                                dcc.Dropdown(
                                    id='episode-dropdown',
                                    options=episode_options,
                                    value=1,  # Default value
                                    clearable=False
                                ),
                            ],
                            width=12
                        )
                    ],
                    className="mb-3"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Data Set", style={'color': 'white'}),
                                dcc.Dropdown(
                                    id='data-set-dropdown',
                                    options=data_set_options,
                                    value='gs://gresearch/robotics/berkeley_cable_routing/0.1.0',  # Default value
                                    clearable=False
                                ),
                            ],
                            width=12
                        )
                    ],
                    className="mb-3"
                ),
            ]
        ),
    ],
    width=2,  # Sidebar occupies 2/12 of the row
    className="sidebar",
    style={
        'backgroundColor': '#0078f0',
        'padding': '20px',
        'height': '100vh',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'overflowY': 'auto'
    }
)

# Define the main content layout with a slider at the bottom
main_content = dbc.Col(
    [
        # Main Content Area
        dbc.Container(
            [
                dcc.Loading(
                    [
                        html.H1("Episode Viewer", className="text-center my-4"),
                        html.P('Instruction = None', id='language-instruction'),
                        html.Div(
                            id='columns-container',
                            className="horizontal-scroll",
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "overflowX": "auto",
                                "padding": "10px",
                                "whiteSpace": "nowrap",
                            },
                        ),
                    ],
                    overlay_style={"visibility": "visible", "opacity": 0.5},
                    custom_spinner=html.H2([
                        "Loading Episode Data",
                        dbc.Spinner(color="danger")
                    ]),
                ),
            ],
            fluid=True,
            style={'paddingTop': '20px', 'paddingBottom': '100px'}  # Extra padding for slider
        ),
    ],
    width=10,  # Main content occupies 10/12 of the row
    className="main-content",
    style={
        'backgroundColor': '#bbbdbf',
        'marginLeft': '16.666667%',  # 2/12 of the width for the sidebar
        'minHeight': '100vh',
        'paddingBottom': '100px'  # Ensure content doesn't hide behind the slider
    }
)

# Combine sidebar and main content into a single layout
layout = dbc.Container(
    dbc.Row(
        [
            sidebar,
            main_content,
        ]
    ),
    fluid=True,
    style={'padding': '0'}
)
