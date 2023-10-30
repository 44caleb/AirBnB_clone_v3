#!/usr/bin/python3
"""api endpoint for amenities objs based on place"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def amenities_by_place(place_id):
    """gets, creates amenity obj from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if method == "GET":
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
        return jsonify(amenities), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def amenity_by_id(place_id, amenity_id):
    """deletes or links amenity obj with a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if request.method == "DELETE":
        if amenity not in place.amenities:
            abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "POST":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
