import streamlit as st
from pathlib import Path
import json
import folium
from streamlit_folium import st_folium
import pandas as pd
import sys
import matplotlib.pyplot as plt

# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.constantes import data_out_path, coords_agloms_path

path_persona = data_out_path / "usu_individual.csv"
path_coords_agloms = coords_agloms_path / "aglomerados_coordenadas.json"

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Personas desocupadas",
        "Evolución desempleo/empleo",
        "Tipo de empleo por aglomerado",
        "Evolución de tasas por aglomerado",
    ]
)

with tab1:

    def inciso1_5_1(path_persona):
        """
        Visualiza la cantidad de personas desocupadas según el nivel de estudios alcanzado
        para un año y trimestre seleccionados por el usuario.
        """
        df = pd.read_csv(
            path_persona,
            sep=";",
            encoding="utf-8",
            usecols=["ANO4", "TRIMESTRE", "ESTADO", "NIVEL_ED", "PONDERA"],
        )

        anios_disponibles = df["ANO4"].dropna().unique()
        anios_disponibles.sort()

        anio_usuario = st.selectbox("Seleccione un año:", anios_disponibles)
        df_anio = df[df["ANO4"] == anio_usuario]

        trimestres_disponibles = sorted(df_anio["TRIMESTRE"].dropna().unique())
        trimestre_usuario = st.selectbox(
            "Seleccione un trimestre:", trimestres_disponibles
        )

        # Filtro desocupados
        df_filtrado = df[
            (df["ANO4"] == anio_usuario)
            & (df["TRIMESTRE"] == trimestre_usuario)
            & (df["ESTADO"] == 2)
        ]

        # Mapear niveles educativos
        niveles_educativos = {
            1: "Sin instrucción",
            2: "Primaria incompleta",
            3: "Primaria completa",
            4: "Secundaria incompleta",
            5: "Secundaria completa",
            6: "Superior incompleto",
            7: "Superior completo",
        }
        df_filtrado["Nivel educativo"] = df_filtrado["NIVEL_ED"].map(niveles_educativos)

        conteo = (
            df_filtrado.groupby("Nivel educativo")["PONDERA"]
            .sum()
            .round(0)
            .sort_index()
        )

        # Streamlit
        st.subheader(
            f"Cantidad de personas desocupadas por nivel educativo - Año {anio_usuario}, Trimestre {trimestre_usuario}"
        )
        st.dataframe(conteo.reset_index().rename(columns={"PONDERA": "Cantidad"}))

        # Gráfico
        plt.figure(figsize=(10, 5))
        plt.bar(conteo.index, conteo.values, color="#E74C3C")
        plt.xticks(rotation=45)
        plt.ylabel("Cantidad estimada de personas")
        plt.title(
            f"Personas desocupadas según nivel educativo\nAño {anio_usuario}, Trimestre {trimestre_usuario}"
        )
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        st.pyplot(plt)

    inciso1_5_1(path_persona)

