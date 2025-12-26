import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import sys

# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.constantes import data_out_path

path_hogar = data_out_path / "usu_hogar.csv"


def elegir_anio(path_hogar):
    """
    Permite al usuario seleccionar un año de los datos disponibles en un archivo CSV, usando un widget de Streamlit.

    Parámetros:
    -----------
    path_hogar : str
        Ruta al archivo CSV de hogares.

    Retorna:
    --------
    str
        El año seleccionado por el usuario (como cadena), o 'Todos' si se eligió esa opción.
    """
    df = pd.read_csv(path_hogar, sep=";", usecols=["ANO4"], encoding="utf-8")
    anios = sorted(df["ANO4"].dropna().unique().astype(str))
    anios.insert(0, "Todos")
    option = st.selectbox("Elija un año a procesar", (anios))
    return option


anio = elegir_anio(path_hogar)


def inciso1_4_1(path_hogar, anio):
    """
    Muestra en pantalla (usando Streamlit) la cantidad total de viviendas para un año específico
    a partir del archivo de datos de hogares.

    Parámetros:
    ----------
    path_hogar : str
        Ruta al archivo CSV que contiene los datos de hogares.

    anio : str
        Año seleccionado por el usuario. Si se pasa 'Todos', se contabilizan todas las viviendas
        independientemente del año.

    Retorna:
    -------
    None
    """
    df = pd.read_csv(path_hogar, delimiter=";", encoding="utf-8")

    # evaluo el año que se seleccionó
    if anio != "Todos":
        df_por_anio = df[df["ANO4"].astype(str) == anio]
    else:
        df_por_anio = df
    cant_hogares = len(df_por_anio)

    # muestro la cantidad de viviendas de ese año
    st.markdown(f"### Cantidad total de viviendas para el año: {anio}")
    st.write(f"**{cant_hogares}** viviendas")


inciso1_4_1(path_hogar, anio)


def inciso1_4_2(path_hogar, anio):
    """
    Calcula y grafica la proporción de tipos de hogares según el tipo de vivienda para un año específico
    o para todos los años, a partir de un archivo CSV de hogares.

    Parámetros:
    ----------
    path_hogar : str
        Ruta al archivo CSV con los datos de hogares.

    anio : str
        Año seleccionado para filtrar los datos.

    Variables internas:
    -------------------
    tipo_vivienda : dict
        Diccionario que mapea los códigos de tipo de vivienda a sus descripciones textuales.

    Retorna:
    -------
    None
    """
    tipo_vivienda = {
        1: "Casa",
        2: "Departamento",
        3: "Pieza de inquilinato",
        4: "Pieza de hotel/Pension",
        5: "Local no construido para habitación",
    }

    df = pd.read_csv(path_hogar, delimiter=";", encoding="utf-8")

    if anio != "Todos":
        df_filtro = df[df["ANO4"].astype(str) == anio]
    else:
        df_filtro = df.copy()

    df_filtro["tipo_vivienda"] = df_filtro["IV1"].map(tipo_vivienda)

    # Calculo cuantos hogares hay de cada tipo
    conteo = (
        df_filtro.groupby("tipo_vivienda")["PONDERA"].sum().sort_values(ascending=False)
    )

    # gráfico
    plt.figure(figsize=(10, 4))
    plt.pie(
        conteo,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#FF5733", "#33FF57", "#F0E68C", "#00054D", "#6F00FF"],
    )
    plt.title(f"Proporción de tipos de hogares - Año {anio}")
    plt.legend(labels=conteo.index, loc="lower right", title="Tipo de hogar")
    plt.ylabel("")  # Eliminar etiqueta del eje y
    plt.axis("equal")  # Asegura que el gráfico sea un círculo
    plt.tight_layout()
    st.pyplot(plt)


inciso1_4_2(path_hogar, anio)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Tipo de piso por aglomerado",
        "Regimen de tenencias",
        "Proporción viviendas c/baño",
        "Viviendas en villa",
        "Porcentaje de viviendas",
    ]
)

