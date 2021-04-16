 # Run with python index.py and
# visit http://127.0.0.1:8050/ browser

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# creat app
app = dash.Dash()

# html output
app.layout = html.Div (children=[
    html.H1(children='Hello World'),
    html.P(children='Lorem Ipsum')
])

# on production server change debug to false
if __name__ == '__main__':
    app.run_server(debug=True)
