#!/usr/bin/python3
"""
Creates new view for City objects that handles
    all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities_by_states(state_id):
    """
    Gets list of all cities of a state
    """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def retrieve_city(city_id):
    """
    Retrieves city ID, if not found, raises 404 error
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes city ID, return empty dictionary with status code 200
        returns 404 error if city ID is not found
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message 'Missing name'
    Returns the new City with the status code 201
    """
    if request.content_type != "application/json":
        return abort(400, description="Not a JSON")
    state = storage.get(State, state_id)

    if not state:
        return abort(404)

    if not request.get_json():
        return abort(400, description="Not a JSON")
    else:
        data = request.get_json()

    if "name" not in data:
        return abort(400, description="Missing name")
    data["state_id"] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    If the city_id is not linked to any CIty object, raise a 404 error
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'

    Update the City object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the City object with the status code 200
    """
    if request.content_type != "application/json":
        return abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, description="Not a JSON")

        data = request.get_json()
        ignore_keys = ["id", "state_id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
