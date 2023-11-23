#!/usr/bin/python

import pandas as pd
import joblib
import sys
import os
import json
from loguru import logger
import traceback

def predict(year, mileage, state, make, model):
    
    reg = joblib.load('model.pkl') 
    
    # Cargar el diccionario desde el archivo JSON
    with open("cod_categoricas.json", 'r') as archivo:
        dic_categoricas = json.load(archivo)

    try:
        state_ = dic_categoricas['State'][state]
        make_ = dic_categoricas['Make'][make]
        model_ = dic_categoricas['Model'][model]
    except KeyError:
        state_ = -1
        make_ = -1
        model_ = -1
    
    car_ = pd.DataFrame([[year, mileage, state_, make_, model_]], columns=['Year','Mileage','State','Make','Model'])   
    car_['YxM'] = (year * mileage)
    
    #Make prediction
    p1 = int(reg.predict(car_)[0])

    #Rango aceptable de precios +/- 20% del precio de referencia
    min_price = p1 * 0.80
    max_price = p1 * 1.20

    similar_cars = []
    for mk in dic_categoricas['Make'].keys():

        car_2 = pd.DataFrame([[year, mileage, state_, dic_categoricas['Make'][mk], model_]], columns=['Year','Mileage','State','Make','Model'])   
        car_2['YxM'] = (year * mileage)

        price = int(reg.predict(car_2)[0])

        if min_price <= price <= max_price and mk != make:
            similar_cars.append({'Make':mk,'Price':price})

    # Ordenar la lista de diccionarios por la distancia al valor de referencia
    similar_cars = sorted(similar_cars, key=lambda x: abs(x['Price'] - p1))

    # Tomar los 5 diccionarios más cercanos
    top_5_similar_cars = similar_cars[:5]

    result_dict = {
        'Predict': p1,
        'Top5': top_5_similar_cars
    }

    return p1


if __name__ == "__main__":
    logger.info("Year: {}".format(sys.argv[0]))

    if len(sys.argv) == 1:
        print('Please add an URL')
    else:
        print(sys.argv[0])


        year = sys.argv[0]
        mileage = sys.argv[1]
        state = sys.argv[2]
        make = sys.argv[3]
        model = sys.argv[4]
        
        p1 = predict(year, mileage, state, make, model)
        
        print(car_)
        print('Car Price: ', p1)
        