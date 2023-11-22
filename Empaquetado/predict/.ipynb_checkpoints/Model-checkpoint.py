#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xgboost as xgb


def load_model(model_path):
    # Cargamos el modelo XGBoost desde la ruta especificada
    model = xgb.Booster()
    model.load_model(model_path)
    return model


def make_prediction(model, X):
    # Realizamos predicciones usando el modelo XGBoost
    predictions = model.predict(X)
    return predictions

