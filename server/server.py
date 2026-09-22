import util
from flask import Flask, jsonify, request
from flask_cors import CORS
app=Flask(__name__)
CORS(app)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({

        'location':util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route('/predict_home_price',methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
    'estimated-price': util.get_estimated_price(
        location,
        total_sqft,
        bath,
        bhk
    )
})

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
if __name__=="__main__":
    util.load_artifacts()
    print("Starting python flask Server for Home price Prediction")
    app.run(debug=True, port=5001)