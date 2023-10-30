#!/usr/bin/python3
""" starts a flask rest api"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


api_host = os.getenv("HBNB_API_HOST")
api_port = os.getenv("HBNB_API_PORT")


cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=api_host, port=api_port, threaded=True)
