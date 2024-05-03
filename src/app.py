# #App with Contrast by DEPARTAMENTO Y MUNICIPIO (BEST app display! blue orange markers)
# import pandas as pd
# import geopandas as gpd
# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc, html, Input, Output
# import plotly.express as px
# import os
#
# # Load environment variables
# from dotenv import load_dotenv
# load_dotenv()
#
# # Ensuring the Mapbox Access Token is set
# MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
# if not MAPBOX_ACCESS_TOKEN:
#     raise EnvironmentError("The Mapbox Access Token has not been set in the environment variables.")
# px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)
#
# # Load the data
# data_path = 'https://github.com/rmejia41/open_datasets/raw/main/Cleaned_Homicidios_Accidentes_Trafico_C.xlsx'
# data = pd.read_excel(data_path)
#
# # # Load GeoJSON for municipalities and departments using Geopandas
# municipalities_geojson_path = 'https://github.com/rmejia41/open_datasets/raw/main/Servicios_Publicos_Municipios_d.json'
# #departments_geojson_path = 'https://github.com/rmejia41/open_datasets/raw/main/Subregiones_Provincias_de_Colombia.json'
# municipalities = gpd.read_file(municipalities_geojson_path)
# #departments = gpd.read_file(departments_geojson_path)
#
# # Load GeoJSON for municipalities and departments using Geopandas
# #municipalities_geojson_path = 'Subregiones_-_Provincias_de_Colombia.geojson'
# departments_geojson_path = 'colombia-with-regions_1430.geojson'
# #municipalities = gpd.read_file(municipalities_geojson_path)
# departments = gpd.read_file(departments_geojson_path)
#
# #print(municipalities.columns)
#
# # Normalize 'MUNICIPIO' column to uppercase and remove any potential leading/trailing whitespaces
# data['MUNICIPIO'] = data['MUNICIPIO'].str.upper().str.strip()
#
# # Collapse 'GENERO' categories 'NO REPORTADO' and 'NO REPOTADO' into 'NO REPORTA'
# data['GENERO'] = data['GENERO'].replace({'NO REPORTADO': 'NO REPORTA', 'NO REPOTADO': 'NO REPORTA'})
#
# # Initialize the Dash app with a theme
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
# server = app.server
#
# app.layout = dbc.Container([
#     dbc.Row([dbc.Col(html.H1("Traffic Accident Homicide Cases in Colombia", style={'margin-bottom': '20px'}), className='text-center', width=12)]),
#     dbc.Row([
#         dbc.Col(html.Label("Select a year:", style={'margin-bottom': '1.5px'}), width=1.5),
#         dbc.Col(dcc.Dropdown(
#             id='year-dropdown',
#             options=[{'label': year, 'value': year} for year in sorted(data['Año'].unique())] + [{'label': 'All Cases', 'value': 'All Cases'}],
#             value='All Cases',
#             clearable=False,
#             style={'width': '80%', 'margin-bottom': '1px'}
#         ), width=3),
#         dbc.Col(html.Label("Select a municipality:", style={'margin-bottom': '1.5px'}), width=1.5),
#         dbc.Col(dcc.Dropdown(
#             id='municipio-dropdown',
#             options=[{'label': mun, 'value': mun} for mun in sorted(data['MUNICIPIO']. unique())] + [{'label': 'All Cases', 'value': 'All Cases'}],
#             value='All Cases',
#             clearable=False,
#             style={'width': '80%', 'margin-bottom': '1px'}
#         ), width=3)
#     ]),
#     dbc.Row([
#         dbc.Col(html.Label("Select a visualization option:", style={'margin-bottom': '10px'}), width=2),
#         dbc.Col(dbc.RadioItems(
#             id='map-radio',
#             options=[
#                 {'label': 'Show Regional Borders', 'value': 'municipalities'},
#                 {'label': 'Show Department Borders', 'value': 'departments'},
#                 {'label': 'No Borders', 'value': 'none'}
#             ],
#             value='none',
#             inline=True
#         ), width=9)
#     ]),
#     dbc.Row([dbc.Col(dcc.Graph(id='map-graph', style={'height': '700px'}), width=12)])
# ], fluid=True)
#
# @app.callback(
#     Output('map-graph', 'figure'),
#     [Input('year-dropdown', 'value'),
#      Input('municipio-dropdown', 'value'),
#      Input('map-radio', 'value')]
# )
# def update_map(selected_year, selected_municipio, show_borders):
#     filtered_data = data.copy()
#     if selected_year != 'All Cases':
#         filtered_data = filtered_data[filtered_data['Año'] == selected_year]
#     if selected_municipio != 'All Cases':
#         filtered_data = filtered_data[filtered_data['MUNICIPIO'] == selected_municipio]
#
#     color_discrete_map = {'MASCULINO': 'blue', 'FEMENINO': 'orange'}  # Moved definition outside the condition
#
#     if selected_year != 'All Cases' or selected_municipio != 'All Cases':
#         filtered_data = filtered_data.groupby(['LATITUDE', 'LONGITUDE', 'MUNICIPIO', 'Año', 'GENERO'], as_index=False).agg({
#             'CANTIDAD': 'sum',
#             'ARMAS MEDIOS': lambda x: ', '.join([f"{k}: {v:.2%}" for k, v in pd.Series(x).value_counts(normalize=True).items()])
#         })
#
#     fig = px.scatter_mapbox(
#         filtered_data,
#         lat='LATITUDE',
#         lon='LONGITUDE',
#         color='GENERO',
#         size='CANTIDAD',
#         hover_name='MUNICIPIO',
#         hover_data={'Año': True, 'GENERO': True, 'CANTIDAD': True, 'ARMAS MEDIOS': True},
#         zoom=5,
#         mapbox_style="mapbox://styles/mapbox/navigation-day-v1",
#         size_max=15,
#         color_discrete_map=color_discrete_map
#     )
#
#     if show_borders == 'municipalities':
#         choropleth_trace = px.choropleth_mapbox(
#             municipalities, geojson=municipalities.geometry, locations=municipalities.index, opacity=0.5,
#             color_discrete_sequence=["#666666"],
#             hover_name='MPIO_CNMBR'
#         ).data[0]
#         fig.add_trace(choropleth_trace)
#     elif show_borders == 'departments':
#         choropleth_trace = px.choropleth_mapbox(
#             departments, geojson=departments.geometry, locations=departments.index, opacity=0.5,
#             color_discrete_sequence=["#666666"],
#             hover_name='name'
#         ).data[0]
#         fig.add_trace(choropleth_trace)
#
#     return fig
#
# if __name__ == '__main__':
#     app.run_server(debug=False, port=8051)