with tab2:

    def inciso1_5_2(path_persona):
        """
        Informa la evolución de la tasa de desempleo a lo largo del tiempo,
        con opción de filtrar por aglomerado.
        """
        df = pd.read_csv(
            path_persona,
            sep=";",
            encoding="utf-8",
            usecols=["ANO4", "TRIMESTRE", "AGLOMERADO", "ESTADO", "PONDERA"],
        )

        aglomerados = ["Todos"] + sorted(df["AGLOMERADO"].dropna().unique())
        filtro_aglomerado = st.selectbox(
            "Seleccione aglomerado (tasa de desempleo)", aglomerados
        )

        if filtro_aglomerado != "Todos":
            df = df[df["AGLOMERADO"] == filtro_aglomerado]

        resumen = df.groupby(["ANO4", "TRIMESTRE", "ESTADO"])["PONDERA"].sum().unstack()
        ocupados = resumen[1]
        desocupados = resumen[2]

        tasa_desempleo = (desocupados / (ocupados + desocupados) * 100).round(2)

        resultado = tasa_desempleo.reset_index(name="Tasa de desempleo (%)")

        st.subheader(f"Evolución tasa de desempleo - Aglomerado: {filtro_aglomerado}")
        st.dataframe(resultado)

        plt.figure(figsize=(10, 5))
        plt.plot(
            resultado["ANO4"].astype(str) + "T" + resultado["TRIMESTRE"].astype(str),
            resultado["Tasa de desempleo (%)"],
            marker="o",
        )
        plt.xticks(rotation=45)
        plt.ylabel("Tasa de desempleo (%)")
        plt.title("Evolución tasa de desempleo")
        plt.grid(True)
        st.pyplot(plt)

    inciso1_5_2(path_persona)

    def inciso1_5_3(path_persona):
        """
        Informa la evolución de la tasa de empleo a lo largo del tiempo,
        con opción de filtrar por aglomerado.
        """
        df = pd.read_csv(
            path_persona,
            sep=";",
            encoding="utf-8",
            usecols=["ANO4", "TRIMESTRE", "AGLOMERADO", "ESTADO", "PONDERA"],
        )

        aglomerados = ["Todos"] + sorted(df["AGLOMERADO"].dropna().unique())
        filtro_aglomerado = st.selectbox(
            "Seleccione aglomerado (tasa de empleo)", aglomerados
        )

        if filtro_aglomerado != "Todos":
            df = df[df["AGLOMERADO"] == filtro_aglomerado]

        resumen = df.groupby(["ANO4", "TRIMESTRE", "ESTADO"])["PONDERA"].sum().unstack()

        # Acceso directo: asumimos que siempre hay datos para estado 1 (ocupados) y 2 (desocupados)
        ocupados = resumen[1]
        desocupados = resumen[2]

        tasa_empleo = (ocupados / (ocupados + desocupados) * 100).round(2)
        resultado = tasa_empleo.reset_index(name="Tasa de empleo (%)")

        st.subheader(f"Evolución tasa de empleo - Aglomerado: {filtro_aglomerado}")
        st.dataframe(resultado)

        # Gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(
            resultado["ANO4"].astype(str) + "T" + resultado["TRIMESTRE"].astype(str),
            resultado["Tasa de empleo (%)"],
            marker="o",
            color="green",
        )
        plt.xticks(rotation=45)
        plt.ylabel("Tasa de empleo (%)")
        plt.title("Evolución tasa de empleo")
        plt.grid(True)
        st.pyplot(plt)

    inciso1_5_3(path_persona)

with tab3:

    def inciso1_5_4(path_individual):
        """
        Muestra una tabla y un gráfico de la distribución del tipo de empleo (Estatal, Privado, Otro)
        por aglomerado, a partir de un archivo CSV de datos individuales.

        Parámetros:
        ----------
        path_individual : str
            Ruta al archivo CSV que contiene los datos individuales, separado por punto y coma, codificado en UTF-8.

        Variables internas:
        -------------------
        aglomerados : dict
            Diccionario que mapea los códigos de aglomerados a sus nombres descriptivos.

        Retorna:
        -------
        None
        """
        aglomerados = {
            2: "Gran La Plata",
            3: "Bahía Blanca - Cerri",
            4: "Gran Rosario",
            5: "Gran Santa Fé",
            6: "Gran Paraná",
            7: "Posadas",
            8: "Gran Resistencia",
            9: "Comodoro Rivadavia - Rada Tilly",
            10: "Gran Mendoza",
            12: "Corrientes",
            13: "Gran Córdoba",
            14: "Concordia",
            15: "Formosa",
            17: "Neuquén - Plottier",
            18: "Santiago del Estero - La Banda",
            19: "Jujuy - Palpalá",
            20: "Río Gallegos",
            22: "Gran Catamarca",
            23: "Gran Salta",
            25: "La Rioja",
            26: "Gran San Luis",
            27: "Gran San Juan",
            29: "Gran Tucumán - Tafí Viejo",
            30: "Santa Rosa - Toay",
            31: "Ushuaia - Río Grande",
            32: "Ciudad Autonoma de Buenos Aires",
            33: "Partidos del GBA",
            34: "Mar del Plata",
            36: "Río Cuarto",
            38: "San Nicolás - Villa Constitución",
            91: "Rawson - Trelew",
            93: "Viedma - Carmen de Patagones",
        }

        # Cargar datos
        df = pd.read_csv(path_individual, sep=";", encoding="utf-8")

        # Filtrar personas ocupadas
        ocupados = df[df["ESTADO"] == 1].copy()

        # Clasificar tipo de empleo
        def clasificar_empleo(x):
            if x == 1:
                return "Estatal"
            elif x == 2:
                return "Privado"
            else:
                return "Otro"

        ocupados["tipo_empleo"] = ocupados["PP07H"].map(clasificar_empleo)

        # Agrupar por aglomerado y tipo de empleo
        tabla = (
            ocupados.groupby(["AGLOMERADO", "tipo_empleo"])["PONDERA"]
            .sum()
            .unstack(fill_value=0)
        )

        # Calcular total y porcentajes
        tabla["Total"] = tabla.sum(axis=1)
        tabla["Estatal"] = 100 * tabla.get("Estatal", 0) / tabla["Total"]
        tabla["Privado"] = 100 * tabla.get("Privado", 0) / tabla["Total"]
        tabla["Otro"] = 100 * tabla.get("Otro", 0) / tabla["Total"]

        # Crear nuevo DataFrame solo con porcentajes
        porcentajes = tabla[["Estatal", "Privado", "Otro"]].copy()

        # Reemplazar índices por nombres
        porcentajes.index = porcentajes.index.map(aglomerados)

        # Orden opcional por porcentaje estatal (puede cambiarse)
        porcentajes = porcentajes.sort_values("Estatal", ascending=False)

        # Mostrar tabla
        st.subheader("Distribución del tipo de empleo por aglomerado")
        st.dataframe(porcentajes.style.format("{:.2f}%"))

        # Gráfico
        porcentajes.plot(kind="bar", stacked=True, figsize=(18, 7), colormap="Set3")

        plt.title("Distribución del tipo de empleo por aglomerado")
        plt.xlabel("Aglomerado")
        plt.ylabel("Porcentaje (%)")
        plt.xticks(rotation=60, ha="right")
        plt.legend(title="Tipo de empleo", bbox_to_anchor=(1, 0), loc="lower right")
        plt.tight_layout()
        st.pyplot(plt)

    inciso1_5_4(path_persona)

