#!/usr/bin/python

import pandas as pd
import joblib
import sys
import os
import json

def predict(year, mileage, state, make, model):
    
    reg = joblib.load(os.path.dirname(__file__) + '/model.pkl') 
    
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

    #Rango aceptable de precios +/- 10% del precio de referencia
    min_price = p1 * 0.90
    max_price = p1 * 1.10

    similar_cars = []
    for mk in dic_categoricas['Make'].keys():

        car_2 = pd.DataFrame([[year, mileage, state_, dic_categoricas['Make'][mk], model_]], columns=['Year','Mileage','State','Make','Model'])   
        car_2['YxM'] = (year * mileage)

        price = int(reg.predict(car_2)[0])

        if min_price <= price <= max_price and mk != make:
            similar_cars.append((mk,price))

    # Ordena los resultados por similitud de precio
    similar_cars.sort(key=lambda x: abs(x[1] - p1))

    # Presenta los 5 mejores resultados
    top_5_similar_cars = similar_cars[:5]

    result_dict = {
        'Predict': p1,
        'Top5': top_5_similar_cars
    }

    return result_dict


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('Please add an URL')
    else:
        
        year = sys.argv[1]
        mileage = sys.argv[2]
        state = sys.argv[3]
        make = sys.argv[4]
        model = sys.argv[5]
        
        p1 = predict(year, mileage, state, make, model)
        
        print(car_)
        print('Car Price: ', p1)
        