#Added link to policia nacional
# App with Contrast by DEPARTAMENTO Y MUNICIPIO (BEST app display! blue orange markers)
import pandas as pd
import geopandas as gpd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Ensuring the Mapbox Access Token is set
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
if not MAPBOX_ACCESS_TOKEN:
    raise EnvironmentError("The Mapbox Access Token has not been set in the environment variables.")
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

# Load the data
data_path = 'https://github.com/rmejia41/open_datasets/raw/main/Cleaned_Homicidios_Accidentes_Trafico_C.xlsx'
data = pd.read_excel(data_path)

# Load GeoJSON for municipalities
municipalities_geojson_path = 'https://github.com/rmejia41/open_datasets/raw/main/Servicios_Publicos_Municipios_d.json'
municipalities = gpd.read_file(municipalities_geojson_path)

# Load GeoJSON for departments
departments_geojson_path = 'colombia-with-regions_1430.geojson'
departments = gpd.read_file(departments_geojson_path)

# Normalize 'MUNICIPIO' column to uppercase and remove any potential leading/trailing whitespaces
data['MUNICIPIO'] = data['MUNICIPIO'].str.upper().str.strip()

# Collapse 'GENERO' categories 'NO REPORTADO' and 'NO REPOTADO' into 'NO REPORTA'
data['GENERO'] = data['GENERO'].replace({'NO REPORTADO': 'NO REPORTA', 'NO REPOTADO': 'NO REPORTA'})

