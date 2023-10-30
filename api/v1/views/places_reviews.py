#!/usr/bin/python3
"""api endpoint for review objects"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def reviews_by_place(place_id):
    """gets, creates review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews), 200
    if request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if "text" not in data:
            abort(400, "Missing text")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        data["place_id"] = place_id
        new_obj = Review(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def reviews_by_id(review_id):
    """gets, updates, deletes review obj based on id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict()), 200
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key in ["place_id", "user_id", "id", "created_at", "updated_at"]:
                pass
            else:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
