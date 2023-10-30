#!/usr/bin/python3
"""api endpoint for user objects"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def user():
    """gets or creates new user object"""
    if request.method == "GET":
        users = []
        for obj in storage.all(User).values():
            users.append(obj.to_dict())
        return jsonify(users), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if "password" not in data:
            abort(400, "Missing password")
        if "email" not in data:
            abort(400, "Missing email")
        new_obj = User(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def user_by_id(user_id):
    """get, updates, deletes user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404) 
    if request.method == "GET":
        return jsonify(user.to_dict()), 200
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key in ["id", "email", "created_at", "updated_at"]:
                pass
            else:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
