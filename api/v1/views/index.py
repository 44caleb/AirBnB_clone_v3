#!/usr/bin/python3
"""creates api endpoint that returns status"""


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """returns a status json response"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """returns the count of all objects for each class"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
            "reviews": Review, "states": State, "users": User}
    new_dict = {}
    for name, cls in classes.items():
        new_dict[name] = storage.count(cls)
    return jsonify(new_dict)