# Initialize the Dash app with a theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Traffic Accident Homicide Cases in Colombia", style={'margin-bottom': '20px'}), className='text-center', width=12)
    ]),
    dbc.Row([
        dbc.Col(width=9),  # This empty column will push the link to the right
        dbc.Col(html.A("Police Department Open Data",
                       href="https://www.datos.gov.co/Seguridad-y-Defensa/Homicidios-accidente-de-tr-nsito-Polic-a-Nacional/ha6j-pa2r/about_data",
                       target="_blank",
                       className="link",
                       style={'width': '100%', 'display': 'inline-block', 'text-align': 'right', 'fontSize': '80%'}),
                width=3)
    ]),
    dbc.Row([
        dbc.Col(html.Label("Select a year:", style={'margin-bottom': '1.5px'}), width=1.5),
        dbc.Col(dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(data['Año'].unique())] + [{'label': 'All Cases', 'value': 'All Cases'}],
            value='All Cases',
            clearable=False,
            style={'width': '80%', 'margin-bottom': '1px'}
        ), width=3),
        dbc.Col(html.Label("Select a municipality:", style={'margin-bottom': '1.5px'}), width=1.5),
        dbc.Col(dcc.Dropdown(
            id='municipio-dropdown',
            options=[{'label': mun, 'value': mun} for mun in sorted(data['MUNICIPIO'].unique())] + [{'label': 'All Cases', 'value': 'All Cases'}],
            value='All Cases',
            clearable=False,
            style={'width': '80%', 'margin-bottom': '1px'}
        ), width=3)
    ]),
    dbc.Row([
        dbc.Col(html.Label("Select a visualization option:", style={'margin-bottom': '10px'}), width=2),
        dbc.Col(dbc.RadioItems(
            id='map-radio',
            options=[
                {'label': 'Show Regional Borders', 'value': 'municipalities'},
                {'label': 'Show Department Borders', 'value': 'departments'},
                {'label': 'No Borders', 'value': 'none'}
            ],
            value='none',
            inline=True
        ), width=9)
    ]),
    dbc.Row([dbc.Col(dcc.Graph(id='map-graph', style={'height': '700px'}), width=12)])
], fluid=True)

@app.callback(
    Output('map-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('municipio-dropdown', 'value'),
     Input('map-radio', 'value')]
)
def update_map(selected_year, selected_municipio, show_borders):
    filtered_data = data.copy()
    if selected_year != 'All Cases':
        filtered_data = filtered_data[filtered_data['Año'] == selected_year]
    if selected_municipio != 'All Cases':
        filtered_data = filtered_data[filtered_data['MUNICIPIO'] == selected_municipio]

    color_discrete_map = {'MASCULINO': 'blue', 'FEMENINO': 'orange'}  # Moved definition outside the condition

    if selected_year != 'All Cases' or selected_municipio != 'All Cases':
        filtered_data = filtered_data.groupby(['LATITUDE', 'LONGITUDE', 'MUNICIPIO', 'Año', 'GENERO'], as_index=False).agg({
            'CANTIDAD': 'sum',
            'ARMAS MEDIOS': lambda x: ', '.join([f"{k}: {v:.2%}" for k, v in pd.Series(x).value_counts(normalize=True).items()])
        })

    fig = px.scatter_mapbox(
        filtered_data,
        lat='LATITUDE',
        lon='LONGITUDE',
        color='GENERO',
        size='CANTIDAD',
        hover_name='MUNICIPIO',
        hover_data={'Año': True, 'GENERO': True, 'CANTIDAD': True, 'ARMAS MEDIOS': True},
        zoom=5,
        mapbox_style="mapbox://styles/mapbox/navigation-day-v1",
        size_max=15,
        color_discrete_map=color_discrete_map
    )

    if show_borders == 'municipalities':
        choropleth_trace = px.choropleth_mapbox(
            municipalities, geojson=municipalities.geometry, locations=municipalities.index, opacity=0.5,
            color_discrete_sequence=["#666666"],
            hover_name='MPIO_CNMBR'
        ).data[0]
        fig.add_trace(choropleth_trace)
    elif show_borders == 'departments':
        choropleth_trace = px.choropleth_mapbox(
            departments, geojson=departments.geometry, locations=departments.index, opacity=0.5,
            color_discrete_sequence=["#666666"],
            hover_name='name'
        ).data[0]
        fig.add_trace(choropleth_trace)

    return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8051)