# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import plotly.graph_objs as go

# PREDICTION API URL 
api_url = "http://44.211.203.63:5000/Api/Predict/"

# Importando datos
df = pd.read_csv('../datos/dataTrain_carListings.csv')

with open('feature_importance.json') as f:
    feature_importance_data = json.load(f)

with open('top_five_make.json') as f:
    car_data = json.load(f)

with open('prediction.json') as f:
    price_comparison_data = json.load(f)

with open('Comparativo.json') as f:
    price_data = json.load(f)

# Extraer los datos de año, precio predicho y precio real
years = [entry['Year'] for entry in price_data]
predicted_prices = [entry['PredictedPrice'] for entry in price_data]
real_prices = [entry['RealPrice'] for entry in price_data]

# Extraer los datos de precio actual y precio anterior
current_price = price_comparison_data['CurrentPrice']
previous_price = price_comparison_data['PreviousPrice']

# Top 5 Prices
makes = [entry['Make'] for entry in car_data]
prices = [entry['Price'] for entry in car_data]

df_sorted_make = pd.DataFrame(df['Make'].sort_values(ascending=True).unique(), columns=['Make'])
df_sorted_model = pd.DataFrame(df['Model'].sort_values(ascending=True).unique(), columns=['Model'])
df_sorted_state = pd.DataFrame(df['State'].sort_values(ascending=True).unique(), columns=['State'])
df_sorted_year = pd.DataFrame(df['Year'].sort_values(ascending=True).unique(), columns=['Year'])

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
        # Top Five Make
        dbc.Col(
            dcc.Graph(
                id='top-makes-treemap',
                figure={
                    'data': [
                        go.Treemap(
                            labels=makes,
                            parents=[''] * len(makes),
                            values=prices
                        )
                    ],
                    'layout': go.Layout(
                        title='Top Car Makes by Price (Treemap)'
                    )
                }
            ),
            width=5
        ),
         # Prediction
        dbc.Col(
            dcc.Graph(
                id='price-comparison-bar-chart',
                figure={
                    'data': [
                        go.Bar(
                            x=['Current Price', 'Previous Price'],
                            y=[current_price, previous_price]
                        )
                    ],
                    'layout': go.Layout(
                        title='Prediction',
                        yaxis={'title': 'Price'}
                    )
                }
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
                            x=years,
                            y=predicted_prices,
                            mode='lines',
                            name='Predicted Price'
                        ),
                        go.Scatter(
                            x=years,
                            y=real_prices,
                            mode='lines',
                            name='Real Price'
                        )
                    ],
                    'layout': go.Layout(
                        title='Predicted vs Real Prices Over Years',
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
    ]),

    #Tercera fila de gráficos
    dbc.Row([
        # Real Price vs Predicted Price
        dbc.Col(
            # Add a textarea for large text input
            dcc.Textarea(id='large-text-input', placeholder='Enter large text here', style={'width': '100%', 'height': '100px'}, className='mb-3'),
            width=12
        )
    ]),

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
    Output(component_id='large-text-input', component_property='value'),
    [Input(component_id='predict-button', component_property='n_clicks')],
    [State('year-dropdown', 'value'),
     State('numeric-input', 'value'),
     State('state-dropdown', 'value'),
     State('make-dropdown', 'value'),
     State('model-dropdown', 'value')]
)
def make_api_request(n_clicks,year, mileage, state, make, model):

    if any(value is None for value in [year, mileage, state, make, model]):
        return "Enter all required data before making the API request"

    try:
        payload = {'YEAR': year, 'MILEAGE': mileage, 'STATE': state, 'MAKE': make, 'MODEL': model}

        headers =  {"Content-Type":"application/json", "accept": "application/json"}

        # Make a POST request to the API
        response = requests.post(api_url, json=payload),
        if response.status_code == 200:
            api_data = response.json()
                
        else:
            return f"API request failed with status code: {response.status_code}"

    except ValueError:
        return "Enter valid data before making the API request"

    return api_data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
