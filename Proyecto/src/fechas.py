from pathlib import Path
import csv, sys


sys.path.append(str(Path(__file__).parent.parent))

from src.utils.constantes import data_out_path

file_path = data_out_path / "usu_hogar.csv"


def obtener_desde_fecha():
    """
    Extrae y devuelve la fecha más antigua (trimestre y año) disponible en el archivo 'usu_hogar.csv'.

    La función abre el archivo ubicado en la carpeta 'data_out', lee sus filas y busca los valores mínimos
    de las columnas correspondientes a 'anio' y 'trimestre' (posiciones 1 y 2, respectivamente).

    Retorna:
    - str: Una cadena con el formato "trimestre,año", representando la fecha más antigua encontrada.

    También imprime el resultado en consola.
    """
    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        # Suponiendo que hay columnas 'anio' y 'trimestre' en el archivo
        next(reader)
        primer_anio = None
        primer_trimestre = None
        for fila in reader:
            # obtener el primer y último año y trimestre suponiendo que las columnas
            #'anio' y 'trimestre' están en las posiciones 1 y 2 respectivamente
            # y que el archivo tiene encabezados y Convertir a int para evitar problemas de comparación
            anio = int(fila[1])
            trimestre = int(fila[2])
            if primer_anio is None or (
                anio < primer_anio
                or (anio == primer_anio and trimestre < primer_trimestre)
            ):
                primer_anio = anio
                primer_trimestre = trimestre
    result = f"{primer_trimestre},{primer_anio}"
    print(result)
    return result


def obtener_hasta_fecha():
    """
    Extrae y devuelve la fecha más reciente (trimestre y año) disponible en el archivo 'usu_hogar.csv'.

    La función abre el archivo ubicado en la carpeta 'data_out', recorre las filas y detecta los valores
    máximos de las columnas correspondientes a 'anio' y 'trimestre' (ubicadas en los índices 1 y 2).

    Retorna:
    - str: Una cadena con el formato "trimestre,año", representando la fecha más reciente encontrada.

    También imprime el resultado por consola.
    """
    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        # Suponiendo que hay columnas 'anio' y 'trimestre' en el archivo
        next(reader)
        ultimo_anio = None
        ultimo_trimestre = None
        for fila in reader:
            # obtener el primer y último año y trimestre Suponiendo que las columnas
            #'anio' y 'trimestre' están en las posiciones 1 y 2 respectivamente
            # y que el archivo tiene encabezados y Convertir a int para evitar problemas de comparación
            anio = int(fila[1])
            trimestre = int(fila[2])
            if ultimo_anio is None or (
                anio > ultimo_anio
                or (anio == ultimo_anio and trimestre > ultimo_trimestre)
            ):
                ultimo_anio = anio
                ultimo_trimestre = trimestre
    result = f"{ultimo_trimestre},{ultimo_anio}"
    print(result)
    return result
