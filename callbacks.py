from dagshub.auth import add_app_token
from dagshub.common.api.repo import RepoAPI
from dagshub.data_engine.datasources import (
    get_datasource,
    get_datasources,
)

import dash
from dash import callback, dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate

from dtale.views import startup
from dtale.global_state import cleanup

import git
import json
import os
from pathlib import Path
import requests
from sweetviz import analyze
import tempfile
from ydata_profiling import ProfileReport

from components import FileTree


def init_callbacks(app):
    """
    Initialize all the callbacks.
    """
    @app.callback(
        Output("file-tree-drawer", "opened"),
        Input("file-tree-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def file_tree_open(n_clicks):
        """
        Open the file tree drawer when the user clicks the button.
        """
        return True

    @app.callback(
        Output("loading-overlay", "visible"),
        #Input("loaded-window", "style"),
        Input("loading-state", "data"),
        prevent_initial_call=True,
    )
    #def show_loading_overlay(style):
    def show_loading_overlay(data):
        """
        Show the loading overlay when the user clicks the load button.
        """
        #if style["display"] == "block":
        #    return False
        #
        #elif style["display"] == "none":
        #    return True
        #
        #return False
        if data['loading']:
            return True
        else:
            return False

    app.callback(
        Output("loading-state", "data"),
        Input("load-button", "n_clicks"),
        prevent_initial_call=True,
    )(lambda x: {"loading": True})

    app.clientside_callback(
        """
        function updateLoadingState(n_clicks) {
            return true
        }
        """,
        Output("loading-overlay", "visible", allow_duplicate=True),
        Input("load-button", "n_clicks"),
        prevent_initial_call=True,
    )

    @app.callback(
        Output("login-alert", "hide"),
        Output("app-state", "data"),
        Output("login-window", "style"),
        Output("main-navbar", "style"),
        Output("initial-window", "style"),
        Input("login-button", "n_clicks"),
        State("login-token", "value"),
        State("app-state", "data"),
    )
    def login_to_dagshub(n_clicks, token, data):
        """
        Login to the Dagshub API.
        """
        if data['token'] is not None:
            add_app_token(data['token'])
            return (
                True,
                data,
                {"display": "none"},
                {"display": "block"},
                {"display": "block"},
            )

        if not token:
            raise PreventUpdate

        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            "https://dagshub.com/api/v1/user",
            headers=headers,
        )

        if response.status_code != 200:
            data |= {"token": None}
            return (
                False,
                data,
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
            )

        else:
            data |= {"token": token}
            add_app_token(token)
            return (
                True,
                data,
                {"display": "none"},
                {"display": "block"},
                {"display": "block"},
            )

    @app.callback(
        Output("loading-state", "data", allow_duplicate=True),
        Output("app-state", "data", allow_duplicate=True),
        Output("name-header", "children"),
        Output("file-tree", "children"),
        Output("initial-window", "style", allow_duplicate=True),
        Output("loaded-window", "style", allow_duplicate=True),
        Input("load-button", "n_clicks"),
        State("repo-dropdown", "value"),
        State("dataset-dropdown", "value"),
        State("app-state", "data"),
        State("loaded-window", "style"),
        prevent_initial_call=True,
    )
    def update_repo_state(n_clicks, repo_id, dataset_id, data, style):
        """
        Update the app state based on the search button click.
        """
        if not n_clicks:
            raise PreventUpdate

        if not repo_id or not dataset_id:
            data['update_success'] = False
            data['update_error'] = "Repo / Dataset not selected."
            return (
                {"loading": False},
                data,
                "",
                [],
                {"display": "block"},
                {"display": "none"},
            )
    
        repo_owner, repo_name = repo_id.split("/")

        if (
            repo_owner == data.get("repo_owner") 
            and repo_name == data.get("repo_name")
            and style["display"] == "block"
        ):
            raise PreventUpdate
    
        try:
            # Connect to the Dagshub Client
            repo = RepoAPI(repo_id)
            repo_info = repo.get_repo_info()
    
            # Get the entire dataset
            ds = get_datasource(repo_id, dataset_id)
            query_all = ds.all()
            df = query_all.dataframe
    
            # File tree
            tempdir = tempfile.TemporaryDirectory()
            files_path = Path(tempdir.name) / repo_id
            os.makedirs(files_path, exist_ok=True)
            repo_git = git.Repo.clone_from(repo_info.clone_url, files_path)
    
            # YData report
            ydata_profile = ProfileReport(df, title="Profiling Report")
            ydata_html = ydata_profile.to_html()
    
            # Sweetviz report
            sweetviz_report = analyze(df)
            sweetviz_report.show_html(
                str(files_path / "sweetviz_report.html"), 
                open_browser=False, 
                layout="vertical",
            )
            with open(files_path / "sweetviz_report.html", "r") as f:
                sweetviz_html = f.read()
    
            # Update app state on frontend
            data |= {
                "repo_owner": repo_owner, 
                "repo_name": repo_name,
                "dataset_id": dataset_id,
                "dataframe": df.to_json(orient="columns"),
                "ydata_html": ydata_html,
                "sweetviz_html": sweetviz_html,
            }
    
            req = requests.post(
                "http://localhost:8080/create-df",
                json=data,
            )

            data |= req.json()
            data['update_success'] = True

        except Exception as e:
            data['update_success'] = False
            data['update_error'] = str(e)
            return (
                {"loading": False},
                data,
                "",
                [],
                {"display": "block"},
                {"display": "none"},
            )
    
        return (
            {"loading": False},
            data, 
            repo_info.full_name, 
            FileTree(files_path).render(),
            {"display": "none"},
            {"display": "block"},
        )
    
    
    @app.callback(
        Output("repo-dropdown", "options"),
        Input("repo-dropdown", "search_value"),
        State("app-state", "data"),
    )
    def update_repo_options(value, data):
        """
        List repositories based on search bar input.
        """
        if not value:
            raise PreventUpdate

        headers = {"Authorization": f"Bearer {data['token']}"}
    
        response = requests.get(
            f"https://dagshub.com/api/v1/repos/search?q={value}&uid=0&limit=50&page=1",
            headers=headers,
        )
    
        return [x.get("full_name") for x in response.json().get("data")]


    @app.callback(
        Output("dataset-dropdown", "options"),
        Input("repo-dropdown", "value"),
    )
    def update_dataset_options(value):
        """
        List datasets based on the selected repository.
        """
        if not value:
            raise PreventUpdate
    
        repo_owner, repo_name = value.split("/")
    
        ds_list = get_datasources(value)
    
        return [x._source.name for x in ds_list]
    
    
    #@app.callback(
    #    Output("mantine-provider", "forceColorScheme"),
    #    Input("color-mode-switch", "value"),
    #)
    #def update_mantine_color_scheme(switch_on):
    #    """
    #    Switch between light and dark mode for dash mantine components.
    #    """
    #    return "light" if switch_on else "dark"
    #
    #
    ## Clientside callback to toggle dash bootstrap dark mode
    #app.clientside_callback(
    #    """
    #    (switchOn) => {
    #       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
    #       return window.dash_clientside.no_update
    #    }
    #    """,
    #    Output("color-mode-switch", "id"),
    #    Input("color-mode-switch", "value"),
    #)
    
    
    # TODO add callback for our own gittruck like files visualizer
    @app.callback(
        Output("window-1", "children"),
        Input("ydata-button", "n_clicks"),
        Input("sweetviz-button", "n_clicks"),
        Input("dtale-button", "n_clicks"),
        State("app-state", "data"),
    )
    def update_active(n0, n1, n2, data):
        """
        Update the active window based on the button clicked.
        """
        ctx = dash.callback_context
    
        if not ctx.triggered:
            return html.Div(
                style={
                    "width": "100%", 
                    "height": "100%",
                    "background-color": "white",
                },
            )
    
        else:
    
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
            if button_id == "ydata-button":
                return html.Iframe(
                    srcDoc=data["ydata_html"],
                    style={"width": "100%", "height": "100%"},
                )
    
            elif button_id == "sweetviz-button":
                return html.Iframe(
                    srcDoc=data["sweetviz_html"],
                    style={"width": "100%", "height": "100%"},
                )
    
            elif button_id == "dtale-button":
                return html.Iframe(
                    src=f"http://localhost:8080/dtale/main/{data['instance_id']}",
                    width="100%",
                    height="100%",
                )
    
            else:
                raise Exception(f"Invalid button id: {button_id}")
