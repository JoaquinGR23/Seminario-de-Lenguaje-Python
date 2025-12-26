import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import sys
# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.constantes import data_out_path
path_individual = data_out_path/'usu_individual.csv'
tab1,tab2,tab3 = st.tabs (['Distribucion poblacional por edad y sexo','Edad promedio por aglomerado','Evolución dependencia'])

with tab1:
    def inciso1_3_1(path_individual):
        """ Lee el archivo CSV usu_individual.csv, calcula la edad a partir del año de nacimiento,
        filtra los datos por año y trimestre ingresados por el usuario, agrupa la población en
        intervalos de edad de 10 años y grafica la distribución poblacional por sexo.

        Pasos principales:
        - Carga el archivo 'usu_individual.csv'.
        - Extrae el año de nacimiento desde la columna 'CH05' y calcula la edad.
        - Filtra datos con edades entre 0 y 110 años.
        - Mapea el código de sexo a 'Varón' y 'Mujer'.
        - Solicita al usuario un año y un trimestre válidos para filtrar los datos.
        - Agrupa los datos por grupos etarios de 10 años y por sexo, ponderando por la columna 'pondera'.
        - Genera un gráfico de barras apiladas mostrando la distribución poblacional por sexo y edad.

        return none
        """
        # uso use cols para no recorrer todo el archivo, excepcion por si el archivo no esta
        try:
            df = pd.read_csv(path_individual,sep=';', usecols=['CH05', 'ANO4', 'TRIMESTRE', 'CH04','PONDERA'])
        except FileNotFoundError:
            st.error("No se encontró el archivo. Verifique la ruta.")
            return
        except pd.errors.EmptyDataError:
            st.error("El archivo está vacío.")
            return
        # busca los 4 digitos consecutivos (año) y lo convierte a float(pq acepta NaN)
        df['anio_nac'] = df['CH05'].str.extract(r'(\d{4})').astype(float)

        # calculo edad
        df['edad'] = df['ANO4'] - df['anio_nac']

        # filtro x edades entre 0-110 años
        df = df[(df['edad'] >= 0) & (df['edad'] <= 110)]

        # mapeo sexo tmb puede ser con ch04_str
        df['sexo'] = df['CH04'].map({1: 'Varón', 2: 'Mujer'})
    
        # Obtengo los años sin repeticiones y los ordeno
        anios_disponibles = df['ANO4'].dropna().unique()
        anios_disponibles.sort()

        anio_usuario = st.selectbox("Seleccione un año:", anios_disponibles)
        # creo un dataset con los datos del año que selecciono el usuario
        df_anio = df[df['ANO4'] == anio_usuario]
        # unique(trimestres del año seleccionado)
        trimestres_disponibles = sorted(df_anio['TRIMESTRE'].dropna().unique())
        # elijo el trimestre que quiero
        trimestre_usuario = st.selectbox("Seleccione un trimestre:", trimestres_disponibles)

        # Filtrar por año y trimestre
        df_filtrado = df[(df['ANO4'] == anio_usuario) & (df['TRIMESTRE'] == trimestre_usuario)]

        # en caso de que este vacio
        if df_filtrado.empty:
            st.warning("No hay datos para el año y trimestre seleccionados.")
            return

        # Crear grupos de edad de 10 en 10
        bins = range(0, 110, 10) # bins = limite de intervalos,pd.cut()
        labels = [f'{i}-{i+9}' for i in bins[:-1]] # ej 0-9
        df_filtrado['grupo_edad'] = pd.cut(df_filtrado['edad'], bins=bins, labels=labels, right=False)

        # agrupo x edad y sexo usando pondera. Uso unstack por el grafico de barras dobles, si hay valores Nan los pongo en 0?
        df_grouped = df_filtrado.groupby(['grupo_edad', 'sexo'])['PONDERA'].sum().unstack(fill_value=0)

        # Graficar
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Ancho de las barras
        x = range(len(labels))  # Posiciones para las barras

        # Dibujar barras para Varón y Mujer
        ax.bar([i - bar_width/2 for i in x], df_grouped.get('Varón', 0), bar_width, label='Varón', color='blue')
        ax.bar([i + bar_width/2 for i in x], df_grouped.get('Mujer', 0), bar_width, label='Mujer', color='pink')
        ax.set_xticks(x) # def las posiciones de x donde van a ir las labels
        ax.set_xticklabels(labels) # asigna las labels a las pos definidas en set_xticks
        plt.title(f'Distribución poblacional por edad y sexo\nAño {anio_usuario}, Trimestre {trimestre_usuario}')
        plt.xlabel('Grupo de Edad')
        plt.ylabel('Población estimada (ponderada)')
        plt.xticks(rotation=45)
        plt.legend(title='Sexo')
        plt.tight_layout() # ajusta margenes

        st.pyplot(fig)
    inciso1_3_1(path_individual)

