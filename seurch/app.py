import subprocess

from flask import jsonify, render_template
from flask.wrappers import Response
from insig.logging.logger import Logger

from seurch.make_app import make_app

app = make_app()

logger = Logger().get_logger()


@app.get("/status")
def check_status() -> Response:
    commit_id = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    return jsonify({"sha": commit_id, "status": "up"})

