#!/usr/bin/python3
"""
Creates new view for State objects that handles
    all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states")
def get_all_states():
    """
    Gets all states objects
    """
    states = storage.all(state).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/states/<state_id>")
def retrieve_state(state_id):
    """
    Retrieves state ID, if not found, raises 404 error
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Deletes state ID, return empty dictionary with status code 200
        returns 404 error if state ID is not found
    """
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"])
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
    if request.content_type != "application/json":
        return abort(404, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")

    kwargs = request.get_json()

    if "name" not in kwargs:
        return abort(400, "Missing name")

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["PUT"])
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
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
