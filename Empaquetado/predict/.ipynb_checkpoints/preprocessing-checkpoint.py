#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle

# Global settings
n_jobs = -1 # This parameter conrols the parallel processing. -1 means using all processors.
random_state = 40


# URL del archivo CSV en el repositorio de GitHub
url1 = 'https://raw.githubusercontent.com/jsalcedo14/DSA_project/master/dataTrain_carListings.csv'
url2 = 'https://raw.githubusercontent.com/jsalcedo14/DSA_project/master/dataTest_carListings.csv'
# Lee el archivo CSV en un DataFrame de pandas
data = pd.read_csv(url1)
test = pd.read_csv(url2)


def load_data(data):
    # Devuelve los datos de entrada
    return data


def encode_categorical_features(data):
    # Codifica las variables categoricas
    cat = ['State','Make','Model']
    for i in cat:
        idx, codex = pd.factorize(data[i])
        data[i] = idx
    return data


def remove_outliers(data):
    # Elimina los outliers
    Q1 = data['Price'].quantile(0.25)
    Q3 = data['Price'].quantile(0.75)
    IQR = Q3 - Q1
    BI_Calculado = (Q1 - 1.5 * IQR)
    BS_Calculado = (Q3 + 1.5 * IQR)
    ubicacion_outliers = (data['Price'] < BI_Calculado) | (data['Price'] > BS_Calculado)
    outliers = data[ubicacion_outliers]
    data = data[ubicacion_outliers == False]
    return data


def add_y_mx_feature(data):
    # Agrega la variable YxM
    data['YxM'] = data['Year'] * data['Mileage']
    return data


# In[1]:


from nbconvert import PythonExporter
import nbformat

def notebook_to_python(notebook_path, python_path):
    """
    Convierte un notebook (.ipynb) a un archivo Python (.py).

    Parameters:
    - notebook_path (str): Ruta del notebook a convertir.
    - python_path (str): Ruta del archivo Python de salida.
    """
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    python_exporter = PythonExporter()
    python_code, _ = python_exporter.from_notebook_node(notebook_content)

    with open(python_path, 'w', encoding='utf-8') as python_file:
        python_file.write(python_code)

# Rutas de entrada y salida
notebook_path = 'app.ipynb'
python_path = 'app.py'

# Llama a la función para convertir el notebook a Python
notebook_to_python(notebook_path, python_path)

