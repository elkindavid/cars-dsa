#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request
from preprocessing import load_data, encode_categorical_features, remove_outliers, add_y_mx_feature
from model import load_model

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    # Obtenemos los datos de entrada
    data = request.get_json()

    # Preprocesamos los datos
    X = load_data(data)
    X = encode_categorical_features(X)
    X = remove_outliers(X)
    X['YxM'] = X['Year'] * X['Mileage']

    # Cargamos el modelo
    model = load_model("model.pkl")

    # Realizamos la predicción
    predictions = model.predict(X)

    # Devolvemos la respuesta
    return {"predictions": predictions}


if __name__ == "__main__":
    app.run(debug=True)

