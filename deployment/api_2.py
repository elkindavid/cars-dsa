#!/usr/bin/python

from flask import Flask, jsonify, request, abort
from flask_restx import Api, Resource, fields
import joblib
from model import predict
from flask_cors import CORS
import json
import ssl
from functools import wraps
import pandas as pd


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Definición API Flask
api = Api(
    app, 
    version='1.0', 
    title='Car Prices API',
    description='Car Prices API')

ns = api.namespace('Api/Predict', 
     description='Car Prices API')

# Definición argumentos o parámetros de la API
parser = api.parser()

parser.add_argument(
    'YEAR', 
    type=int, 
    required=True, 
    help='Year', 
    location='args')

parser.add_argument(
    'MILEAGE', 
    type=int, 
    required=True, 
    help='Mileage', 
    location='args')

parser.add_argument(
    'STATE', 
    type=str, 
    required=True, 
    help='State', 
    location='args')

parser.add_argument(
    'MAKE', 
    type=str, 
    required=True, 
    help='Make', 
    location='args')

parser.add_argument(
    'MODEL', 
    type=str, 
    required=True, 
    help='Model', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

# @app.route('/', methods=['GET'])
# def title_page():
#     return 'Car Rest API'

@ns.route('/', methods=['POST'])
def predict():
    try:
        json_ = json.loads(request.json)
        df = pd.DataFrame(json_)['YEAR','MILEAGE','STATE','MAKE','MODEL']
        prediction = predict(df).tolist()
        return jsonify({'Prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = 6500
    app.run(host='0.0.0.0', port=port, debug=False)