## Comandos para la terminal: 1)cd dashboard 2)python app.py
"""
Dashboard Interactivo Ejecutivo - StreamView Analytics (EP5)
Autores: Benjamin Patiño & Benjamin Vargas
Asignatura: Visualización de Datos (ADY1104) - Duoc UC
"""
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Carga resiliente del dataset maestro o de las fuentes originales
if os.path.exists('../data/streamview_master_processed.csv'):
    df_master_processed = pd.read_csv('../data/streamview_master_processed.csv')
elif os.path.exists('streamview_master_processed.csv'):
    df_master_processed = pd.read_csv('streamview_master_processed.csv')
else:
    df_tv = pd.read_csv('data/netflix_tv_shows_detailed_up_to_2025.csv')
    df_movies = pd.read_csv('data/netflix_movies_detailed_up_to_2025.csv')
    df_tv['tipo_contenido'] = 'TV Show'
    df_movies['tipo_contenido'] = 'Movie'
    cols = ['show_id', 'tipo_contenido', 'title', 'country', 'date_added',
            'release_year', 'genres', 'language', 'popularity', 'vote_count', 'vote_average']
    df_master_processed = pd.concat([df_tv[cols], df_movies[cols]], ignore_index=True)
    df_master_processed[['country', 'genres', 'language']] = df_master_processed[['country', 'genres', 'language']].fillna('Unknown')
    df_master_processed['date_added'] = pd.to_datetime(df_master_processed['date_added'], errors='coerce')
    df_master_processed = df_master_processed.dropna(subset=['date_added'])
    df_master_processed['año_agregado'] = df_master_processed['date_added'].dt.year
    df_master_processed['genero_principal'] = df_master_processed['genres'].apply(lambda x: str(x).split(',')[0].strip())
    df_master_processed['pais_principal'] = df_master_processed['country'].apply(lambda x: str(x).split(',')[0].strip())
    df_master_processed = df_master_processed.drop_duplicates(subset=['show_id'])

# Paleta corporativa accesible (Daltonismo-safe: Azul Petróleo vs Ámbar Cálido)
COLOR_MAP = {'TV Show': '#005F73', 'Movie': '#EE9B00'}

app = Dash(__name__)
app.title = "StreamView Analytics | Executive Dashboard"

paises_top = ['Todos'] + sorted(df_master_processed['pais_principal'].value_counts().head(15).index.tolist())
generos_top = ['Todos'] + sorted(df_master_processed['genero_principal'].unique().tolist())

