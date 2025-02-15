#!/usr/bin/python3
"""
Creates new view for State objects that handles
    all default RESTFul API actions
"""
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """
    Gets list of all states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def retrieve_state(state_id):
    """
    Retrieves state ID, if not found, raises 404 error
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes state ID, return empty dictionary with status code 200
        returns 404 error if state ID is not found
    """
    state = storage.get(State, state_id)

    if not state:
        return abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message 'Missing name'
    Returns the new State with the status code 201
    """
    if not request.get_json():
        return abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        return abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    If the state_id is not linked to any State object, raise a 404 error
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'

    Update the State object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the State object with the status code 200
    """
    state = storage.get(State, state_id)

    if not state:
        return abort(404)

    if not request.get_json():
        return abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at"]

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
