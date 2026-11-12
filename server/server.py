
import util

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Load the ML model when the application starts.
# This also works when Gunicorn imports the app.
util.load_artifacts()


@app.route("/")
def home():
    return jsonify({
        "message": "HomePrice AI API is running!"
    })


@app.route("/get_location_names")
def get_location_names():
    return jsonify({
        "location": util.get_location_names()
    })


@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():

    total_sqft = float(request.form["total_sqft"])
    location = request.form["location"]
    bhk = int(request.form["bhk"])
    bath = int(request.form["bath"])

    price = util.get_estimated_price(
        location,
        total_sqft,
        bath,
        bhk
    )

    return jsonify({
        "estimated-price": price
    })


if __name__ == "__main__":
    app.run(debug=False, port=5001)
