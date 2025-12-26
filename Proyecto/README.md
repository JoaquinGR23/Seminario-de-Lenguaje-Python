# Proyecto:
## 1. EPH (Encuesta permanente de hogares)
Es un programa nacional de produccion permanente de indicadores sociales cuyo objetivo es conocer las caracteristicas socioeconomicas de la poblacion.
## 2. Encuest.AR
Es una app de busqueda y visualizacion de datos relacionados a la EPH y su objetivo es hacer comprensibles y accesibles los datos crudos de la EPH.

## Instalacion de Dependencias

Para ejecutar este proyecto, se recomienda crear un entorno virtual y luego instalar las dependencias necesarias.

### 1. Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- En Windows:
  ```bash
  source venv\Scripts\activate
  ```
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias
Para poder ejecutar correctamente esta App se deben instalar las siguientes dependencias:

- En Windows:
1. Abre la linea de comandos o terminal en Windows.
2. Navega hasta el directorio donde se encuentra el archivo `requirements.txt` usando el comando `cd <ruta_del_directorio>`.
3. Una vez en el directorio correcto, puedes instalar las dependencias usando los siguientes comandos:

```bash
pip install -r requirements.txt
```

Este comando utiliza `pip`, el gestor de paquetes de Python, para instalar todas las dependencias listada en el archivo `requirements.txt`.

Instalación en Linux:
1. Abre la terminal en Linux.
2. Navega hasta el directorio donde se encuentra el archivo `requirements.txt` usando el comando `cd <ruta_del_directorio>`.
3. Una vez en el directorio correcto, puedes instalar las dependencias usando los siguientes comandos:

```bash
pip install -r requirements.txt
```

Al igual que en Windows, este comando utiliza `pip`, el gestor de paquetes de Python, para instalar todas las dependencias listada en el archivo `requirements.txt`.

Asegurate de tener Python 3.12 o posterior y `pip` instalados en tu sistema antes de ejecutar estos comandos. Tambien es recomendable utilizar un entorno virtual de Python para evitar conflictos entre diferentes proyectos y sus dependencias. 


## Ejecución del Proyecto
Para analizar los datos, ejecuta el script principal:

desde un **notebook**, asegurate de estar en el entorno virtual y luego abre Jupyter Notebook:
```bash
jupyter notebook
```
Dentro de Jupyter, navega hasta la carpeta `notebooks` y abre el archivo Encuest_ar.ipynb 

Para abrir streamlit asegurate de estar posicionado en Code/streamlit en una terminal y ejecuta:

 `streamlit run 1_inicio.py`


## Estructura del Proyecto
```
Encuest_ar/
│── coord_agloms
|   │── aglomerados_coordenadas.json  # Informacion de las coordenadas de los aglomerados
│── data_canasta_basica
|   │── valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv      # Informacion de la CBA Y CBT de la INDEX desde 2016 hasta la actualidad
│── data_eph                          # Datos de la EPH correspondiente al 2do y 3er trimestre del 2024
|   │── EPH_usu_2do_Trim2024_txt      # Datos del 2do trimestre
|   |   │── usu_hogar_T224.txt 
|   |   │── usu_individual_T224.txt
|   │── EPH_usu_3er_Trim2024_txt      # Datos del 3er trimestre
|   |   │── usu_hogar_T324.txt 
|   |   │── usu_individual_T324.txt
│── data_out  # Esta carpeta contiene datos procesados a nivel de hogar e individuos, generados a partir de los archivos crudos de la EPH.
│   │──usu_hogar.csv
│   │──usu_individual.csv
│── notebooks/           # Notebooks con analisis y resultados
│    ├── Encuest_ar.ipynb # Este notebook contiene el flujo principal de análisis del proyecto     
│── src/                 # Código fuente y funciones
│   │── utils/           # Funciones auxiliares y definiciones reutilizables para el procesamiento y análisis de datos del proyecto
│   │     ├── constantes.py   # Constantes y configuraciones generales usadas en todo el proyecto.
│   │── main.py          # Módulo con las funciones principales 
│   │── nivelEducativo.py    # Análisis y visualizacion de la distribución de la población 
según el nivel educativo alcanzado, usando datos individuales de la EPH  
│   │── button.py            # Módulo con la funcion para tener el boton de streamlit y session_state para mantener el estado del botón entre ejecuciones.  
│   │── __init__.py          # Para convertir src en un paquete de python
│   │── fechas.py            # módulo con funciones para extraer información de año y trimestre  
desde el archivo procesado 'usu_hogar.csv', ubicado en la carpeta 'data_out'.
│── streamlit/                 # Código fuente y funciones
│   │── pages/
│   │   │── 2_Carga_De_Datos.py                   # Gestión de los datos utilizados por la aplicación.Búsqueda_Por_Tema.py
│   │   │── 3_Caracteristicas_demograficas.py     # Análisis de las características demográficas de la población.
│   │   │── 4_Caracteristicas_de_la_vivienda.py   # Análisis y visualizacion de las distintas características de las viviendas relevadas por la EPH. 
a partir del archivo procesado `usu_hogar.csv`.
|   │   │── 5_Actividad_y_empleo.py               # Se visualizará información relacionada a la actividad y empleo según la Encuesta Permanente de Hogares (EPH).
│   │   │── 6_Educacion.py                        # Análisis descriptivo del nivel educativo alcanzado por la población
según los datos de la Encuesta Permanente de Hogares (EPH).
│   │   │── 7_Ingresos.py                         # Análisis de la situación de pobreza e indigencia en hogares de 4 integrantes según los datos de ingresos provenientes de la EPH y los valores de la Canasta Básica Total (CBT) y Canasta Básica Alimentaria (CBA) proporcionados por INDEC.
│   │── 1_Inicio.py                               # Pantalla inicial de la aplicación Streamlit
│── requirements.txt     # Dependencias del proyecto
│── README.md            # Instrucciones y documentación
│── .gitignore.txt       # Archivos y carpetas ignorados por Git
│── LICENSE              # Licencia del codigo
```
**Leer licencia**
* La licencia asociada a la App es: Ver archivo LICENSE

## Autores
- Gimenez Ruiz Joaquin Alejo 
- Erik Nishimura
- Rasic Avril Antonella 
- Carrizo Senra Rocio
- Manucci Lautaro David