with tab1:

    def inciso1_4_3(path_hogar, option):
        """
        Muestra el material predominante en los pisos interiores de las viviendas por aglomerado para un año dado.

        Parámetros:
        -----------
        path_hogar : str
        Ruta al archivo CSV que contiene los datos de hogares.
        option : str
        Año seleccionado para filtrar los datos.

        Retorna:
        --------
        None
        """
        try:
            df = pd.read_csv(
                path_hogar,
                sep=";",
                usecols=["ANO4", "AGLOMERADO", "IV3"],
                encoding="utf-8",
            )
        except FileNotFoundError:
            st.error("No se encontró el archivo. Verifique la ruta.")
            return
        except pd.errors.EmptyDataError:
            st.error("El archivo está vacío.")
            return
        aglomerados_str = {
            2: "2.Gran La Plata",
            3: "3.Bahía Blanca - Cerri",
            4: "4.Gran Rosario",
            5: "5.Gran Santa Fé",
            6: "6.Gran Paraná",
            7: "7.Posadas",
            8: "8.Gran Resistencia",
            9: "9.Comodoro Rivadavia - Rada Tilly",
            10: "10.Gran Mendoza",
            12: "12.Corrientes",
            13: "13.Gran Córdoba",
            14: "14.Concordia",
            15: "15.Formosa",
            17: "17.Neuquén - Plottier",
            18: "18.Santiago del Estero - La Banda",
            19: "19.Jujuy - Palpalá",
            20: "20.Río Gallegos",
            22: "22.Gran Catamarca",
            23: "23.Gran Salta",
            25: "25.La Rioja",
            26: "26.Gran San Luis",
            27: "27.Gran San Juan",
            29: "29.Gran Tucumán - Tafí Viejo",
            30: "30.Santa Rosa - Toay",
            31: "31.Ushuaia - Río Grande",
            32: "32.Ciudad Autonoma de Buenos Aires",
            33: "33.Partidos del GBA",
            34: "34.Mar del Plata",
            36: "36.Río Cuarto",
            38: "38.San Nicolás - Villa Constitución",
            91: "91.Rawson - Trelew",
            93: "93.Viedma - Carmen de Patagones",
        }
        if option != "Todos":
            df_anio = df[df["ANO4"].astype(str) == option]
        else:
            df_anio = df

        if df_anio.empty:
            st.warning(f"No hay datos disponibles para el año seleccionado: {option}")
            return

        categorias = {
            1: "mosaico/baldosa/madera/cerámica/alfombra",
            2: "cemento/ladrillo fijo",
            3: "ladrillo suelto/tierra",
            4: "otro",
        }
        # agg aplicar 1 o + funciones de agregacion a df,idmax para saber cual se repite mas.
        resultados = (
            df_anio.groupby("AGLOMERADO")["IV3"]
            .agg(lambda x: x.value_counts().idxmax())
            .replace(categorias)
        )

        if resultados.empty:
            st.warning("No se pudo determinar el material predominante.")
            return

        # puedo usar map en lugar de replace pero si hay un valor que no este en el dict lo convierte a Nan
        resultados.index = resultados.index.map(aglomerados_str)
        st.subheader(
            "Material predominante en los pisos interiores de las viviendas por aglomerado cargado:"
        )
        st.dataframe(resultados)

    inciso1_4_3(path_hogar, anio)