with tab4:

    def inciso1_5_5(path_individual, path_aglomerados):
        """
        Muestra la evolución de las tasas de empleo y desempleo por aglomerado a lo largo del tiempo,
        comparando el período más antiguo y más reciente, y visualizando los resultados en un mapa.

        Parámetros:
        ----------
        path_individual : str
            Ruta al archivo CSV que contiene los datos individuales, separado por punto y coma, codificado en UTF-8.
        path_aglomerados : str
            Ruta al archivo JSON que contiene las coordenadas de los aglomerados.
        Variables internas:
        -------------------
        - df : pd.DataFrame
            DataFrame que contiene los datos de empleo y desempleo por aglomerado, año y trimestre.
        - tasas : pd.DataFrame
            DataFrame que contiene las tasas de empleo y desempleo calculadas por aglomerado, año y trimestre.
        - min_periodo : pd.Series
            Serie que contiene el período más antiguo en los datos.
        - max_periodo : pd.Series
            Serie que contiene el período más reciente en los datos.
        - antiguo : pd.DataFrame
            DataFrame que contiene las tasas de empleo y desempleo del período más antiguo.
        - actual : pd.DataFrame
            DataFrame que contiene las tasas de empleo y desempleo del período más reciente.
        - comparacion : pd.DataFrame
            DataFrame que contiene la comparación de tasas entre el período más antiguo y el más reciente por aglomerado.
        - df_coords : pd.DataFrame
            DataFrame que contiene las coordenadas de los aglomerados, cargadas desde un archivo JSON.
        - mapa : folium.Map
            Mapa interactivo creado con Folium para visualizar los aglomerados y sus tasas de empleo/desempleo.
        - modo : str
            Modo seleccionado por el usuario para visualizar las tasas, ya sea "empleo" o "desempleo".
        - asignar_color : function
            Función que asigna un color a cada fila del DataFrame de comparación según la evolución de las tasas.
        - popup_text : str
            Texto que se muestra al hacer clic en un marcador del mapa, mostrando las tasas de empleo o desempleo.
        - df_final : pd.DataFrame
            DataFrame final que combina las tasas de empleo/desempleo con las coordenadas de los aglomerados.

        Retorna:
        -------
        None
        """
        # Título de la app
        st.subheader("Evolución de tasas por aglomerado")

        # Cargar archivo de datos individuales
        df = pd.read_csv(path_individual, sep=";", encoding="utf-8")

        # Filtrar valores válidos
        df = df[df["ESTADO"].notna()]

        # Crear columnas auxiliares
        df["empleado"] = df["ESTADO"].isin([1]).astype(int)
        df["desempleado"] = df["ESTADO"].isin([2]).astype(int)
        df["fuerza_laboral"] = df["ESTADO"].isin([1, 2]).astype(int)

        # Calcular tasas por aglomerado, año y trimestre
        tasas = (
            df.groupby(["AGLOMERADO", "ANO4", "TRIMESTRE"])
            .apply(
                lambda x: pd.Series(
                    {
                        "tasa_empleo": (x["empleado"] * x["PONDERA"]).sum()
                        / (x["fuerza_laboral"] * x["PONDERA"]).sum()
                        * 100,
                        "tasa_desempleo": (x["desempleado"] * x["PONDERA"]).sum()
                        / (x["fuerza_laboral"] * x["PONDERA"]).sum()
                        * 100,
                    }
                )
            )
            .reset_index()
        )

        # Buscar trimestre más antiguo y más reciente
        min_periodo = tasas[["ANO4", "TRIMESTRE"]].min()
        max_periodo = tasas[["ANO4", "TRIMESTRE"]].max()

        # Crear columna de período para ordenar correctamente
        tasas["PERIODO"] = tasas["ANO4"] * 10 + tasas["TRIMESTRE"]

        # Encontrar valores extremos reales que existen en los datos
        min_periodo = tasas["PERIODO"].min()
        max_periodo = tasas["PERIODO"].max()

        # Separar año y trimestre
        min_ano = min_periodo // 10
        min_trim = min_periodo % 10
        max_ano = max_periodo // 10
        max_trim = max_periodo % 10

        antiguo = tasas[
            (tasas["ANO4"] == min_ano) & (tasas["TRIMESTRE"] == min_trim)
        ].copy()
        actual = tasas[
            (tasas["ANO4"] == max_ano) & (tasas["TRIMESTRE"] == max_trim)
        ].copy()

        # Renombrar para comparación
        antiguo = antiguo.rename(
            columns={
                "tasa_empleo": "tasa_empleo_antigua",
                "tasa_desempleo": "tasa_desempleo_antigua",
            }
        )
        actual = actual.rename(
            columns={
                "tasa_empleo": "tasa_empleo_actual",
                "tasa_desempleo": "tasa_desempleo_actual",
            }
        )

        # Unir los dos DataFrames
        comparacion = pd.merge(
            antiguo[["AGLOMERADO", "tasa_empleo_antigua", "tasa_desempleo_antigua"]],
            actual[["AGLOMERADO", "tasa_empleo_actual", "tasa_desempleo_actual"]],
            on="AGLOMERADO",
        )

        # Selector: empleo o desempleo
        modo = st.selectbox("¿Qué tasa quierés analizar?", ["empleo", "desempleo"])

        # Definir colores según evolución
        def asignar_color(fila, modo):
            if modo == "empleo":
                return (
                    "green"
                    if fila["tasa_empleo_actual"] > fila["tasa_empleo_antigua"]
                    else "red"
                )
            else:
                return (
                    "red"
                    if fila["tasa_desempleo_actual"] > fila["tasa_desempleo_antigua"]
                    else "green"
                )

        comparacion["color"] = comparacion.apply(
            lambda fila: asignar_color(fila, modo), axis=1
        )

        # Cargar coordenadas y convertirlas en DataFrame
        with open(path_aglomerados, "r", encoding="utf-8") as f:
            data = json.load(f)

        df_coords = (
            pd.DataFrame.from_dict(data, orient="index")
            .reset_index()
            .rename(columns={"index": "AGLOMERADO"})
        )
        df_coords["AGLOMERADO"] = df_coords["AGLOMERADO"].astype(int)
        df_coords["lat"] = df_coords["coordenadas"].apply(lambda x: x[0])
        df_coords["lon"] = df_coords["coordenadas"].apply(lambda x: x[1])
        df_coords.drop(columns=["coordenadas"], inplace=True)

        # Merge con coordenadas
        df_final = comparacion.merge(df_coords, on="AGLOMERADO", how="left")

        # Crear mapa con folium
        mapa = folium.Map(location=[-34.6, -58.4], zoom_start=4.7)

        for _, row in df_final.iterrows():
            popup_text = f"<b>{row['nombre']}</b><br>"

            if modo == "empleo":
                popup_text += f"Anterior: {row['tasa_empleo_antigua']:.2f}%<br>Actual: {row['tasa_empleo_actual']:.2f}%"
            else:
                popup_text += f"Anterior: {row['tasa_desempleo_antigua']:.2f}%<br>Actual: {row['tasa_desempleo_actual']:.2f}%"

            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=7,
                color=row["color"],
                fill=True,
                fill_color=row["color"],
                fill_opacity=0.75,
                popup=folium.Popup(popup_text, max_width=250),
            ).add_to(mapa)

        # Mostrar mapa
        st_folium(mapa)

    inciso1_5_5(path_persona, path_coords_agloms)
