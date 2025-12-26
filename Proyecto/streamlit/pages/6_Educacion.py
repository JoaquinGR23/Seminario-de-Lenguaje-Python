import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import sys
# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.constantes import data_out_path
path_individual = data_out_path/'usu_individual.csv'
tab1,tab2,tab3,tab4 = st.tabs(['Población por nivel educativo','Nivel educativo más común por grupo etario',
                               'Top 5 aglomerados','Porcentaje de personas alfabetas y analfabetas'])
with tab1:
    def inciso1_6_1(path_individual):
        """
        Visualiza la distribución de la población por nivel educativo para un año seleccionado.

        Parámetros:
        -----------
        path_individual : str
            Ruta al archivo CSV que contiene los datos individuales.

        Retorna:
        --------
        None
        """
        df = pd.read_csv(path_individual, sep = ';',usecols=['ANO4','PONDERA','NIVEL_ED'], encoding='utf-8')
        anios =sorted(df['ANO4'].dropna().unique())
        option = st.selectbox("Elija un año a procesar",(anios))
        df_anio = df[df['ANO4'] == option].copy()
        nivelEd_str = {
            1: "Primario \nincompleto\n(incluye educación especial)",
            2: "Primario \ncompleto",
            3: "Secundario \nincompleto",
            4: "Secundario \ncompleto",
            5: "Superior universitario\n incompleto",
            6: "Superior universitario\n completo",
            7: "Sin instrucción",
            9 : "Ns/Nr"
        }
        df_anio['NIVEL_ED'] = df_anio['NIVEL_ED'].map(nivelEd_str)
        resultados = df_anio.groupby('NIVEL_ED')['PONDERA'].sum().reset_index(name='Cantidad de personas')
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(resultados['NIVEL_ED'], resultados['Cantidad de personas'], color='#B597F5')
        ax.set_title(f'Población por Nivel Educativo - Año {option}')
        ax.set_xlabel('Nivel educativo')
        ax.set_ylabel('Población estimada (ponderada)')
        for label in ax.get_xticklabels():
            label.set_rotation(0)
            label.set_ha('right')
        plt.tight_layout()
        st.pyplot(fig)
    inciso1_6_1(path_individual)

with tab2:
    def inciso1_6_2(path_individual):
        """
        Muestra una tabla con el nivel educativo más común por grupo etario a partir de un archivo CSV de datos individuales.
        Permite al usuario seleccionar grupos etarios específicos para visualizar los resultados.

        Parámetros:
        ----------
        path_individual : str
            Ruta al archivo CSV que contiene los datos individuales, separado por punto y coma, codificado en UTF-8.

        Variables internas:
        -------------------
        niveles : dict
            Diccionario que mapea los códigos de nivel educativo a sus descripciones textuales.
        bins : list
            Lista de límites para agrupar las edades en intervalos de 10 años.
        labels : list
            Lista de etiquetas para los grupos etarios correspondientes a los límites definidos en `bins`.

        Retorna:
        -------
        None
        """
        # Cargar CSV
        df = pd.read_csv(path_individual, sep=";", encoding="utf-8")

        # Diccionario de nombres de niveles educativos
        niveles = {
            1: "Primario incompleto",
            2: "Primario completo",
            3: "Secundario incompleto",
            4: "Secundario completo",
            5: "Superior Universitario incompleto",
            6: "Superior Universitario completo",
            7: "Posgrado",
            8: "Sin Instrucción",
            9: "Ns/Nr",
        }

        # Agregar grupo etario
        bins = [20, 30, 40, 50, 60, 150]
        labels = ["20-29", "30-39", "40-49", "50-59", "60+"]
        df = df[df["CH06"] >= 20].copy()
        df["grupo_etario"] = pd.cut(df["CH06"], bins=bins, labels=labels, right=False)

        # Título
        st.subheader("Nivel educativo más común por grupo etario")

        # Selección de grupos etarios
        grupos_seleccionados = st.multiselect(
            "Seleccioná los grupos etarios a mostrar:",
            options=labels,
            default=labels,  # Mostrar todos por defecto
        )

        # Verificar si se seleccionaron grupos
        if not grupos_seleccionados:
            st.warning("Por favor, seleccioná al menos un grupo etario.")
        else:
            # Filtrar según selección
            df_filtrado = df[df["grupo_etario"].isin(grupos_seleccionados)]

            # Agrupar por grupo etario y nivel educativo
            tabla = (
                df_filtrado.groupby(["grupo_etario", "NIVEL_ED"])["PONDERA"]
                .sum()
                .reset_index()
            )

            # Obtener el nivel más común por grupo etario
            nivel_mas_comun = tabla.loc[
                tabla.groupby("grupo_etario")["PONDERA"].idxmax()
            ].copy()
            nivel_mas_comun["Nivel educativo más común"] = nivel_mas_comun["NIVEL_ED"].map(
                niveles
            )

            # Mostrar solo los seleccionados
            nivel_mas_comun = nivel_mas_comun[
                nivel_mas_comun["grupo_etario"].isin(grupos_seleccionados)
            ]

            # Mostrar tabla
            tabla_final = nivel_mas_comun[
                ["grupo_etario", "Nivel educativo más común", "PONDERA"]
            ].rename(
                columns={"grupo_etario": "Grupo etario", "PONDERA": "Personas estimadas"}
            )

            st.table(tabla_final.set_index("Grupo etario"))
    inciso1_6_2(path_individual)

