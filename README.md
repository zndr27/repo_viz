# RepoViz

Automated exploratory data analysis for <a href="https://dagshub.com">DagsHub</a> repositories.

## Installation

RepoViz supports Python 3.10 - 3.12.

First, create a virtual environment and install the dependencies from the pyproject.toml file using your favorite package management tools.

For example, you can use <a href="https://pdm-project.org/en/latest/">pdm</a> and <a href="https://github.com/pyenv/pyenv">pyenv</a> as follows:
```
cd path/to/repo-viz
pyenv install 3.12.4
pdm use 3.12.4
pdm install
```

Second, use pip to install the DagsHub client in the virtual environment. This is necessary due to a dependency version conflict with ydata-profiling.

For example:
```
cd path/to/repo-viz 
eval $(pdm venv activate)
python -m pip install --upgrade dagshub
```

## Run

First, start the D-Tale server in your terminal:
```
python ./dtale_app.py
```

Then, run the RepoViz server in your terminal:
```
python ./app.py
```

Finally, open your browser and navigate to `http://localhost:8051/`.

## Usage

When the app starts you'll be prompted to provide an <a href="https://dagshub.com/user/settings/tokens">access token</a>.

![image1](https://i.ibb.co/kB8dxwj/image.png)

Once you provide the access token, you'll be able to select a repository and a dataset to visualize.

![image2](https://i.ibb.co/tMTCJwR/image.png)
 
![image3](https://i.ibb.co/Z1G9QHh/image.png)

The app uses <a href="https://github.com/man-group/dtale">D-Tale</a>, <a href="https://pypi.org/project/sweetviz/">Sweetviz</a>, and <a href="https://github.com/ydataai/ydata-profiling">YData Profiling</a> to generate the visualizations.
