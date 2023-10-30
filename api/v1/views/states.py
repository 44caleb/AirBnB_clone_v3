#!/usr/bin/python3
"""view for state objeects that handles all its RESTful API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def get_states():
    """returns and creates states"""
    if request.method == "GET":
        state_objs = []
        for objs in storage.all(State).values():
            state_objs.append(objs.to_dict())
        return jsonify(state_objs)

    if request.method == "POST":
        post_data = request.get_json()
        if not post_data:
            abort(400, "Not a JSON")
        if "name" not in post_data:
            abort(400, "Missing name")
        new_state = State(**post_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def single_state(state_id):
    """returns a state with given id"""
    state_obj = storage.get(State, state_id)
    if request.method == "GET":
        if not state_obj:
            abort(404)
        return jsonify(state_obj.to_dict())

    if request.method == "DELETE":
        if not state_obj:
            abort(404)
        state_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        if not state_obj:
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key == "id" or key == "created_at" or key == "updated_at":
                pass
            setattr(state_obj, key, value)
        storage.save()
        return jsonify(state_obj.to_dict()), 200