def media_ponderada(grupo):
    """
    Calcula la media ponderada de la edad en un grupo de datos, usando como peso la columna 'PONDERA'.

    Parámetros:
    ----------
    grupo : pandas.DataFrame

    Retorna:
    -------
    float or None
        La media ponderada de la edad. Devuelve `None` si la suma de los pesos es cero.
    """
    suma_ponderada = (grupo['edad'] * grupo['PONDERA']).sum()
    suma_pesos = grupo['PONDERA'].sum()
    return suma_ponderada / suma_pesos if suma_pesos != 0 else None

def mediana_ponderada(grupo):
    """
    Calcula la mediana ponderada de la edad en un grupo de datos, utilizando la columna 'PONDERA' como peso.

    Parámetros:
    ----------
    grupo : pandas.DataFrame

    Retorna:
    -------
    float
        Valor de la mediana ponderada de la edad. 
    """
    grupo = grupo[['edad', 'PONDERA']].dropna().sort_values('edad')
    grupo['cum_pondera'] = grupo['PONDERA'].cumsum()
    total = grupo['PONDERA'].sum()
    mitad = total / 2
    mediana = grupo[grupo['cum_pondera'] >= mitad].iloc[0]['edad']
    return mediana

def inciso_1_3_4(path_individual):
    """
    Calcula la media y mediana ponderada de la edad para cada combinación de año y trimestre
    a partir de un archivo CSV con datos individuales.

    Parámetros:
    -----------
    path_individual : str
        Ruta al archivo CSV que contiene los datos individuales. 

    Retorna:
    --------
    pandas.DataFrame
    """
    df = pd.read_csv(path_individual, sep=';', usecols=['CH05', 'ANO4', 'TRIMESTRE', 'CH04', 'PONDERA'])
    df['anio_nac'] = df['CH05'].str.extract(r'(\d{4})').astype(float)
    df['edad'] = df['ANO4'] - df['anio_nac']
    df = df[(df['edad'] >= 0) & (df['edad'] <= 110)]

    media = df.groupby(['ANO4', 'TRIMESTRE']).apply(media_ponderada).reset_index(name='media_ponderada')
    mediana = df.groupby(['ANO4', 'TRIMESTRE']).apply(mediana_ponderada).reset_index(name='mediana_ponderada')

    resultado = pd.merge(media, mediana, on=['ANO4', 'TRIMESTRE'])
    return resultado

st.title("Características Demográficas - Media y Mediana Ponderadas de Edad")

resultado = inciso_1_3_4(path_individual)
st.dataframe(resultado)

