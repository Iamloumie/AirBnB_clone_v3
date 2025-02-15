#!/usr/bin/python3
"""
Create route on app_views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def api_status():
    """
    returns json response for RESTful API health
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats")
def get_stats():
    """
    Creates endpoint that retrieves the number of each objects by type
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "users": storage.count("User"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
    }

    return jsonify(stats)
