# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import plotly.graph_objs as go
import requests
from flask import request
from loguru import logger

# PREDICTION API URL 
api_url = "http://192.168.1.6:6500/Api/Predict/"

prediction_list = [0,0]

# Importando datos
df = pd.read_csv('../datos/dataTrain_carListings_predict.csv')
#df_line = df.groupby(['Year','Make'])['Price','Predictions'].mean().reset_index()
df_line = df.groupby(['Year', 'Make']).agg({'Price': 'mean', 'Predictions': 'mean'}).reset_index()

with open('feature_importance.json') as f:
    feature_importance_data = json.load(f)

with open('top_five_make.json') as f:
    car_data = json.load(f)

with open('prediction.json') as f:
    price_comparison_data = json.load(f)

with open('Comparativo.json') as f:
    price_data = json.load(f)

# Extraer los datos de año, precio predicho y precio real
#years = [entry['Year'] for entry in price_data]
#predicted_prices = [entry['PredictedPrice'] for entry in price_data]
#real_prices = [entry['RealPrice'] for entry in price_data]

makes = [entry['Make'] for entry in car_data]
prices = [entry['Price'] for entry in car_data]

df_sorted_make = pd.DataFrame(df['Make'].sort_values(ascending=True).unique(), columns=['Make'])
df_sorted_model = pd.DataFrame(df['Model'].sort_values(ascending=True).unique(), columns=['Model'])
df_sorted_state = pd.DataFrame(df['State'].sort_values(ascending=True).unique(), columns=['State'])
df_sorted_year = pd.DataFrame(df['Year'].sort_values(ascending=False).unique(), columns=['Year'])

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    # Título
    dbc.Row([
        html.Div('Car Prices', className="text-primary text-center fs-3"),
        html.Hr(),
    ]),

    # Labels
    dbc.Row([
        dbc.Col(
            html.Label('Make'),  
            width=2
        ),
        dbc.Col(
            html.Label('Model'),  
            width=2
        ),
        dbc.Col(
            html.Label('State'),  
            width=2
        ),
        dbc.Col(
            html.Label('Year'),  
            width=2
        ),dbc.Col(
            html.Label('Mileage'),  
            width=2
        )
    ]),

    # Controles
    dbc.Row([
        dbc.Col(
            # Lista de Marcas
            dcc.Dropdown(
                id='make-dropdown',
                options=[{'label': make, 'value': make} for make in df_sorted_make['Make']],
                value=df_sorted_make['Make'][0], 
                style={'width': '260px'}
            ),
            width=2
        ),
        dbc.Col(
            # Lista de Modelos
            dcc.Dropdown(
                id='model-dropdown',
                options=[{'label': model, 'value': model} for model in df_sorted_model['Model']],
                value=df_sorted_model['Model'][0], 
                style={'width': '260px'}
            ),
            width=2
        ),
        dbc.Col(
                # Lista de Estados
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': state, 'value': state} for state in df_sorted_state['State']],
                value=df_sorted_state['State'][0], 
                style={'width': '260px'}
            ),
            width=2
        ),
        dbc.Col(
            # Lista de años
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in df_sorted_year['Year']],
                value=df_sorted_year['Year'][0],  
                style={'width': '260px'}
            ),
            width=2
        ),
        dbc.Col(
            # Agregar una caja de entrada numérica
            dbc.Input(id='numeric-input', type='number', placeholder='Enter a Number', className='mb-3'),
            width=2
        ),
        dbc.Col(
            # Agregar un botón de predicción
            dbc.Button('Predict', id='predict-button', color='primary', className='mb-3'),
            width=2
        )
         
    ]),


    #Primera fila de gráficos
    dbc.Row([
        # Feature Importance
        dbc.Col(
            dcc.Graph(
                id='feature-importance-bar-chart',
                figure={
                    'data': [
                        go.Bar(
                            y=list(feature_importance_data.keys()),
                            x=list(feature_importance_data.values()),
                            orientation='h'
                        )
                    ],
                    'layout': go.Layout(
                        title='Feature Importance',
                        xaxis={'title': 'Features'},
                        yaxis={'title': 'Importance'}
                    )
                }
            ),
            width=5
        ),
        # Similar Cars Options

        dbc.Col(
            dcc.Graph(
                id='top-makes-treemap',
                figure={}
            ),
            width=5
        ),
         # Prediction
        dbc.Col(
            dcc.Graph(
                id='price-comparison-bar-chart',
                figure={}
            ),
            width=2
        )
    ]),

     dbc.Row([
        dbc.Col(
            width=6
        ),
        dbc.Col(
            dbc.RadioItems(
                options=[{"label": x, "value": x} for x in ['Year', 'State', 'Make']],
                value='Year',
                inline=True,
                id='radio-buttons-final'
            ),
            width=6
        ) 
    ]),

    #Segunda fila de gráficos
    dbc.Row([
        # Real Price vs Predicted Price
        dbc.Col(
            dcc.Graph(
                id='price-comparison-line-chart',
                figure={
                    'data': [
                        go.Scatter(
                            x=df_line['Year'],
                            y=df_line['Predictions'],
                            mode='lines',
                            name='Predicted Price'
                        ),
                        go.Scatter(
                            x=df_line['Year'],
                            y=df_line['Price'],
                            mode='lines',
                            name='Real Price'
                        )
                    ],
                    'layout': go.Layout(
                        title='Predicted vs Real avg Prices  Over Years',
                        xaxis={'title': 'Year'},
                        yaxis={'title': 'Price'}
                    )
                }
            ),
            width=5
        ),
        # Distribución de los datos
        dbc.Col(    
            dcc.Graph(figure={}, id='my-first-graph-final'), 
            width=7
        )
    ])

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value'),
)
def update_graph(col_chosen):

    fig = px.histogram(df, x=col_chosen, y='Price', histfunc='avg')
    fig.update_layout(title_text="Data Distribution")
    return fig


