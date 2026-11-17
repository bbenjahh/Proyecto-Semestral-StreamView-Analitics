"""
Módulo de Integración y Limpieza de Datos - StreamView Analytics (EP5)
Autores: Benjamin Patiño & Benjamin Vargas
Asignatura: Visualización de Datos (ADY1104) - Duoc UC
"""
import pandas as pd

def load_and_merge_datasets(tv_path: str, movies_path: str) -> pd.DataFrame:
    df_tv = pd.read_csv(tv_path)
    df_movies = pd.read_csv(movies_path)

    df_tv['tipo_contenido'] = 'TV Show'
    df_movies['tipo_contenido'] = 'Movie'

    cols_comunes = [
        'show_id', 'tipo_contenido', 'title', 'country', 'date_added',
        'release_year', 'genres', 'language', 'popularity', 'vote_count', 'vote_average'
    ]
    df_master = pd.concat([df_tv[cols_comunes], df_movies[cols_comunes]], ignore_index=True)

    # Imputación de valores nulos categóricos
    for col in ['country', 'genres', 'language']:
        df_master[col] = df_master[col].fillna('Unknown')

    # Conversión temporal y limpieza
    df_master['date_added'] = pd.to_datetime(df_master['date_added'], errors='coerce')
    df_master = df_master.dropna(subset=['date_added'])

    # Feature Engineering para análisis visual
    df_master['año_agregado'] = df_master['date_added'].dt.year
    df_master['mes_agregado'] = df_master['date_added'].dt.month
    df_master['genero_principal'] = df_master['genres'].apply(lambda x: str(x).split(',')[0].strip())
    df_master['pais_principal'] = df_master['country'].apply(lambda x: str(x).split(',')[0].strip())

    # Eliminación de duplicados por identificador único
    df_master = df_master.drop_duplicates(subset=['show_id']).reset_index(drop=True)
    return df_master
