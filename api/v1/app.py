#!/usr/bin/python3
"""
Created flask app; and registered the blueprint app_views
    to Flask instance app.
"""
from os import getenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flasgger import Swagger


app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_engine(exception):
    """End incoming session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """customized error page in json format"""
    response = {"error": "Not found"}
    return jsonify(response), 404


app.config["SWAGGER"] = {"title": "AirBnB clone Restful API", "uiversion": 3}

Swagger(app)


if __name__ == "__main__":
    """Main Function"""
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
