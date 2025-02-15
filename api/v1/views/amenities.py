#!/usr/bin/python3
"""
Objects that handles all default RestFul API actions for Amenities
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """
    Gets list of all amenities
    """
    all_amenities = storage.all((Amenity).values())
    list_of_amenities = []

    for amenity in all_amenities:
        list_of_amenities.append(amenity.to_dict())
    return jsonify(list_of_amenities)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def retrieve_amenity(amenity_id):
    """
    Retrieves Amenity objects, if not found, raises 404 error
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes Amenity objects, return empty dictionary with status code 200
        returns 404 error if amenity ID is not found
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message 'Missing name'
    Returns the new amenity with the status code 201
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    If the amenity_id is not linked to any Amenity object, raise a 404 error
    Using request.get_json from Flask to transform the
        HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message 'Not a JSON'

    Update the Amenity object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the Amenity object with the status code 200
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at"]

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
