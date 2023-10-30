#!/usr/bin/python3
"""api endpoints for city objects"""


from api.v1.views import app_views, jsonify
from flask import Flask, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def city_by_state(state_id):
    """gets or posts a city object from a particular state"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if request.method == "GET":
        city_list = []
        for city_obj in state_obj.cities:
            city_list.append(city_obj.to_dict())
        return jsonify(city_list), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        # adds state id to post data
        if "state_id" not in data:
            data["state_id"] = state_id
        new_obj = City(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city_by_id(city_id):
    """get, deletes or update city object of particular id"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if request.method == "GET":
        return jsonify(city_obj.to_dict()), 200
    
    if request.method == "DELETE":
        city_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key in ["id", "state_id", "created_at", "updated_at"]:
                pass
            setattr(city_obj, key, value)
        storage.save()
        return jsonify(city_obj.to_dict()), 200
