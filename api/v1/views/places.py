#!/usr/bin/python3
"""objects that handle all default RestFul API actions for Places"""
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    If the city_id is not linked to any City object, raise a 404 error
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route("/places/<place_id>", strict_slashes=False)
def retrieve_place(place_id):
    """
    Retrieves a Place object
    If the place_id is not linked to any Place object, raise a 404 error
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place Object
    If the place_id is not linked to any Place object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    Using request.get_json from Flask to transform
        the HTTP request to a dictionary
    If the city_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON,
        raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id,
        raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object, raise a 404 error
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message Missing name
    Returns the new Place with the status code 201
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])

    if not user:
        abort(404)

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place
    If the place_id is not linked to any Place object, raise a 404 error
    Using request.get_json from Flask to transform
        the HTTP request to a dictionary
    If the HTTP request body is not valid JSON,
        raise a 400 error with the message Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, user_id, city_id, created_at and updated_at
    Returns the Place object with the status code 200
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get("states", None)
        cities = data.get("cities", None)
        amenities = data.get("amenities", None)

    if not data or not len(data) or (not states and not cities and not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [
            place
            for place in list_places
            if all([am in place.amenities for am in amenities_obj])
        ]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop("amenities", None)
        places.append(d)

    return jsonify(places)