with tab2:
    def inciso1_3_2(path_individual):
        """
        Calcula y grafica la edad promedio ponderada por aglomerado para el último año y trimestre disponible en los datos.

        Parámetros:
        -----------
        path_individual : str
        Ruta al archivo CSV que contiene los datos individuales con las columnas:
        'AGLOMERADO' (zona o área geográfica),
        'CH06' (edad),
        'ANO4' (año),
        'TRIMESTRE' (trimestre),
        'PONDERA' (peso para ponderación).

        Retorna:
        --------
        None
        """
        try:
            df = pd.read_csv(path_individual,sep=';', usecols=['AGLOMERADO','CH06','ANO4','TRIMESTRE','PONDERA'],encoding='utf-8')
        except FileNotFoundError:
            st.error("No se encontró el archivo. Verifique la ruta.")
            return
        except pd.errors.EmptyDataError:
            st.error("El archivo está vacío.")
            return
        # filtro por ultimo año y trimestre cargado
        anios = df['ANO4'].dropna().unique()
        maxA = anios.max()
        trimestre = df[df['ANO4'] == maxA]['TRIMESTRE'].dropna().unique()
        maxT = trimestre.max() 

        df_fecha =df[(df['ANO4'] == maxA) & (df['TRIMESTRE'] == maxT)]
        # calculo la media
        def media():
             df_fecha.groupby(['PONDERA','CH06']).mean()
    
        # calculo edad promedio por aglomerado
        resultados = df_fecha.groupby('AGLOMERADO').apply( 
             lambda x: (x['CH06'] * x['PONDERA']).sum() / x['PONDERA'].sum()).reset_index(name='EDAD PROMEDIO') 
        resultados['EDAD PROMEDIO'] = resultados['EDAD PROMEDIO'].round(0)
        if resultados.empty:
            return
        sorted(df['AGLOMERADO'].dropna().unique())
        st.write("Edad promedio por aglomerado:")
        st.line_chart(data=resultados, x='AGLOMERADO', y='EDAD PROMEDIO',color='#AA75EB') 
    inciso1_3_2(path_individual)

with tab3:
    def clasificar_edad(edad):
        """
        Clasifica una edad individual en uno de tres grupos etarios: '0-14', '15-64' o '65+'.

        Parámetros:
        ----------
        edad : int or float
            Edad de la persona a clasificar.

        Retorna:
        -------
        un valor tipo Str 
        """
        if edad <= 14:
            return "0-14"
        elif edad <= 64:
            return "15-64"
        else:
            return "65+"

    def inciso1_3_3(path_individual):
        """
        Calcula y grafica la evolución del índice de dependencia demográfica por aglomerado a partir de un archivo CSV.

        Parámetros:
        -----------
        path_individual : str
            Ruta al archivo CSV con los datos individuales de la EPH, delimitado por punto y coma.
            
        Retorna:
        --------
        None. Muestra el gráfico directamente en la interfaz de Streamlit.
        """
        df = pd.read_csv(path_individual,delimiter = ';', encoding = 'utf-8')

        #creo grupos por edad
        df['grupo_por_edad'] = df['CH06'].apply(clasificar_edad)

        #agrupo por aglomerado, año, trimestre y grupo de edad
        agrupar = (
            df.groupby(['AGLOMERADO','ANO4','TRIMESTRE','grupo_por_edad'])
            .size()
            .unstack(fill_value =0)
            .reset_index()
        )

        #calculo la dependencia = (('0-14'+'65+')/'15-64')*100
        agrupar['DEPENDENCIA'] = (
            (agrupar['0-14']+agrupar['65+']) / agrupar['15-64']
        )*100

        #creo columna de período
        agrupar['PERIODO'] = agrupar['ANO4'].astype(str)+" - T"+agrupar['TRIMESTRE'].astype(str)

        #selecciono un aglomerado y filtro por el mismo 
        aglomerados = agrupar['AGLOMERADO'].unique()
        aglo_sel = st.selectbox("Seleccione el aglomerado", options=aglomerados)
        df_aglo = agrupar[agrupar['AGLOMERADO'] == aglo_sel].sort_values(['ANO4','TRIMESTRE'])

        #gráfico de la evolución
        plt.figure(figsize=(10, 6))
        plt.plot(df_aglo['PERIODO'], df_aglo['DEPENDENCIA'], marker="o")
        plt.title(f"Evolución de la Dependencia Demográfica - Aglomerado {aglo_sel}")
        plt.xlabel("Período (Año-Trimestre)")
        plt.ylabel("Índice de dependencia (%)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)
    inciso1_3_3(path_individual)


