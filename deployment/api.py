#!/usr/bin/python

from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
import joblib
from model import predict
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Definición aplicación Flask
app = Flask(__name__)

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

# Definición de la clase para disponibilización
@ns.route('/')
class CarPriceApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        
        return {
         "result": predict(args['YEAR'], args['MILEAGE'], args['STATE'], args['MAKE'], args['MODEL'])
        }, 200
    
    
if __name__ == '__main__':
    # Ejecución de la aplicación que disponibiliza el modelo de manera local en el puerto 5000
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=6500)
