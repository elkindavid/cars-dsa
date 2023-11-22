#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
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


# Codificación de las variables categoricas
cat = ['State','Make','Model']
for i in cat:
    idx, codex = pd.factorize(data[i])
    data[i] = idx

# Elimina los outliers
Q1 = data['Price'].quantile(0.25)
Q3 = data['Price'].quantile(0.75)
IQR = Q3 - Q1
BI_Calculado = (Q1 - 1.5 * IQR)
BS_Calculado = (Q3 + 1.5 * IQR)
ubicacion_outliers = (data['Price'] < BI_Calculado) | (data['Price'] > BS_Calculado)
outliers = data[ubicacion_outliers]
data = data[ubicacion_outliers == False]

# Separamos los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(data.drop(['Price'], axis=1), data['Price'], test_size=0.33, random_state=40)

# defina los parámetros del modelo
learning_rate = 0.1
max_depth = 10
n_estimators = 300
subsample = 1

# Crea el modelo con los parámetros definidos
model = xgb.XGBRegressor(
    learning_rate=learning_rate,
    max_depth=max_depth,
    n_estimators=n_estimators,
    subsample=subsample,
    verbosity=0,
    random_state=random_state
)

# Entrena con los datos de entrenamiento
model.fit(X_train, y_train)

with open("model.pkl", "wb") as pkl_file:
    pickle.dump(model, pkl_file)


# In[5]:


import os
import inspect

def export_current_code(file_name):
    # Obtener el código fuente del módulo actual
    current_code = inspect.getsource(inspect.currentframe().f_code)

    # Obtener el directorio actual
    current_directory = os.getcwd()

    # Unir el directorio actual con el nombre del archivo
    file_path = os.path.join(current_directory, file_name)

    # Escribir el código en el archivo especificado
    with open(file_path, 'w') as file:
        file.write(current_code)

if __name__ == "__main__":
    # Especifica el nombre del archivo .py en el que deseas exportar el código
    nombre_archivo = "train.py"
    
    # Llama a la función para exportar el código
    export_current_code(nombre_archivo)

    print(f"El código actual ha sido exportado a {nombre_archivo} en el directorio actual.")

