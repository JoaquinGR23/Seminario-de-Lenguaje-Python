import streamlit as st
from pathlib import Path
import pandas as pd
import sys
# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.constantes import data_out_path
path_canasta = data_out_path/'canasta-basica.csv'
path_hogar = data_out_path/'usu_hogar.csv'
def inciso7_1(path_hogar, path_canasta):
    """solicita al usuario que ingrese un año y trimestre y a partir de esta información 
    informar la cantidad y porcentajes de hogares de 4  integrantes que se encuentran por debajo de la línea de 
    pobreza y por debajo de la línea de indigencia.Para esto:
    -filtra por el año y trimestre elegido.
    -asigna los meses de del csv de la canasta al trimestre correspondiente del csv hogar.
    -calculo el porcentaje de hogares por debajo de la linea de pobreza e indigencia y 
    despues la cantidad de hogares
    """
    df_hogar = pd.read_csv(
        path_hogar,
        sep=";",
        usecols=["ANO4", "TRIMESTRE", "IX_TOT", "ITF", "CODUSU", "NRO_HOGAR"],
        encoding="utf-8",
    )
    df_canasta = pd.read_csv(
        path_canasta,
        sep=",",
        usecols=["indice_tiempo", "linea_indigencia", "linea_pobreza"],
        encoding="utf-8",
    )
    # copio el dataset para no modificar el original
    df_canasta_copia = df_canasta.copy()
    # convierto a datetime para poder extraer año y meses
    df_canasta_copia["indice_tiempo"] = pd.to_datetime(df_canasta_copia["indice_tiempo"], format="%Y-%m-%d")
    df_canasta_copia["año"] = df_canasta_copia["indice_tiempo"].dt.year
    df_canasta_copia["mes"] = df_canasta_copia["indice_tiempo"].dt.month

    #filtro los años cargados y los ordeno
    anios_disponibles = df_hogar["ANO4"].dropna().unique()
    anios_disponibles.sort()
    # elijo año
    anio_usuario = st.selectbox("Seleccione un año:", anios_disponibles)
    # creo un dataset con los datos del año que selecciono el usuario
    df_anio = df_hogar[df_hogar["ANO4"] == anio_usuario]
    # unique(trimestres del año seleccionado)
    trimestres_disponibles = sorted(df_anio["TRIMESTRE"].dropna().unique())
    # elijo el trimestre que quiero
    trimestre_usuario = st.selectbox("Seleccione un trimestre:", trimestres_disponibles)

    # Filtrar por año y trimestre
    df_filtrado = df_hogar[
        (df_hogar["ANO4"] == anio_usuario)
        & (df_hogar["TRIMESTRE"] == trimestre_usuario)
        & (df_hogar["IX_TOT"] == 4)
    ]
    # diccionario con los mese correspondientes a cada trimestre
    dict_trimestre = {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9], 4: [10, 11, 12]}
    # le asigno los meses a considerar del trimestre elegido por el usuario
    key_meses = dict_trimestre[trimestre_usuario]

    # calculo la media de la linea de pobreza e indigencia para esos años
    promedio_pobreza = df_canasta_copia[
        (df_canasta_copia["año"] == anio_usuario)
        & (df_canasta_copia["mes"].isin(key_meses))
    ]["linea_pobreza"].mean()
    promedio_indigencia = df_canasta_copia[
        (df_canasta_copia["año"] == anio_usuario)
        & (df_canasta_copia["mes"].isin(key_meses))
    ]["linea_indigencia"].mean()

    # calculo la cantidad de hogares
    cantidad_pobres = (df_filtrado["ITF"] < promedio_pobreza).sum()
    cantidad_indigentes = (df_filtrado["ITF"] < promedio_indigencia).sum()
    # cantidad total de hogares de 4 integrantes para ese año y trimestre
    total_hogares = len(df_filtrado)
    # calculo el porcentaje
    if pd.isna(total_hogares) or total_hogares == 0:
        st.warning("No hay datos disponibles para calcular el promedio.")
    else:
        porcentaje_pobres = (cantidad_pobres / total_hogares) * 100
        porcentaje_indigentes = (cantidad_indigentes / total_hogares) * 100

    # imprimo resultados
    st.metric(label="Cantidad de hogares (de 4 integrantes) pobres", value=cantidad_pobres)
    st.metric(label="Cantidad de hogares (de 4 integrantes) indigentes", value=cantidad_indigentes)

    st.metric(label="Porcentaje de pobreza", value=f"{porcentaje_pobres:.2f}%")
    st.metric(label="Porcentaje de indigencia", value=f"{porcentaje_indigentes:.2f}%")

inciso7_1(path_hogar,path_canasta)