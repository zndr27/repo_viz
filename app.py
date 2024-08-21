import dagshub
from dagshub.common.api.repo import RepoAPI
from dagshub.data_engine.datasources import get_datasource

import dash
from dash import html, dcc, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from flask import Flask, request, jsonify

import git
from io import BytesIO
import multiprocessing as mp
import os
import pandas as pd
from pathlib import Path
import requests
import tempfile
import uuid

### from dtale.app import build_app
### from dtale.views import startup
### from dtale.global_state import cleanup

from sweetviz import analyze
from ydata_profiling import ProfileReport

from callbacks import init_callbacks
from layouts import init_layout

# Set the react version to support mantine
dash._dash_renderer._set_react_version("18.2.0")

# Bootstrap CSS
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME,
    dbc_css,
]

# Mantine CSS
external_stylesheets += [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

# Load the figure templates for bootstrap
load_figure_template(["bootstrap", "bootstrap_dark"])

# Dagshub logo
dagshub_logo = "https://dagshub.com/wp-content/uploads/2024/04/dagshab.svg"
dagshub_logo_simple = "https://dagshub.com/img/favicon.svg"

### # Create the dtale server
### dtale_server = build_app(reaper_on=False)
### 
### @dtale_server.route("/create-df", methods=["POST"])
### def create_df():
###     """
###     Create a dataframe instance in the dtale server.
###     """
###     data = request.json
### 
###     df = pd.read_json(data["dataframe"])
###     data_id = data.get("instance_id", None)
### 
###     if data_id is not None:
###         cleanup(data_id)
###     else:
###         data_id = str(uuid.uuid4())
###     
###     instance = startup(data_id=data_id, data=df, ignore_duplicate=True)
### 
###     return {"instance_id": instance._data_id}
### 
### # Run the dtale server
### dtale_process = mp.Process(
###     target=dtale_server.run, 
###     kwargs={"host": "0.0.0.0", "port": 8080},
### )
### dtale_process.start()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

init_layout(app)
init_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False, port=8051, host="localhost")
