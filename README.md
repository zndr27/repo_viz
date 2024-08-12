# RepoViz

Automated exploratory data analysis for <a href="https://dagshub.com">DagsHub</a> repositories.

## Installation

Create a virtual environment and install the dependencies from the pyproject.toml file.

Then run "python -m install --upgrade dagshub" to ensure you have the latest version of the Dagshub CLI, as certain package managers may install an older version.

## Run

Run the app in your terminal using the app.py script.

## Usage

When the app starts you'll be prompted to provide an <a href="https://dagshub.com/user/settings/tokens">access token</a>.

![image1](https://i.ibb.co/kB8dxwj/image.png)

Once you provide the access token, you'll be able to select a repository and a dataset to visualize.

![image2](https://i.ibb.co/tMTCJwR/image.png)
 
![image3](https://i.ibb.co/Z1G9QHh/image.png)

The app uses <a href="https://github.com/man-group/dtale">D-Tale</a>, <a href="https://pypi.org/project/sweetviz/">Sweetviz</a>, and <a href="https://github.com/ydataai/ydata-profiling">YData Profiling</a> to generate the visualizations.
