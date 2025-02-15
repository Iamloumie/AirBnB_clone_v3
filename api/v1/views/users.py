#!/usr/bin/python3
"""
Objects that handles all default RestFul API actions for Users
"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/users", strict_slashes=False)
def get_users():
    """
    Gets list of all users
    """
    all_users = storage.all(User).values()
    list_of_users = []

    for user in all_users:
        list_of_users.append(user.to_dict())
    return jsonify(list_of_users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def retrieve_user(user_id):
    """
    Retrieves User ID, if not found, raises 404 error
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes User objects, return empty dictionary with status code 200
        returns 404 error if user ID is not found
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'
    If the dictionary doesn’t contain the key email,
        raise a 400 error with the message Missing email
    If the dictionary doesn’t contain the key password,
        raise a 400 error with the message Missing password
    Returns the new User with the status code 201
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "email" not in request.get_json():
        abort(400, description="Missing email")
    if "password" not in request.get_json():
        abort(400, descripton="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    If the user_id is not linked to any User object, raise a 404 error
    Using request.get_json from Flask to transform
        the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON
    Update the User object with all key-value pairs of the dictionary
    Ignore keys: id, email, created_at and updated_at
    Returns the User object with the status code 200
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "email", "created_at", "updated_at"]

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
