#!/usr/bin/python3
"""api endpoints for place objects"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def place_by_city(city_id):
    """gets or post place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "GET":
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places), 200
    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        if not storage.get(User, data["user_id"]):
            abort(404)
        data["city_id"] = city_id
        new_obj = Place(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def place_by_id(place_id):
    """gets, updates, deletes place obj based on id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict()), 200
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
                pass
            else:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
