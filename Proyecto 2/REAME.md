# Proyecto: Analisis de Partidas y MVPs

Este proyecto analiza los resultados de varias partidas, generando rankings y determinando los MVPs.
El codigo fuente con las funciones necesarias se encuentra en el directorio `src`, mientras que los notebooks de analisis estan en la carpeta `notebooks`.

## Instalacion de Dependencias

Para ejecutar este proyecto, se recomienda crear un entorno virtual y luego instalar las dependencias necesarias.

### 1. Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- En Windows:
  ```bash
  venv\Scripts\activate
  ```
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar dependencias
Ejecuta el siguiente comando en la terminal dentro del proyecto:
```bash
pip install -r requirements.txt
```
Si el archivo `requirements.txt` no está presente, puedes generarlo con:
```bash
pip freeze > requirements.txt
```

## Ejecución del Proyecto

Para analizar los datos, ejecuta el script principal:
```bash
python Ej10.py
```

Si deseas trabajar desde un **notebook**, asegurate de estar en el entorno virtual y luego abre Jupyter Notebook:
```bash
jupyter notebook
```
Dentro de Jupyter, navega hasta la carpeta `notebooks` y abre el archivo correspondiente.

## Estructura del Proyecto
```
proyecto/
│── notebooks/           # Notebooks con analisis y resultados
│── src/                 # Código fuente y funciones
│   ├── funciones.py     # Modulo con funciones principales
│── requirements.txt     # Dependencias del proyecto
│── README.md            # Instrucciones y documentación
```

## Autor
Gimenez Ruiz Joaquin Alejo  23470/5