app.layout = html.Div(style={'fontFamily': 'Segoe UI, Roboto, sans-serif', 'backgroundColor': '#F8F9FA', 'padding': '20px'}, children=[
    # Encabezado Corporativo
    html.Div(style={'backgroundColor': '#1D3557', 'color': 'white', 'padding': '20px 28px', 'borderRadius': '10px', 'marginBottom': '20px', 'boxShadow': '0 4px 10px rgba(0,0,0,0.1)'}, children=[
        html.H1("StreamView Analytics — Dashboard de Retención y Engagement", style={'margin': '0', 'fontSize': '26px'}),
        html.P("Solución Integral de Visualización de Datos para Decisiones C-Level y Product Managers | Consultores: Benjamin Patiño & Benjamin Vargas", style={'margin': '6px 0 0 0', 'color': '#A8DADC', 'fontSize': '14px'})
    ]),

    # Panel de Filtros Interactivos (Evaluación 2 + EP5)
    html.Div(style={'backgroundColor': 'white', 'padding': '18px', 'borderRadius': '10px', 'marginBottom': '20px', 'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '18px', 'boxShadow': '0 2px 6px rgba(0,0,0,0.06)'}, children=[
        html.Div([
            html.Label("Formato de Contenido:", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#1D3557'}),
            dcc.Dropdown(
                id='filtro-formato',
                options=[{'label': 'Todos los Formatos', 'value': 'Todos'},
                         {'label': 'Series (TV Show)', 'value': 'TV Show'},
                         {'label': 'Películas (Movie)', 'value': 'Movie'}],
                value='Todos', clearable=False
            )
        ]),
        html.Div([
            html.Label("País Productor Principal (Top 15):", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#1D3557'}),
            dcc.Dropdown(
                id='filtro-pais',
                options=[{'label': p, 'value': p} for p in paises_top],
                value='Todos', clearable=False
            )
        ]),
        html.Div([
            html.Label("Género Principal:", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#1D3557'}),
            dcc.Dropdown(
                id='filtro-genero',
                options=[{'label': g, 'value': g} for g in generos_top],
                value='Todos', clearable=False
            )
        ]),
        html.Div([
            html.Label("Rango de Año de Incorporación:", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#1D3557'}),
            dcc.RangeSlider(
                id='filtro-anio',
                min=2010, max=2025, step=1,
                value=[2010, 2025],
                marks={yr: str(yr) for yr in range(2010, 2026, 3)}
            )
        ])
    ]),

    # Tarjetas de Indicadores Clave (KPIs)
    html.Div(id='kpi-container', style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '18px', 'marginBottom': '20px'}),

    # Navegación por Pestañas (Storytelling & Exploración)
    dcc.Tabs(id='tabs-analisis', value='tab-ejecutivo', children=[
        dcc.Tab(label='1. Panorama Ejecutivo y Evolución Temporal', value='tab-ejecutivo', style={'fontWeight': 'bold'}, selected_style={'fontWeight': 'bold', 'borderTop': '3px solid #005F73'}),
        dcc.Tab(label='2. Engagement por Género y Matriz Calidad vs. Tracción', value='tab-engagement', style={'fontWeight': 'bold'}, selected_style={'fontWeight': 'bold', 'borderTop': '3px solid #EE9B00'}),
        dcc.Tab(label='3. Distribución Geográfica y Mercados Clave', value='tab-mercados', style={'fontWeight': 'bold'}, selected_style={'fontWeight': 'bold', 'borderTop': '3px solid #1D3557'})
    ]),

    html.Div(id='contenido-tabs', style={'marginTop': '18px'})
])

@app.callback(
    [Output('kpi-container', 'children'),
     Output('contenido-tabs', 'children')],
    [Input('filtro-formato', 'value'),
     Input('filtro-pais', 'value'),
     Input('filtro-genero', 'value'),
     Input('filtro-anio', 'value'),
     Input('tabs-analisis', 'value')]
)
def actualizar_dashboard(formato, pais, genero, rango_anio, tab_activa):
    dff = df_master_processed[
        (df_master_processed['año_agregado'] >= rango_anio[0]) &
        (df_master_processed['año_agregado'] <= rango_anio[1])
    ].copy()

    if formato != 'Todos':
        dff = dff[dff['tipo_contenido'] == formato]
    if pais != 'Todos':
        dff = dff[dff['pais_principal'] == pais]
    if genero != 'Todos':
        dff = dff[dff['genero_principal'] == genero]

    total_titulos = len(dff)
    pop_promedio = dff['popularity'].mean() if total_titulos > 0 else 0
    dff_votados = dff[dff['vote_count'] > 0]
    calif_promedio = dff_votados['vote_average'].mean() if len(dff_votados) > 0 else 0
    pct_series = (len(dff[dff['tipo_contenido'] == 'TV Show']) / total_titulos * 100) if total_titulos > 0 else 0

    card_style = {'backgroundColor': 'white', 'padding': '16px 20px', 'borderRadius': '10px', 'boxShadow': '0 2px 6px rgba(0,0,0,0.06)', 'borderLeft': '5px solid #005F73'}
    kpis = [
        html.Div(style=card_style, children=[
            html.Div("CATÁLOGO ACTIVO FILTRADO", style={'fontSize': '12px', 'color': '#6C757D', 'fontWeight': 'bold'}),
            html.Div(f"{total_titulos:,} títulos", style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#1D3557', 'marginTop': '4px'}),
            html.Div(f"Periodo {rango_anio[0]} - {rango_anio[1]}", style={'fontSize': '12px', 'color': '#2A9D8F'})
        ]),
        html.Div(style={**card_style, 'borderLeft': '5px solid #EE9B00'}, children=[
            html.Div("ÍNDICE DE ENGAGEMENT (POPULARIDAD)", style={'fontSize': '12px', 'color': '#6C757D', 'fontWeight': 'bold'}),
            html.Div(f"{pop_promedio:.1f} pts", style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#1D3557', 'marginTop': '4px'}),
            html.Div("Tracción media por título", style={'fontSize': '12px', 'color': '#E76F51'})
        ]),
        html.Div(style={**card_style, 'borderLeft': '5px solid #2A9D8F'}, children=[
            html.Div("CALIFICACIÓN MEDIA USUARIOS (VOTADOS)", style={'fontSize': '12px', 'color': '#6C757D', 'fontWeight': 'bold'}),
            html.Div(f"{calif_promedio:.2f} / 10", style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#1D3557', 'marginTop': '4px'}),
            html.Div(f"Sobre {len(dff_votados):,} títulos calificados", style={'fontSize': '12px', 'color': '#2A9D8F'})
        ]),
        html.Div(style={**card_style, 'borderLeft': '5px solid #1D3557'}, children=[
            html.Div("CUOTA DE SERIES (RETENCIÓN >90 DÍAS)", style={'fontSize': '12px', 'color': '#6C757D', 'fontWeight': 'bold'}),
            html.Div(f"{pct_series:.1f}% Series", style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#1D3557', 'marginTop': '4px'}),
            html.Div(f"{100 - pct_series:.1f}% Películas", style={'fontSize': '12px', 'color': '#6C757D'})
        ])
    ]

    if tab_activa == 'tab-ejecutivo':
        df_t = dff.groupby(['año_agregado', 'tipo_contenido']).agg(
            cantidad=('show_id', 'count'),
            popularidad=('popularity', 'mean')
        ).reset_index()
        fig_evol = px.line(
            df_t, x='año_agregado', y='cantidad', color='tipo_contenido', markers=True,
            title='Evolución Anual de Incorporaciones al Catálogo',
            labels={'año_agregado': 'Año de Ingreso', 'cantidad': 'Cantidad de Títulos', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        fig_pop_t = px.line(
            df_t, x='año_agregado', y='popularidad', color='tipo_contenido', markers=True,
            title='Evolución del Índice de Popularidad Promedio por Formato',
            labels={'año_agregado': 'Año de Ingreso', 'popularidad': 'Popularidad Promedio', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        contenido = html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '18px'}, children=[
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_evol)]),
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_pop_t)])
        ])
    elif tab_activa == 'tab-engagement':
        top_g = dff['genero_principal'].value_counts().head(10).index
        df_g = dff[dff['genero_principal'].isin(top_g)].groupby(['genero_principal', 'tipo_contenido'])['popularity'].mean().reset_index()
        fig_bar = px.bar(
            df_g, x='popularity', y='genero_principal', color='tipo_contenido', barmode='group', orientation='h',
            title='Popularidad Promedio en el Top 10 de Géneros',
            labels={'popularity': 'Popularidad Promedio', 'genero_principal': 'Género Principal', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})

        df_sc = dff[(dff['vote_average'] > 0) & (dff['popularity'] < 400)]
        fig_sc = px.scatter(
            df_sc, x='vote_average', y='popularity', color='tipo_contenido', opacity=0.45,
            hover_data=['title', 'genero_principal', 'pais_principal'],
            title='Matriz de Calidad (Calificación) vs. Tracción (Popularidad)',
            labels={'vote_average': 'Calificación Promedio (1-10)', 'popularity': 'Índice de Popularidad', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        contenido = html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '18px'}, children=[
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_bar)]),
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_sc)])
        ])
    else:
        df_p = dff[dff['pais_principal'] != 'Unknown'].groupby(['pais_principal', 'tipo_contenido']).agg(
            cantidad=('show_id', 'count'),
            popularidad=('popularity', 'mean')
        ).reset_index()
        top_p = dff[dff['pais_principal'] != 'Unknown']['pais_principal'].value_counts().head(10).index
        df_p = df_p[df_p['pais_principal'].isin(top_p)]
        fig_pais = px.bar(
            df_p, x='cantidad', y='pais_principal', color='tipo_contenido', barmode='stack', orientation='h',
            title='Top 10 Países Productores por Volumen de Catálogo',
            labels={'cantidad': 'Cantidad de Títulos', 'pais_principal': 'País Productor', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        fig_pais.update_layout(yaxis={'categoryorder': 'total ascending'})

        fig_pais_pop = px.bar(
            df_p, x='popularidad', y='pais_principal', color='tipo_contenido', barmode='group', orientation='h',
            title='Engagement (Popularidad Media) por País de Origen',
            labels={'popularidad': 'Popularidad Promedio', 'pais_principal': 'País Productor', 'tipo_contenido': 'Formato'},
            color_discrete_map=COLOR_MAP, template='plotly_white'
        )
        fig_pais_pop.update_layout(yaxis={'categoryorder': 'total ascending'})
        contenido = html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '18px'}, children=[
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_pais)]),
            html.Div(style={'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px'}, children=[dcc.Graph(figure=fig_pais_pop)])
        ])

    return kpis, contenido

if __name__ == '__main__':
    app.run(debug=True, port=8050)