with tab3:
    def inciso1_6_3(path_individual):
        """
        Muestra y exporta el ranking de los 5 aglomerados con mayor porcentaje de hogares
        con dos o más personas con estudios universitarios completos (nivel 6), ponderado según EPH.
        """

        usecols = [
            "ANO4",
            "TRIMESTRE",
            "CODUSU",
            "NRO_HOGAR",
            "AGLOMERADO",
            "NIVEL_ED",
            "PONDERA",
        ]
        df = pd.read_csv(path_individual, sep=";", encoding="utf-8", usecols=usecols)

        # calculo del trimestre y año más reciente
        df["FECHA"] = df["ANO4"] * 10 + df["TRIMESTRE"]
        fecha_max = df["FECHA"].max()
        anio_max = fecha_max // 10
        trimestre_max = fecha_max % 10

        df_reciente = df[
            (df["ANO4"] == anio_max) & (df["TRIMESTRE"] == trimestre_max)
        ].copy()

        df_reciente["es_universitario_completo"] = df_reciente["NIVEL_ED"] == 6

        # Conteo de universitarios por hogar
        grupo_hogar = df_reciente.groupby(["CODUSU", "NRO_HOGAR", "AGLOMERADO"])

        df_hogares = grupo_hogar.agg(
            cant_universitarios=("es_universitario_completo", "sum"),
            pondera_hogar=("PONDERA", "first"),  # una vez por hogar
        ).reset_index()

        df_hogares["universitario_2+"] = df_hogares["cant_universitarios"] >= 2

        # Agrupar por aglomerado con ponderación
        resumen = (
            df_hogares.groupby("AGLOMERADO")
            .agg(
                total_ponderado=("pondera_hogar", "sum"),
                hogares_con_2_uni_pond=(
                    "pondera_hogar",
                    lambda x: x[df_hogares.loc[x.index, "universitario_2+"]].sum(),
                ),
            )
            .reset_index()
        )

        resumen["Proporción (%)"] = (
            resumen["hogares_con_2_uni_pond"] / resumen["total_ponderado"] * 100
        ).round(2)
        resumen = resumen.sort_values("Proporción (%)", ascending=False)

        top_5 = resumen.head(5).copy()
        top_5["AGLOMERADO"] = top_5["AGLOMERADO"].astype(str)

        # Tabla Streamlit
        st.subheader(
            f"Top 5 aglomerados con mayor % de hogares con 2 o mas universitarios completos - Año {anio_max}, Trimestre {trimestre_max}"
        )
        st.dataframe(
            top_5.rename(
                columns={
                    "AGLOMERADO": "Aglomerado",
                    "total_ponderado": "Total de hogares",
                    "hogares_con_2_uni_pond": "Hogares con 2 o mas universitarios",
                }
            ).set_index("Aglomerado")
        )

        # Botón de descarga
        csv = top_5.to_csv(index=False, sep=";", encoding="utf-8")
        st.download_button(
            label=" Descargar ranking como CSV",
            data=csv,
            file_name=f"ranking_aglomerados_ponderado_{anio_max}_T{trimestre_max}.csv",
            mime="text/csv",
        )
    inciso1_6_3(path_individual)

with tab4:
    def inciso1_6_4(path_individual):
        """
        Informa el porcentaje de personas mayores de 6 años alfabetizadas y no alfabetizadas
        (capaces o no de leer y escribir), tomando el trimestre más reciente de cada año.

        Parámetros
        ----------
        path_individual : str
            Ruta al archivo CSV de datos individuales.

        Retorna
        -------
        None
        """

        usecols = ["ANO4", "TRIMESTRE", "CH06", "CH09", "PONDERA"]
        df = pd.read_csv(path_individual, sep=";", encoding="utf-8", usecols=usecols)

        # Filtrar y calculo de trimestre y año
        df = df[df["CH06"] > 6]
        df["FECHA"] = df["ANO4"] * 10 + df["TRIMESTRE"]
        trimestres_max = df.groupby("ANO4")["TRIMESTRE"].max().reset_index()
        df = df.merge(trimestres_max, on=["ANO4", "TRIMESTRE"])

        # mapeo para la carga de la nueva columna
        df["alfabetismo"] = df["CH09"].map(
            {1: "Sabe leer", 2: "No sabe leer", 3: "No sabe leer"}
        )

        agrupado = (
            df.groupby(["ANO4", "alfabetismo"])["PONDERA"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Calculo de porcentajes
        agrupado["Total"] = agrupado["Sabe leer"] + agrupado["No sabe leer"]
        agrupado["% Sabe leer"] = (agrupado["Sabe leer"] / agrupado["Total"] * 100).round(2)
        agrupado["% No sabe leer"] = (
            agrupado["No sabe leer"] / agrupado["Total"] * 100
        ).round(2)

        # Tabla streamlit
        st.subheader(
            "Porcentaje de personas alfabetizadas y no alfabetizadas que son mayores de 6 años"
        )
        st.dataframe(
            agrupado[["ANO4", "% Sabe leer", "% No sabe leer"]].rename(
                columns={"ANO4": "Año"}
            )
        )

        # Gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(agrupado["ANO4"], agrupado["% Sabe leer"], marker="o", label="Sabe leer")
        plt.plot(
            agrupado["ANO4"], agrupado["% No sabe leer"], marker="o", label="No sabe leer"
        )
        plt.title("Evolución del alfabetismo - Personas mayores de 6 años")
        plt.xlabel("Año")
        plt.ylabel("Porcentaje")
        plt.ylim(0, 100)
        plt.xticks(agrupado["ANO4"])
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(plt)
    inciso1_6_4(path_individual)