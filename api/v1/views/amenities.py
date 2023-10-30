#!/usr/bin/python3
"""api endpoint for amenities objects"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """gets or creates amenity objects"""
    if request.method == "GET":
        amenities = []
        for obj in storage.all(Amenity).values():
            amenities.append(obj.to_dict())
        return jsonify(amenities), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        new_obj = Amenity(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["DELETE", "PUT", "GET"])
def amenities_by_id(amenity_id):
    """get, deletes or updates amenity object based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict()), 200
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key in ["id", "created_at", "updated_at"]:
                pass
            else:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