@callback(
    [Output(component_id='price-comparison-bar-chart', component_property='figure'),
    Output(component_id='top-makes-treemap', component_property='figure')],
    [Input(component_id='predict-button', component_property='n_clicks'),
    State('year-dropdown', 'value'),
    State('numeric-input', 'value'),
    State('state-dropdown', 'value'),
    State('make-dropdown', 'value'),
    State('model-dropdown', 'value')]
)
def make_api_request(nclicks,year, mileage, state, make, model):

    if any(value is None for value in [year, mileage, state, make, model]):
        return {},{}

    try:

        payload = {'YEAR': year, 'MILEAGE': mileage, 'STATE': state, 'MAKE': make, 'MODEL': model}

        headers =  {"Content-Type":"application/json", "accept": "application/json"}

        # Make a GET request to the API
        api_response = requests.get(api_url, params=payload, headers=headers).json()

        # Extrae la cadena JSON de la respuesta
        json_string = api_response["result"]

        # Convierte la cadena JSON a un diccionario de Python
        data = json.loads(json_string.replace("'", "\""))
        
        # Verifica si la clave 'Predict' está presente en el diccionario
        if 'Predict' in data:
            # Guarda el valor de 'Predict' en una variable
            predict_value = data['Predict']
            prediction_list.append(predict_value)
            print(f'Valor de Predict: {predict_value}')
        
        # Verifica si la clave 'Top5' está presente en el diccionario
        if 'Top5' in data:
            # Guarda el valor de 'Top5' en una variable
            top5_value = data['Top5']
            print(f'Valor de Top5: {top5_value}')
        
        # Similar cars variables
        makes = [entry['Make'] for entry in top5_value]
        prices = [entry['Price'] for entry in top5_value]

        if len(makes) != 0:
            treemap={
                        'data': [
                            go.Treemap(
                                labels=makes,
                                parents=[''] * len(makes),
                                values=prices
                            )
                        ],
                        'layout': go.Layout(
                            title='Similar Cars Options'
                        )
                    }
        else:
            treemap = {}
        
        bar_chart={
                    'data': [
                        go.Bar(
                            x=['Current Price', 'Previous Price'],
                            y=[predict_value, prediction_list[-2]]
                        )
                    ],
                    'layout': go.Layout(
                        title='Prediction',
                        yaxis={'title': 'Price'}
                    )
                }
        
    except ValueError:
        return "Enter valid data before making the API request"

    return bar_chart,treemap

@app.callback(
    Output(component_id='price-comparison-line-chart', component_property='figure'),
    [Input(component_id='make-dropdown', component_property='value')],
)
def update_price_comparison_chart(selected_make):
    # Filter data based on the selected make
    filtered_data = df_line[df_line['Make'] == selected_make]

    # Extract the updated values for years, predicted prices, and real prices
    updated_years = filtered_data['Year']
    updated_predicted_prices = filtered_data['Predictions']
    updated_real_prices = filtered_data['Price']

    # Create a new figure for the line chart
    fig = {
        'data': [
            go.Scatter(
                x=updated_years,
                y=updated_predicted_prices,
                mode='lines+markers',  # Agrega marcadores a la línea
                name='Predicted Price',
                text=[f'Make: {make}, Predicted Price: {predicted_price}' for make, predicted_price in zip([selected_make] * len(updated_years), updated_predicted_prices)],
                hoverinfo='text'  # Muestra información al pasar el ratón sobre los marcadores
            ),
            go.Scatter(
                x=updated_years,
                y=updated_real_prices,
                mode='lines+markers',  # Agrega marcadores a la línea
                name='Real Price',
                text=[f'Make: {make}, Real Price: {real_price}' for make, real_price in zip([selected_make] * len(updated_years), updated_real_prices)],
                hoverinfo='text'  # Muestra información al pasar el ratón sobre los marcadores
            )
        ],
        'layout': go.Layout(
            title=f'Predicted vs Real Prices for Make: {selected_make}',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Price'}
        )
    }

    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
