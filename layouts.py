from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

# Dagshub logo
dagshub_logo = "https://dagshub.com/wp-content/uploads/2024/04/dagshab.svg"
dagshub_logo_simple = "https://dagshub.com/img/favicon.svg"


app_state = dcc.Store(
  id="app-state", 
  storage_type="session",
  data={
      "description": "app state",
      "token": None,
  },
)

loading_state = dcc.Store(
    id="loading-state",
    storage_type="memory",
    data={
        "loading": False,
    },
)


color_mode_switch = html.Span(
  [
    dbc.Label(
      className="fa fa-moon",
      html_for="color-mode-switch",
      style={"color": "white"},
    ),
    dbc.Switch(
      id="color-mode-switch",
      value=True,
      className="d-inline-block ms-1",
      persistence=True,
    ),
    dbc.Label(
      className="fa fa-sun",
      html_for="color-mode-switch",
      style={"color": "white"},
    ),
  ]
)


file_tree = dmc.Grid(
  [
    dmc.GridCol(
      id="file-tree",
      style={
        "overflow": "auto",
      },
    ),
  ],
  gutter=0,
)

eda_options = dmc.Group(
  [
    dmc.Button("Files", id="file-tree-button",),
    dmc.Button("Dtale", id="dtale-button"),
    dmc.Button("Sweetviz", id="sweetviz-button"),
    dmc.Button("YData", id="ydata-button"),
  ],
  justify="center",
)

navbar = html.Div(
  dmc.Grid(
    [
      dmc.GridCol(
        html.Div(
          [
            # Change height depending on breakpoint
            html.Img(
              src=dagshub_logo_simple, 
              height="40px",
            ),
            html.Div(
              "RepoViz", 
              style={"paddingLeft": "10px"},
            ),
          ],
          # Align side by side
          style={
            "display": "flex",
            "align-items": "left",
            "color": "white",
            "font-family": "monospace",
            "font-weight": "bold",
            "font-size": "1.5em",
          },
        ),
        offset={
          "xs": 1, "sm": 0, "md": 1, "lg": 1, "xl": 1,
        },
        span={
          "xs": 11, "sm": 2, "md": 2, "lg": 2, "xl": 2,
        },
      ),
      dmc.GridCol(
        html.Div(
          [
            html.Div(
              "Repository",
              style={
                "color": "white",
                "font-family": "monospace",
                "font-weight": "bold",
              },
            ),
            dcc.Dropdown(
              placeholder="Search for a repository",
              id="repo-dropdown",
              className="dbc",
            ),
          ],
        ),
        span={
          "xs": 5, "sm": 4, "md": 4, "lg": 4, "xl": 4,
        },
        offset={
          "xs": 1, "sm": 0, "md": 0, "lg": 0, "xl": 0,
        },
      ),
      dmc.GridCol(
        html.Div(
          [
            html.Div(
              "Dataset",
              style={
                "color": "white",
                "font-family": "monospace",
                "font-weight": "bold",
              },
            ),
            dcc.Dropdown(
              placeholder="Dataset Selection",
              id="dataset-dropdown",
              className="dbc",
            ),
          ],
        ),
        span={
          "xs": 5, "sm": 4, "md": 4, "lg": 4, "xl": 4,
        },
      ),
      dmc.GridCol(
        dmc.Button(
          "Load",
          n_clicks=0,
          id="load-button",
        ),
        span={
          "xs": 1, "sm": 1, "md": 1, "lg": 1, "xl": 1,
        },
      ),
    ],
    justify="space-around",
    align="flex-end",
    gutter="md",
    style={
      # Subtract gutter size from width
      "width": "calc(100% - 30px)",
    },
  ),
  style={
    "backgroundColor": "#02627a",
  },
)


eda_layout = html.Div(
  id="window-1",
  style={
    "height": "85vh",
  },
)



main_window = dmc.Grid(
  [
    dmc.Drawer(
      file_tree,
      title="File Tree",
      id="file-tree-drawer",
      padding="md",
      size="lg",
      zIndex=10000,
    ),
    dmc.GridCol(
      dmc.Group(
        [
          dmc.Text(
            id="name-header",
            size="lg",
            fw=700,
            #style={
            #  "font-size": "1.5em",
            #  "font-family": "monospace",
            #  "font-weight": "bold",
            #  "text-align": "center",
            #},
          ),
          eda_options,
        ],
        justify="space-around",
        #style={
        #  "max-width": "800px",
        #},
      ),
      span={
          "xs": 12, "sm": 11, "md": 10, "lg": 8, "xl": 6,
      },
    ),
    dmc.GridCol(
      style={
        "height": "1vh",
      },
    ),
    dmc.GridCol(
      eda_layout,
      span={
        "xs": 11, "sm": 11, "md": 11, "lg": 11, "xl": 10,
      },
      style={
        "border": "1px solid black",
      },
    ),
  ],
  gutter=0,
  align="center",
  justify="center",
)


main_layout = html.Div(
  [
    html.Div(
      [
        html.Div(
          style={
            "backgroundColor": "#02627a",
            "margin": "0px", 
            "padding": "0px",
            "height": "0.5vh",
          }
        ),
        html.Div(
          navbar,
          style={
            'padding-bottom': '1vh',
          },
        ),
      ],
      id="main-navbar",
      style={
          "display": "none",
      },
    ),
    html.Div(style={"height": "1vh"}),
    # Login in screen, username token
    dmc.Stack(
        [
            dmc.Text(
                "Connect to Dagshub API",
                size="xl",
                fw=700,
                ta="center",
            ),
            dmc.Text(
                "Please provide an access token",
                ta="center",
            ),
            html.Br(),
            dmc.Center([
                dmc.TextInput(
                    placeholder="Token",
                    id="login-token",
                    size="lg",
                    w="300",
                ),
                dmc.Button(
                    "Login",
                    id="login-button",
                    size="lg",
                    w="100",
                ),
            ]),
            html.Br(),
            dmc.Center(
                dmc.Alert(
                    "Please enter a valid token.",
                    title="Login Failed",
                    id="login-alert",
                    color="red",
                    withCloseButton=True,
                    hide=True,
                    w="300",
                ),
            ),
        ],
        pos="center",
        id="login-window",
        style={
            'display': 'block',
        },
    ),
    dmc.Stack(
      [
        dmc.LoadingOverlay(
          visible=False,
          id="loading-overlay",
          overlayProps={
              "raidus": "lg",
              "blur": 2,
          },
        ),
        dmc.Text(
          "Welcome to RepoViz",
          size="xl",
          fw=700,
          ta="center",
        ),
        dmc.Text(
          "Select a repository to get started",
          ta="center",
        ),
      ],
      pos="center",
      id="initial-window",
      style={
          'display': 'none',
      },
    ),
    html.Div(
      main_window,
      style={
        "margin": "0px",
        "height": "90vh",
        "display": "none",
      },
      id="loaded-window",
    ),
  ],
  id="main-layout",
)


layout = dmc.MantineProvider(
  [
    loading_state,
    app_state,
    main_layout,
  ],
  id="mantine-provider",
)


def init_layout(app):
    """
    """
    app.layout = layout
