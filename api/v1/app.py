#!/usr/bin/python3
"""
Created flask app; and registered the blueprint app_views
    to Flask instance app.
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_engine(exception):
    """End incoming session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """customized error page in json format"""
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    """Main Function"""
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
