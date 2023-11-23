#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from flask import Flask, request, jsonify
from preprocessing import load_data, encode_categorical_features, remove_outliers, add_y_mx_feature
from Model import load_model
from urllib.parse import quote as url_quote

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    # Get the input data
    data = request.get_json()

    # Preprocess the data
    X = load_data(data)
    X = encode_categorical_features(X)
    X = remove_outliers(X)
    X = add_y_mx_feature(X)

    # Load the model
    Model = load_model("model.pkl")

    # Make the prediction
    predictions = model.predict(X)

    # Return the response
    response = jsonify({"predictions": predictions})
    response.headers["Location"] = url_quote("/")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="3.91.71.251", port=5000)