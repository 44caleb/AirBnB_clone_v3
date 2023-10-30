#!/usr/bin/python3
""" starts a flask rest api"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes=False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception=None):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
