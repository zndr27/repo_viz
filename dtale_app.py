from flask import request
from dtale.app import build_app
from dtale.views import startup
from dtale.global_state import cleanup
import pandas as pd
import uuid

# Create the dtale server
dtale_server = build_app(reaper_on=False)

@dtale_server.route("/create-df", methods=["POST"])
def create_df():
    """
    Create a dataframe instance in the dtale server.
    """
    data = request.json

    df = pd.read_json(data["dataframe"])
    data_id = data.get("instance_id", None)

    if data_id is not None:
        cleanup(data_id)
    else:
        data_id = str(uuid.uuid4())
    
    instance = startup(data_id=data_id, data=df, ignore_duplicate=True)

    return {"instance_id": instance._data_id}

if __name__ == "__main__":
    # Run the dtale server
    dtale_server.run(host="0.0.0.0", port=8080)