with tab2:

    def inciso1_4_5(path_hogar, option):
        """
        Analiza y visualiza la evolución de los tipos de tenencia de viviendas en aglomerados urbanos seleccionados.

        Parámetros:
        -----------
        path_hogar : str
        Ruta al archivo CSV con datos de hogares.
        Año seleccionado para filtrar los datos. Puede ser un año específico o 'Todos' para incluir todos los años.

        Retorna:
        --------
        None
        """
        try:
            df = pd.read_csv(
                path_hogar,
                sep=";",
                usecols=["ANO4", "TRIMESTRE", "AGLOMERADO", "II7"],
                encoding="utf-8",
            )
        except FileNotFoundError:
            st.error("No se encontró el archivo. Verifique la ruta.")
            return
        except pd.errors.EmptyDataError:
            st.error("El archivo está vacío.")
            return

        if option != "Todos":
            df_anio = df[df["ANO4"].astype(str) == option]
        else:
            df_anio = df

        tenencias = {
            1: "Propietario de la vivienda y el terreno",
            2: "Propietario de la vivienda solamente",
            3: "Inquilino / arrendatario de la vivienda",
            4: "Ocupante por pago de impuestos / expensas",
            5: "Ocupante en relación de dependencia",
            6: "Ocupante gratuito (con permiso)",
            7: "Ocupante de hecho (sin permiso)",
            8: "Está en sucesión",
        }
        aglomerados_str = {
            2: "2.Gran La Plata",
            3: "3.Bahía Blanca - Cerri",
            4: "4.Gran Rosario",
            5: "5.Gran Santa Fé",
            6: "6.Gran Paraná",
            7: "7.Posadas",
            8: "8.Gran Resistencia",
            9: "9.Comodoro Rivadavia - Rada Tilly",
            10: "10.Gran Mendoza",
            12: "12.Corrientes",
            13: "13.Gran Córdoba",
            14: "14.Concordia",
            15: "15.Formosa",
            17: "17.Neuquén - Plottier",
            18: "18.Santiago del Estero - La Banda",
            19: "19.Jujuy - Palpalá",
            20: "20.Río Gallegos",
            22: "22.Gran Catamarca",
            23: "23.Gran Salta",
            25: "25.La Rioja",
            26: "26.Gran San Luis",
            27: "27.Gran San Juan",
            29: "29.Gran Tucumán - Tafí Viejo",
            30: "30.Santa Rosa - Toay",
            31: "31.Ushuaia - Río Grande",
            32: "32.Ciudad Autonoma de Buenos Aires",
            33: "33.Partidos del GBA",
            34: "34.Mar del Plata",
            36: "36.Río Cuarto",
            38: "38.San Nicolás - Villa Constitución",
            91: "91.Rawson - Trelew",
            93: "93.Viedma - Carmen de Patagones",
        }
        aglo = sorted(df_anio["AGLOMERADO"].dropna().unique())
        selected = st.selectbox(
            "Elija uno de los aglomerados disponibles para el año seleccionado",
            aglo,
            format_func=lambda x: aglomerados_str.get(x, f"Aglomerado {x}"),
        )
        df_aglo = df_anio[df_anio["AGLOMERADO"] == selected].copy()
        tenencias_options = ["Todas"] + list(tenencias.values())  # Agregar 'Todas'
        # convierto a list pq multiselet espera un iterable
        # selecciono una o mas tenencias
        selected_tenencias = st.multiselect(
            "Selecciona los tipos de tenencia:", tenencias_options
        )

        df_aglo["Tenencia"] = df_aglo["II7"].map(tenencias)

        if "Todas" in selected_tenencias:
            # Si selecciono 'Todas' incluyo todas las tenencias
            selected_tenencias = list(tenencias.values())
        else:
            # Uso solo las tenencias seleccionadas
            selected_tenencias = [t for t in selected_tenencias if t != "Todas"]

        # Filtro por tenencias seleccionadas
        if selected_tenencias:
            df_aglo = df_aglo[df_aglo["Tenencia"].isin(selected_tenencias)]

        df_aglo["AnoTrimestre"] = (
            df_aglo["ANO4"].astype(str) + ", Tri:" + df_aglo["TRIMESTRE"].astype(str)
        )
        # calulo la evolucion por año
        # con unstack convierto el añio en indice y las tenencias como columnas, fill x si esta vacio o es NaN
        evolucion = (
            df_aglo.groupby(["AnoTrimestre", "Tenencia"])["Tenencia"]
            .count()
            .unstack(fill_value=0)
        )
        evolucion = evolucion.sort_index()
        st.subheader("Evolucion de las tenencias seleccionadas en el año elegido:")
        # st.line_chart(evolucion)
        evolucion_reset = evolucion.reset_index().melt(
            id_vars="AnoTrimestre", var_name="Tenencia", value_name="Cantidad"
        )

        fig = px.line(
            evolucion_reset,
            x="AnoTrimestre",
            y="Cantidad",
            color="Tenencia",
            markers=True,
            title="Evolución de las tenencias seleccionadas",
            labels={
                "AnoTrimestre": "Año, Trimestre",
                "Cantidad": "Cantidad de viviendas",
            },
        )

        # etiquetas eje X (rotación)
        fig.update_layout(
            xaxis_tickangle=0,
            xaxis=dict(tickmode="linear"),
            legend_title_text="Tipo de Tenencia",
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

    inciso1_4_5(path_hogar, anio)

with tab3:

    def inciso1_4_4(path_hogar, anio):
        """
        Calcula y grafica la proporción de viviendas con baño dentro del hogar por aglomerado,
        para un año específico o para todos los años, a partir de un archivo CSV de hogares.

        Parámetros:
        ----------
        path_hogar : str
            Ruta al archivo CSV que contiene los datos de hogares.

        anio : str
            Año seleccionado para filtrar los datos. Si se pasa el valor 'Todos', se consideran
            todos los años disponibles en el archivo.

        Retorna:
        -------
        None
        """
        df = pd.read_csv(path_hogar, delimiter=";", encoding="utf-8")
        aglomerados_str = {
            2: "2.Gran La Plata",
            3: "3.Bahía Blanca - Cerri",
            4: "4.Gran Rosario",
            5: "5.Gran Santa Fé",
            6: "6.Gran Paraná",
            7: "7.Posadas",
            8: "8.Gran Resistencia",
            9: "9.Comodoro Rivadavia - Rada Tilly",
            10: "10.Gran Mendoza",
            12: "12.Corrientes",
            13: "13.Gran Córdoba",
            14: "14.Concordia",
            15: "15.Formosa",
            17: "17.Neuquén - Plottier",
            18: "18.Santiago del Estero - La Banda",
            19: "19.Jujuy - Palpalá",
            20: "20.Río Gallegos",
            22: "22.Gran Catamarca",
            23: "23.Gran Salta",
            25: "25.La Rioja",
            26: "26.Gran San Luis",
            27: "27.Gran San Juan",
            29: "29.Gran Tucumán - Tafí Viejo",
            30: "30.Santa Rosa - Toay",
            31: "31.Ushuaia - Río Grande",
            32: "32.Ciudad Autonoma de Buenos Aires",
            33: "33.Partidos del GBA",
            34: "34.Mar del Plata",
            36: "36.Río Cuarto",
            38: "38.San Nicolás - Villa Constitución",
            91: "91.Rawson - Trelew",
            93: "93.Viedma - Carmen de Patagones",
        }

        if anio != "Todos":
            df_filtro = df[df["ANO4"].astype(str) == anio]
        else:
            df_filtro = df.copy()

        # agrupo los hogares con baño por aglomerado y el total de hogares por aglomerado
        baño = df_filtro[df_filtro["IV8"] == 1].groupby("AGLOMERADO").size()
        total = df_filtro.groupby("AGLOMERADO").size()

        # calculo
        proporcion = ((baño / total) * 100).round(2).reset_index()
        proporcion.columns = ["AGLOMERADO", "Proporcion"]

        proporcion["AGLOMERADO"] = proporcion["AGLOMERADO"].map(aglomerados_str)
        proporcion["Proporcion"] = proporcion["Proporcion"].astype(str) + "%"

        # Muestro tabla
        st.subheader(f"Proporción de viviendas con baño dentro del hogar - Año {anio}")
        st.dataframe(proporcion.set_index("AGLOMERADO"))

    inciso1_4_4(path_hogar, anio)

with tab4:

    def inciso1_4_6(path_hogar, anio):
        """
        Informa ordenadamente la cantidad de viviendas en villa de emergencia por aglomerado,
        y su porcentaje respecto al total.
        """
        df = pd.read_csv(
            path_hogar,
            sep=";",
            encoding="utf-8",
            usecols=["ANO4", "AGLOMERADO", "IV12_3", "PONDERA"],
        )

        if anio != "Todos":
            df = df[df["ANO4"].astype(str) == anio]

        # Crear columna booleana: True si está en villa
        df["en_villa"] = df["IV12_3"] == 1

        # Agrupar total de viviendas y las que están en villa
        total = df.groupby("AGLOMERADO")["PONDERA"].sum()
        en_villa = df[df["en_villa"]].groupby("AGLOMERADO")["PONDERA"].sum()

        # Armar tabla de resultados
        resultado = pd.DataFrame(
            {"Viviendas en villa": en_villa, "Total viviendas": total}
        )

        resultado["Porcentaje (%)"] = (
            resultado["Viviendas en villa"] / resultado["Total viviendas"] * 100
        ).round(2)
        resultado = resultado.fillna(0).sort_values(
            by="Viviendas en villa", ascending=False
        )

        st.subheader(f"Viviendas en villa de emergencia por aglomerado - Año {anio}")
        st.dataframe(resultado)

    inciso1_4_6(path_hogar, anio)

with tab5:

    def agregar_condicion_de_habitabilidad(df):
        """
        Agrega una columna 'CONDICION_DE_HABITABILIDAD' al DataFrame basado en las condiciones
        de las columnas IV6 a IV10 según las reglas especificadas.

        Parámetros
        ----------
        df : pd.DataFrame
            DataFrame que contiene las columnas IV6, IV7, IV8, IV9, IV10.

        Retorna
        -------
        pd.DataFrame
            DataFrame con la nueva columna 'CONDICION_DE_HABITABILIDAD'.
        """

        # si cambio el orden se sobrescriben Buenas y salubles y quedan como insuficiente
        df["CONDICION_DE_HABITABILIDAD"] = "Insuficiente"
        condiciones = [
            (df["IV6"].between(1, 3))
            & (df["IV7"].between(1, 3))
            & (df["IV8"] == 1)
            & (df["IV9"].between(1, 3))
            & (df["IV10"].between(1, 3)),
            (df["IV6"].between(1, 2))
            & (df["IV7"].between(1, 2))
            & (df["IV8"] == 1)
            & (df["IV9"].between(1, 2))
            & (df["IV10"].between(1, 2)),
            (df["IV6"] == 1)
            & (df["IV7"] == 1)
            & (df["IV8"] == 1)
            & (df["IV9"] == 1)
            & (df["IV10"] == 1),
        ]
        valores = ["Regular", "Saludable", "Buena"]

        for condicion, valor in zip(condiciones, valores):
            df.loc[condicion, "CONDICION_DE_HABITABILIDAD"] = valor

        return df

    def inciso1_4_7(path_hogar, anio):
        """
        Calcula y visualiza el porcentaje de viviendas por condición de habitabilidad en cada aglomerado
        para un año específico o para todos los años, utilizando datos de hogares.

        La condición de habitabilidad es determinada por la función auxiliar `agregar_condicion_de_habitabilidad()`,
        que clasifica los hogares en categorías como 'Buena', 'Saludable', 'Regular' o 'Insuficiente', según
        las condiciones del entorno del hogar (como materiales, baño, agua, etc.).

        Parámetros
        ----------
        path_hogar : str
            Ruta al archivo CSV con los datos de hogares.

        anio : str
            Año a analizar. Si se pasa el valor 'Todos', se consideran todos los años disponibles en el dataset.

        Retorna
        -------
        None
        """
        df1 = pd.read_csv(path_hogar, sep=";", encoding="utf-8")

        df = agregar_condicion_de_habitabilidad(df1)

        columnas = ["ANO4", "AGLOMERADO", "CONDICION_DE_HABITABILIDAD", "PONDERA"]
        df = df[columnas]

        # Filtro por año si no es "Todos"
        if anio != "Todos":
            df_filtro = df[df["ANO4"].astype(str) == anio]
        else:
            df_filtro = df.copy()

        # calculo de porcentajes
        grouped = df_filtro.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"])[
            "PONDERA"
        ].sum()
        total_por_aglo = grouped.groupby(level=0).sum()
        porcentaje = (grouped / total_por_aglo) * 100
        porcentaje = porcentaje.round(2).reset_index(name="PORCENTAJE")

        # Streamlit
        st.subheader(
            f"Porcentaje de viviendas por condición de habitabilidad y aglomerado {anio}"
        )

        tabla_pivot = porcentaje.pivot(
            index="AGLOMERADO",
            columns="CONDICION_DE_HABITABILIDAD",
            values="PORCENTAJE",
        ).fillna(0)
        st.dataframe(tabla_pivot)

        # Gráfico
        plt.figure(figsize=(12, 6))
        for condicion in porcentaje["CONDICION_DE_HABITABILIDAD"].unique():
            subset = porcentaje[porcentaje["CONDICION_DE_HABITABILIDAD"] == condicion]
            plt.bar(
                subset["AGLOMERADO"].astype(str), subset["PORCENTAJE"], label=condicion
            )

        plt.xlabel("Aglomerado")
        plt.ylabel("Porcentaje (%)")
        plt.title(
            f"Porcentaje de viviendas por condición de habitabilidad - Año {anio}"
        )
        plt.xticks(rotation=45)
        plt.legend(title="Condición")
        plt.tight_layout()
        st.pyplot(plt)

        # Botón para exportar CSV
        csv = porcentaje.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar resultados en formato CSV",
            data=csv,
            file_name=f"porcentaje_habitabilidad_{anio}.csv",
            mime="text/csv",
        )

    inciso1_4_7(path_hogar, anio)
