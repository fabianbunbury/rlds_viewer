# app.py

import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Initialize the Dash app with a Bootstrap stylesheet for better styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the layout
app.layout = layout

# Register callbacks
register_callbacks(app)

# Run the Dash app
if __name__ == "__main__":
    app.run_server()