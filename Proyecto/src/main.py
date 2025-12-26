import os, sys, csv
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from src.utils.constantes import data_out_path, data_path, data_out_path

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# raíz del proyecto
root_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(root_dir)

# Variables que representan las rutas de los archivos CSV
archivo_data_out_path_individual = data_out_path / "usu_individual.csv"
archivo_data_out_path_hogar = data_out_path / "usu_hogar.csv"


def cargar_dataset():
    """
    Combina los archivos trimestrales de datos crudos de la EPH en dos archivos de formato CSV.

    Este procedimiento recorre los subdirectorios dentro del directorio `data_path`, buscando:
    - Archivos que comienzan con 'usu_hogar', para combinarlos en un único archivo llamado 'usu_hogar.csv'.
    - Archivos que comienzan con 'usu_individual', para combinarlos en 'usu_individual.csv'.

    Para cada tipo de archivo:
    - Se escribe el encabezado (solo una vez, del primer archivo encontrado).
    - Se copian todas las filas de datos de cada archivo encontrado, sin repetir encabezados.

    El resultado se guarda en la carpeta `data_out_path`, sobrescribiendo los archivos si ya existen.
    """
    # leo los archivo del data_path,solo los usu_hogar y lo guardo
    # en un archivo nuevo csv llamado "usu_hogar.csv"
    #  con todo el contenido de los archivos usu_hogar de cada trimestre en uno solo
    archivo_salida_hogar = data_out_path / "usu_hogar.csv"
    se_escribio_encabezado = False
    try:
        with archivo_salida_hogar.open("w", encoding="utf-8") as salida:
            for archivo in data_path.rglob("usu_hogar*"):
                with open(archivo, encoding="utf-8") as f:
                    encabezado = f.readline()
                    if not se_escribio_encabezado:
                        salida.write(encabezado)
                        se_escribio_encabezado = True
                    for line in f:
                        salida.write(line)

        # leo los archivo del data_path,solo los usu_individual y lo guardo
        # en un archivo nuevo csv llamado "usu_individual.csv"
        # con todo el contenido de los archivos usu_individual de cada trimestre en uno solo
        archivo_salida_indiv = data_out_path / "usu_individual.csv"
        se_escribio_encabezado = False
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")
    try:
        with archivo_salida_indiv.open("w", encoding="utf-8") as salida:
            for archivo in data_path.rglob("usu_indi*"):
                with open(archivo, encoding="utf-8") as f:
                    encabezado = f.readline()
                    if not se_escribio_encabezado:
                        salida.write(encabezado)
                        se_escribio_encabezado = True
                    for line in f:
                        salida.write(line)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")

    # obtengo de cada archivo (hogar o individual) el trimestre y año, los guardo en
    # conjuntos y luego evaluo cada uno, verificando que coincidan los datos y no falte
    # algun archivo
    hogar_id = set()
    indiv_id = set()

    for archivo in data_path.rglob("usu_hogar*.txt"):
        nombre = archivo.name
        fecha = nombre.replace("usu_hogar_", "").replace(".txt", "")
        hogar_id.add(fecha)

    for archivo in data_path.rglob("usu_individual*.txt"):
        nombre = archivo.name
        fecha = nombre.replace("usu_individual_", "").replace(".txt", "")  # ej: T224
        indiv_id.add(fecha)

    hogar = hogar_id - indiv_id
    individual = indiv_id - hogar_id
    falta = False

    # si falta algún archivo imprime trimestre y año
    for id in sorted(hogar):
        anio = id[2:]
        trimestre = id[:2]
        st.write(
            f"Falta el archivo INDIVIDUAL del trimestre: {trimestre}, año: 20{anio}"
        )
        falta = True

    for id in sorted(individual):
        anio = id[2:]
        trimestre = id[:2]
        st.write(f"Falta el archivo HOGAR del trimestre: {trimestre}, año: 20{anio}")
        falta = True

    if falta:
        return
    # si están todos los archivos imprime el mensaje
    st.write("Chequeo exitoso: No se encontraron inconsistencias")


def inciso3_SeccionA():
    """
    Agrega una nueva columna 'CH04_str' al archivo 'usu_individual.csv',
    indicando el sexo de cada persona en formato de texto.

    - Si el valor de la columna CH04 es 1, asigna "masculino".
    - Si el valor de la columna CH04 es distinto de 1, asigna "femenino".

    El archivo es leído, modificado y sobrescrito con la nueva columna.

    """
    fila_modificada = (
        []
    )  # creo una lista vacía que usamos como almacenamiento temporal para todas las
    # filas (el encabezado y cada fila de datos) para despues agregarlo en el archivo csv
    try:
        archivo_data_out_path_individual_tmp = "tmp_output.csv"
        with (
            archivo_data_out_path_individual.open(
                "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_individual_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = reader.fieldnames + ["CH04_str"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for fila in reader:  # 1 = Varón 2 = Mujer
                if int(fila["CH04"]) == 1:
                    texto = "masculino"
                else:
                    texto = "femenino"
                fila["CH04_str"] = texto
                writer.writerow(fila)
        os.replace(
            archivo_data_out_path_individual_tmp, archivo_data_out_path_individual
        )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso4_SeccionA():
    """
    Se recorren los valores de la columna NIVEL_ED y se traducen a su texto correspondiente que puede ser uno de los
    siguientes:
    "Primario Incompleto", "Primario Completo", "Secundario Incompleto", "Secundario Completo",
    "Superior o Universitario", "Sin Informacion".
    Se agregan los valores traducidos a una nueva columna llamada NIVEL_ED_str que se agrega al archivo csv.

    """

    # (el encabezado y cada fila de datos) para despues agregarlo en el archivo csv
    try:
        archivo_data_out_path_individual_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_individual, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_individual_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = reader.fieldnames + ["NIVEL_ED_str"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for fila in reader:
                valor = int(fila["NIVEL_ED"])
                texto = ""
                match valor:
                    case 1:
                        texto = "Primario Incompleto"
                    case 2:
                        texto = "Primario Completo"
                    case 3:
                        texto = "Secundario Incompleto"
                    case 4:
                        texto = "Secundario Completo"
                    case 5 | 6:
                        texto = "Superior o Universitario"
                    case 7 | 9:
                        texto = "Sin Informacion"
                fila["NIVEL_ED_str"] = texto
                writer.writerow(fila)
        os.replace(
            archivo_data_out_path_individual_tmp, archivo_data_out_path_individual
        )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso5_SeccionA():
    """
    Se recorren los valores de la columna ESTADO y CAT_OCUP.
    Segundo el valor de ESTADO y CAT_OCUP se traduce a texto la condicion laboral que puede ser una de las siguientes:
    "Ocupado autonomo", "Ocupado dependiente", "Desocupado", "Inactivo" o "sin informacion".
    Se agregan los valores traducidos a una nueva columna llamada CONDICION_LABORAL que se agrega al archivo csv.
    """

    try:
        archivo_data_out_path_individual_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_individual, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_individual_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = reader.fieldnames + ["CONDICION_LABORAL"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            dict_ocupacion = {
                1: {(1, 2): "Ocupado autonomo", (3, 4, 9): "Ocupado dependiente"},
                2: "Desocupado",
                3: "Inactivo",
                4: "Fuera de categoria/sin informacion",
            }

            for fila in reader:
                estado = int(fila["ESTADO"])
                cat_ocup = int(fila["CAT_OCUP"])
                texto = ""  # Se guarda vacio en caso de ser un Estado igual a 0:Entrevista individual no realizada
                if estado == 1:
                    for claves, valor in dict_ocupacion[1].items():
                        if cat_ocup in claves:
                            texto = valor
                            break
                else:
                    texto = dict_ocupacion.get(estado, "")

                fila["CONDICION_LABORAL"] = texto
                writer.writerow(fila)

        os.replace(
            archivo_data_out_path_individual_tmp, archivo_data_out_path_individual
        )

    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso6_SeccionA():
    """
    Agrega una nueva columna 'UNIVERSITARIO' al archivo 'usu_individual.csv',
    indicando si una persona mayor de edad ha completado al menos el nivel universitario.

    - Si la persona es menor de 18 años, se asigna 2 (No aplica).
    - Si la persona es mayor de edad y su nivel educativo es 'Superior o Universitario' (valores 5 o 6), se
    asigna 1 (Sí).
    - En cualquier otro caso, se asigna 0 (No).

    El archivo se lee completamente, se agrega la nueva columna y luego se sobrescribe con los datos modificados.
    """
    fila_modificada = []
    try:
        archivo_data_out_path_individual_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_individual, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_individual_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = reader.fieldnames + ["UNIVERSITARIO"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            # Columna NIVEL_ED indica el nivel de estudio alcanzado
            # Columna CH06 indica la edad de la persona
            for fila in reader:
                edad = int(fila["CH06"])
                nivel_ed = int(fila["NIVEL_ED"])

                if edad < 18:
                    universitario = 2
                else:
                    if nivel_ed in (5, 6):
                        universitario = 1
                    else:
                        universitario = 0

                fila["UNIVERSITARIO"] = universitario
                writer.writerow(fila)
        os.replace(
            archivo_data_out_path_individual_tmp, archivo_data_out_path_individual
        )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso7_SeccionA():
    """
    Agrega una nueva columna 'TIPO_HOGAR' al archivo 'usu_hogar.csv',
    clasificando los hogares según la cantidad de personas:

    - "Unipersonal" si hay 1 persona.
    - "Nuclear" si hay entre 2 y 4 personas.
    - "Extendido" si hay 5 o más personas.

    El archivo original se sobreescribe con la columna adicional.
    """
    fila_modificada = []
    try:
        archivo_data_out_path_hogar_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_hogar, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_hogar_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            csv_reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = csv_reader.fieldnames + ["TIPO_HOGAR"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            # IX_Tot indica la cantidad de personas en el hogar
            for row in csv_reader:
                personas = int(row["IX_TOT"])
                if personas == 1:
                    tipo = "Unipersonal"
                elif 2 <= personas <= 4:
                    tipo = "Nuclear"
                else:
                    tipo = "Extendido"

                row["TIPO_HOGAR"] = tipo
                writer.writerow(row)
        os.replace(archivo_data_out_path_hogar_tmp, archivo_data_out_path_hogar)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso8_SeccionA():
    """
    Agrega una nueva columna 'MATERIAL_TECHUMBRE' al archivo 'usu_hogar.csv',
    clasificando el material del techo de cada vivienda según el valor del campo IV4.

    La clasificación es la siguiente:
    - Si IV4 está entre 5 y 7: "Material precario".
    - Si IV4 está entre 1 y 4: "Material durable".
    - Si IV4 es 9: "no aplica".

    El archivo se lee completo, se agrega la nueva columna con la descripción correspondiente
    y luego se sobrescribe con los datos modificados.
    """
    fila_modificada = []
    try:
        archivo_data_out_path_hogar_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_hogar, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_hogar_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            csv_reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = csv_reader.fieldnames + ["MATERIAL_TECHUMBRE"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for row in csv_reader:
                if int(row["IV4"]) in range(5, 8):  # de 5 a 7
                    texto = "Material precario"
                elif int(row["IV4"]) in range(1, 5):  # de 1 a 4
                    texto = "Material durable"
                else:  # si es 9
                    texto = "no aplica"
                row["MATERIAL_TECHUMBRE"] = texto
                writer.writerow(row)
        os.replace(archivo_data_out_path_hogar_tmp, archivo_data_out_path_hogar)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso9_SeccionA():
    """
    Agrega una nueva columna 'DENSIDAD_HOGAR' al archivo 'usu_hogar.csv',
    calculando la densidad de ocupación del hogar como el promedio de personas por habitación.

    La categorización se realiza de la siguiente manera:
    - Si el promedio de personas por habitación es menor a 1: "Bajo".
    - Si el promedio es entre 1 y 2 (inclusive): "Medio".
    - Si el promedio es mayor a 2: "Alto".

    El archivo se lee completo, se agrega la nueva columna con la categoría correspondiente
    y luego se sobrescribe con los datos modificados.
    """
    fila_modificada4 = (
        []
    )  # creo una lista vacía que usamos como almacenamiento temporal para todas las filas
    # (el encabezado y cada fila de datos) para despues agregarlo en el archivo csv
    try:
        archivo_data_out_path_hogar_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_hogar, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_hogar_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            csv_reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = csv_reader.fieldnames + ["DENSIDAD_HOGAR"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            # Campo IV2 que indica cuantas habitaciones tiene un hogar en total
            # Campo IX_Tot que indica la cantidad de personas por hogar
            for row in csv_reader:
                habitaciones = int(row["IV2"])
                personas = int(row["IX_TOT"])
                promedio = personas / habitaciones
                if promedio < 1:
                    texto = "Bajo"
                elif 1 <= promedio <= 2:
                    texto = "Medio"
                else:
                    texto = "Alto"

                row["MATERIAL_TECHUMBRE"] = texto
                writer.writerow(row)
        os.replace(archivo_data_out_path_hogar_tmp, archivo_data_out_path_hogar)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso10_seccionA():
    """
    Clasifica la condición de habitabilidad de cada hogar en el archivo `usu_hogar.csv` y agrega
    una nueva columna llamada 'CONDICION_DE_HABITABILIDAD' con una categoría cualitativa.

    La función:
    - Lee el archivo de hogares delimitado por `;`.
    - Evalúa las condiciones habitacionales de cada fila (hogar).
    - Asigna una categoría de habitabilidad según reglas definidas:
        - "Buena": Todos los indicadores tienen el valor óptimo (== 1).
        - "Saludable": Indicadores con valores aceptables (en rango 1-2, IV8 debe ser 1).
        - "Regular": Valores permisibles más amplios (en rango 1-3, IV8 al menos 1).
        - "Insuficiente": Condiciones críticas específicas (IV6 == 3, IV7 == 3, IV8 == 2).
    - Agrega la clasificación al final de cada fila.
    - Sobrescribe el archivo original con los datos actualizados.

    Esta función no recibe parámetros ni devuelve valores, pero modifica el archivo `archivo_data_out_path_hogar`.

    """
    # Descripcion de los campos usados:
    """ 
    Campo IV6:
        Tiene agua...
            1. por cañería dentro de la vivienda
            2. fuera de la vivienda pero dentro del terreno
            3. fuera del terreno
    Campo IV7:
        El agua es de...
            1. red pública (agua corriente)
            2. perforación con bomba a motor
            3. perforación con bomba manual
    Campo IV8:
        ¿Tiene baño / letrina?
            1 = Sí
            2 = No
    Campo IV9:
        El baño o letrina está...
            1. dentro de la vivienda
            2. fuera de la vivienda, pero dentro del terreno
            3. fuera del terreno
    Campo IV10:
        El baño tiene...
            1. inodoro con botón / mochila / cadena y arrastre de agua
            2. inodoro sin botón / cadena y con arrastre de agua (a balde)
            3. letrina (sin arrastre de agua)
    """
    fila_modificada = []
    try:
        archivo_data_out_path_hogar_tmp = "tmp_output.csv"
        with (
            open(
                archivo_data_out_path_hogar, "r", newline="", encoding="utf-8"
            ) as lectura,
            open(
                archivo_data_out_path_hogar_tmp, "w", newline="", encoding="utf-8"
            ) as escritura,
        ):
            csv_reader = csv.DictReader(lectura, delimiter=";")
            fieldnames = csv_reader.fieldnames + ["CONDICION_DE_HABITABILIDAD"]
            writer = csv.DictWriter(escritura, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for row in csv_reader:
                texto = " "
                if (
                    int(row["IV6"]) == 1
                    and int(row["IV7"]) == 1
                    and int(row["IV8"]) == 1
                    and int(row["IV9"]) == 1
                    and int(row["IV10"]) == 1
                ):
                    texto = "Buena"
                elif (
                    int(row["IV6"]) in range(1, 3)
                    and int(row["IV7"]) in range(1, 3)
                    and int(row["IV8"]) == 1
                    and int(row["IV9"]) in range(1, 3)
                    and int(row["IV10"]) in range(1, 3)
                ):
                    texto = "Saludable"
                elif (
                    int(row["IV6"]) in range(1, 4)
                    and int(row["IV7"]) in range(1, 4)
                    and int(row["IV8"]) == 1
                    and int(row["IV9"]) in range(1, 4)
                    and int(row["IV10"]) in range(1, 4)
                ):
                    texto = "Regular"
                else:
                    texto = "Insuficiente"
                row["CONDICION_DE_HABITABILIDAD"] = texto
                writer.writerow(row)
        os.replace(archivo_data_out_path_hogar_tmp, archivo_data_out_path_hogar)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso1_seccionB():
    """
    Calcula e imprime el porcentaje de personas alfabetizadas y no alfabetizadas
    (mayores de 6 años) para cada año, tomando únicamente el trimestre más reciente disponible.

    La función:
    - Lee un archivo CSV con delimitador `;` utilizando `csv.DictReader`.
    - Determina para cada año el trimestre máximo presente en los datos.
    - Filtra personas mayores de 6 años correspondientes al trimestre más reciente de cada año.
    - Clasifica a las personas como alfabetizadas si saben leer  o no alfabetizadas si no saben o no contestaron.
    - Usa el ponderador individual  para realizar un cálculo representativo.
    - Imprime por consola el porcentaje de alfabetizados y no alfabetizados por año.

    Esta función no recibe argumentos ni devuelve valores; muestra directamente los resultados por consola.
    """
    # Primero: encontrar el trimestre máximo por año
    trimestres_maximos = {}
    try:
        with open(archivo_data_out_path_individual, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                año = int(row["ANO4"])
                trimestre = int(row["TRIMESTRE"])
                if año not in trimestres_maximos or trimestre > trimestres_maximos[año]:
                    trimestres_maximos[año] = trimestre

        # Segundo: contar alfabetizados y no alfabetizados por año
        alfabetizados = {}
        no_alfabetizados = {}
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")
    try:
        with open(archivo_data_out_path_individual, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                año = int(row["ANO4"])
                trimestre = int(row["TRIMESTRE"])
                edad = int(row["CH06"])
                sabe_leer = int(row["CH09"])
                pondera = int(row["PONDERA"])

                if trimestre == trimestres_maximos[año] and edad > 6:
                    if sabe_leer == 1:
                        if año not in alfabetizados:
                            alfabetizados[año] = 0
                        alfabetizados[año] += pondera
                    elif sabe_leer == 2 or sabe_leer == 3:
                        if año not in no_alfabetizados:
                            no_alfabetizados[año] = 0
                        no_alfabetizados[año] += pondera

        # Mostrar resultados
        for año in sorted(trimestres_maximos.keys()):
            a = alfabetizados.get(año, 0)
            n = no_alfabetizados.get(año, 0)
            total = a + n
            if total > 0:
                p_saben = (a / total) * 100
                p_no_saben = (n / total) * 100
                print(
                    f"Año {año}: Saben leer = {p_saben:.2f}%, No saben leer = {p_no_saben:.2f}%"
                )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso2_seccionB():
    """
    Calcula e imprime el porcentaje de personas no nacidas en Argentina que hayan cursado
    un nivel universitario (completo o incompleto) durante un año y trimestre específicos.

    La función:
    - Solicita al usuario el año y trimestre a analizar.
    - Lee los datos desde un archivo CSV delimitado por punto y coma.
    - Identifica a las personas nacidas en el extranjero.
    - Dentro de este grupo, cuenta cuántas alcanzaron nivel universitario o superior
    - Usa el ponderador individual para realizar un cálculo representativo.
    - Imprime el porcentaje de extranjeros con estudios universitarios para el período indicado.

    No recibe argumentos ni retorna valores; interactúa directamente con el usuario y muestra el resultado por consola.
    """
    # Descripcion de los campos usados:
    """ 
    Campo CH12:
        ¿Cuál es el nivel más alto que cursa o cursó?
            1 = Jardín/preescolar
            2 = Primario
            3 = EGB
            4 = Secundario
            5 = Polimodal
            6 = Terciario
            7 = Universitario
            8 = Posgrado universitario
            9 = Educación especial (discapacitado)
    Campo CH15:
        ¿Dónde nació?
            1. En esta localidad
            2. En otra localidad de esta provincia
            3. En otra provincia (especificar)
            4. En un país limítrofe (especificar: Brasil, Bolivia, Chile, Paraguay, Uruguay)
            5. En otro país (especificar)
            9. Ns/Nr
    """
    total_extranjera = 0
    total_universitarios = 0
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as entrada:
            csv_reader = csv.DictReader(entrada, delimiter=";")
            try:
                next(csv_reader)
            except StopIteration:
                print("Archivo vacio")
            anio = input(
                "ingrese año para informar el porcentaje de personas "
                "no nacidas en Argentina que hayan cursado un nivel universitario o superior"
            )
            trimestre = input(
                "ingrese trimestre para informar el porcentaje de personas no nacidas en Argentina que "
                "hayan cursado un nivel universitario o superior"
            )
            for row in csv_reader:
                if (row["TRIMESTRE"] == trimestre) and (row["ANO4"] == anio):
                    if int(row["CH15"]) in range(4, 6):
                        total_extranjera += int(row["PONDERA"])
                        if int(row["CH12"]) in range(7, 9):
                            total_universitarios += int(row["PONDERA"])
            porcentaje = round((total_universitarios / total_extranjera) * 100, 2)
        print(
            f"Porcentaje de personas no nacidas en Argentina que hayan cursado un nivel universitario o superior "
            f"del trimestre {trimestre} en el año {anio} es: {porcentaje} "
        )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso3_seccionB():
    """
    Calcula y muestra:
    - El año con la menor tasa promedio de desocupación.
    - El trimestre con la menor tasa de desocupación individual.

    La función procesa los datos del archivo 'usu_individual.csv' para determinar
    la desocupación laboral a lo largo del tiempo, basada en el estado laboral de los individuos.

    Criterios:
    - Se consideran personas activas aquellas en estado 1 (ocupado) o 2 (desocupado).
    - La tasa de desocupación se calcula como: (desocupados / población activa) * 100.
    - Estado 3 (ocupado demandante) también se incluye como activo en trimestres nuevos.

    Proceso:
    - Agrupa por año y trimestre.
    - Calcula la tasa de desocupación por trimestre.
    - Identifica el trimestre con menor tasa de desocupación.
    - Calcula el promedio anual de tasas y determina el año con menor promedio.

    Salida:
    - Imprime el trimestre con menor tasa de desocupación.
    - Imprime el año con menor tasa promedio de desocupación (si hubo más de un año evaluado).
    """
    # Descripcion de los campos usados:
    """ 
    Campo ESTADO:
        Condición de actividad
            0 = Entrevista individual no realizada(no respuesta al cuestionario individual)
            1 = Ocupado
            2 = Desocupado
            3 = Inactivo
            4 = Menor de 10 años
    """
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=";")
            try:
                next(csv_reader, None)
            except StopIteration:
                print("Archivo vacio")
            anio_act = None
            tri_act = None
            tasa_min_tri = 99999
            tasa_min_anio = 99999
            anio_min = None
            tri_min = None
            desocupados = 0  # contador de desocupados
            total = 0  # contador de la cantidad de personas activas, incluye empleados y desempleados. NO incluye la
            # categoria 4 que son los inactivos
            tasa_anio = 0
            for row in csv_reader:
                if int(row["ANO4"]) == anio_act:  # x si cambio de año
                    if (
                        int(row["TRIMESTRE"]) == tri_act
                    ):  # para cuando cambia de trimestre
                        if int(row["ESTADO"]) == 1:
                            total += 1
                        elif int(row["ESTADO"]) == 2:
                            total += 1
                            desocupados += 1
                    else:
                        tasa_desocupados = desocupados / total * 100
                        if tasa_desocupados < tasa_min_tri:  # si es menor la guardo
                            tasa_min_tri = tasa_desocupados
                            tri_min = int(row["TRIMESTRE"])
                            tri_min_anio = anio_act
                        tasa_anio += tasa_desocupados
                        tri_act = int(row["TRIMESTRE"])
                        desocupados = 0  # reinicio los contadores por trimestre
                        total = 0
                        if int(row["ESTADO"]) in [1, 2]:
                            total += 1
                        elif int(row["ESTADO"]) == 3:
                            desocupados += 1
                            total += 1
                else:
                    if tasa_anio < tasa_min_anio:
                        tasa_min_anio = tasa_anio
                        anio_min = anio_act
                    tasa_anio = 0  # suma las tasa de los 4 trimestres
                    anio_act = int(row["ANO4"])
                    tri_act = int(row["TRIMESTRE"])
                    if int(row["ESTADO"]) in [1, 2]:
                        total += 1
                    elif int(row["ESTADO"]) == 3:
                        desocupados += 1
                        total += 1
        if anio_min == None:
            print(
                f"Se evaluo solo el año {tri_min_anio},el trimestre con menor tasa de desocupacion fue el trimestre"
                f"{tri_min}"
            )
        else:
            print(
                f"el año con menor tasa de desocupacion fue {anio_min} y el trimestre con menor tasa de desocupacion"
                " fue el trimestre {tri_min} del año {tri_min_anio}"
            )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso4_seccionB():
    """
    Analiza el archivo de datos de individuos para identificar los 5 aglomerados con mayor porcentaje
    de hogares que tienen al menos dos personas con nivel educativo universitario (completo o incompleto)
    en el trimestre más reciente disponible.

    La función:
    - Lee el archivo CSV separado por punto y coma.
    - Determina el año y trimestre más reciente presentes en el archivo.
    - Agrupa a las personas por hogar usando una combinación de CODUSU y número de hogar.
    - Cuenta cuántas personas con nivel educativo universitario hay en cada hogar.
    - Identifica hogares con 2 o más universitarios.
    - Calcula el porcentaje de estos hogares respecto al total de hogares por aglomerado.
    - Imprime el top 5 de aglomerados con mayor porcentaje de estos hogares.

    No recibe argumentos ni devuelve valores: imprime los resultados directamente.
    """
    # Descripcion de los campos usados:
    """ 
    Campo NIVEL_ED:
        Nivel educativo
            1 = Primario incompleto (incluye educación especial)
            2 = Primario completo
            3 = Secundario incompleto
            4 = Secundario completo
            5 = Superior universitario incompleto
            6 = Superior universitario completo
            7 = Sin instrucción
            9 = Ns/Nr
    Campo AGLOMERADO:
        Código de Aglomerado
            02 = Gran La Plata
            03 = Bahía Blanca - Cerri
            04 = Gran Rosario
            05 = Gran Santa Fé
            06 = Gran Paraná
            07 = Posadas
            08 = Gran Resistencia
            09 = Comodoro Rivadavia - Rada Tilly 
            10 = Gran Mendoza
            12 = Corrientes
            13 = Gran Córdoba
            14 = Concordia
            15 = Formosa
            17 = Neuquén - Plottier
            18 = Santiago del Estero - La Banda
            19 = Jujuy - Palpalá
            20 = Río Gallegos
            22 = Gran Catamarca
            23 = Gran Salta
            25 = La Rioja
            26 = Gran San Luis
            27 = Gran San Juan
            29 = Gran Tucumán - Tafí Viejo
            30 = Santa Rosa - Toay
            31 = Ushuaia - Río Grande
            32 = Ciudad Autónoma de Buenos Aires
            33 = Partidos del GBA
            34 = Mar del Plata
            36 = Río Cuarto
            38 = San Nicolás - Villa Constitución 
            91 = Rawson - Trelew
            93 = Viedma - Carmen de Patagones
    """
    # Para encontrar el anio y el trimestre mas reciente
    trimestres_maximos = {}
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as f:
            reader = csv.reader(f, delimiter=";")
            try:
                next(reader)
            except StopIteration:
                print("Archivo vacio")
            for row in reader:
                anio = int(row["ANO4"])
                trimestre = int(row["TRIMESTRE"])
                if (
                    anio not in trimestres_maximos
                    or trimestre > trimestres_maximos[anio]
                ):
                    trimestres_maximos[anio] = trimestre
            anio_max = max(trimestres_maximos.keys())
            trimestre_max = trimestres_maximos[anio_max]

        # Para contar los hogares con 2 o mas universitarios por aglomerado
        hogares_universitarios = {}
        hogares_totales = {}

        # Para contar personas por hogar
        personas_por_hogar = {}
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as f:
            reader = csv.reader(f, delimiter=";")
            try:
                next(reader)
            except StopIteration:
                print("Archivo vacio")
            for row in reader:
                if (
                    int(row["ANO4"]) == anio_max
                    and int(row["TRIMESTRE"]) == trimestre_max
                ):
                    hogar_id = (
                        row["CODUSU"],
                        row["NRO_HOGAR"],
                    )  # identificador unico del hogar
                    aglomerado = row["AGLOMERADO"]
                    nivel_educativo = int(row["NIVEL_ED"])
                    pondera = int(row["PONDERA"])

                    if hogar_id not in personas_por_hogar:
                        personas_por_hogar[hogar_id] = {
                            "aglomerado": aglomerado,
                            "universitarios": 0,
                            "pondera": pondera,
                        }
                    # Para saber cuántos universitarios hay en ese hogar:
                    if nivel_educativo in [5, 6]:
                        personas_por_hogar[hogar_id]["universitarios"] += 1

        for hogar_id, datos in personas_por_hogar.items():
            aglo = datos["aglomerado"]
            if aglo not in hogares_totales:
                hogares_totales[aglo] = 0
                hogares_universitarios[aglo] = 0

            hogares_totales[aglo] += 1

            if datos["universitarios"] >= 2:
                hogares_universitarios[aglo] += 1

        # Calculo de porcentajes y muestras de resultados:
        porcentajes = []
        for aglo in hogares_totales:
            total = hogares_totales[aglo]
            con_uni = hogares_universitarios[aglo]
            porcentaje = (con_uni / total) * 100 if total > 0 else 0
            porcentajes.append((aglo, porcentaje))

        porcentajes.sort(key=lambda x: x[1], reverse=True)

        print(
            f"\nTop 5 aglomerados con mayor porcentaje de hogares con 2 o más universitarios (Año {anio_max},"
            f" Trimestre {trimestre_max}):"
        )
        for aglo, porcentaje in porcentajes[:5]:
            print(f"Aglomerado {aglo}: {porcentaje:.2f}%")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso5_seccionB():
    """
    Calcula y muestra el porcentaje de hogares propietarios por aglomerado.

    Esta función lee el archivo 'usu_hogar.csv' ubicado en la ruta 'archivo_data_out_path_hogar',
    identifica la condición de tenencia de la vivienda (columna II7), y agrupa la información por
    número de aglomerado (columna AGLO). Luego calcula el porcentaje de propietarios por cada
    aglomerado y lo imprime por consola.

    Propietarios se consideran aquellos con valores 1 o 2 en la columna II7:
    - 1: Propietario de la vivienda y del terreno
    - 2: Propietario solo de la vivienda

    Salida:
    - Imprime en consola el porcentaje de propietarios para cada aglomerado en orden ascendente.
    """
    # Descripcion de los campos usados:
    """ 
    Campo II7:
        Régimen de tenencia
            01 = Propietario de la vivienda y el terreno
            02 = Propietario de la vivienda solamente
            03 = Inquilino / arrendatario de la vivienda
            04 = Ocupante por pago de impuestos / expensas
            05 = Ocupante en relación de dependencia
            06 = Ocupante gratuito (con permiso)
            07 = Ocupante de hecho (sin permiso)
            08 = Está en sucesión
    """
    estadisticas = {}
    try:
        with archivo_data_out_path_hogar.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=";")
            try:
                row = next(csv_reader)
            except StopIteration:
                print("Archivo vacio")

            for row in csv_reader:
                aglo = int(row["AGLOMERADO"])
                condicion = int(row["II7"])

                if aglo not in estadisticas:
                    estadisticas[aglo] = [0, 0]  # propietarios y total
                estadisticas[aglo][1] += 1
                if int(row["II7"]) in (
                    1,
                    2,
                ):  # propietarios vivienda y terreno y propietarios solo vivienda
                    estadisticas[aglo][0] += 1

            for aglo in sorted(
                estadisticas.keys()
            ):  # ordeno el diccionario x num de aglomerado
                propietarios = estadisticas[aglo][0]
                total = estadisticas[aglo][1]
                porcentaje = (propietarios / total) * 100
                print(f"Aglomerado {aglo}: {porcentaje:.2f}% de propietarios")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso6_seccionB():
    """
    Informa el aglomerado con mayor cantidad de viviendas que tienen más de dos ocupantes
    y no poseen baño.

    La función realiza lo siguiente:
    - Lee el archivo de hogares (`archivo_data_out_path_hogar`) separado por punto y coma.
    - Utiliza el campo IV8 para identificar si la vivienda no tiene baño (valor 2).
    - Utiliza el campo IX_TOT para obtener la cantidad total de ocupantes en la vivienda.
    - Agrupa las viviendas por aglomerado (campo AGLOMERADO).
    - Cuenta cuántas viviendas tienen más de dos ocupantes y no disponen de baño en cada aglomerado.
    - Identifica e imprime el aglomerado con la mayor cantidad de estas viviendas, junto con el total.

    No recibe argumentos ni devuelve valores: imprime el resultado directamente por consola.
    """
    # Descripcion de los campos usados:
    """ 
    Campo AGLOMERADO:
        Código de Aglomerado
            02 = Gran La Plata
            03 = Bahía Blanca - Cerri
            04 = Gran Rosario
            05 = Gran Santa Fé
            06 = Gran Paraná
            07 = Posadas
            08 = Gran Resistencia
            09 = Comodoro Rivadavia - Rada Tilly 
            10 = Gran Mendoza
            12 = Corrientes
            13 = Gran Córdoba
            14 = Concordia
            15 = Formosa
            17 = Neuquén - Plottier
            18 = Santiago del Estero - La Banda
            19 = Jujuy - Palpalá
            20 = Río Gallegos
            22 = Gran Catamarca
            23 = Gran Salta
            25 = La Rioja
            26 = Gran San Luis
            27 = Gran San Juan
            29 = Gran Tucumán - Tafí Viejo
            30 = Santa Rosa - Toay
            31 = Ushuaia - Río Grande
            32 = Ciudad Autónoma de Buenos Aires
            33 = Partidos del GBA
            34 = Mar del Plata
            36 = Río Cuarto
            38 = San Nicolás - Villa Constitución 
            91 = Rawson - Trelew
            93 = Viedma - Carmen de Patagones
    Campo IV8:
        ¿Tiene baño / letrina?
            1 = Sí
            2 = No 
    Campo IX_Tot que indica la cantidad de personas por hogar
    """
    viviendas_filtradas = {}
    try:
        with archivo_data_out_path_hogar.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            reader = csv.DictReader(archivo, delimiter=";")
            try:
                next(reader)  # Salta encabezado
            except StopIteration:
                print("Archivo vacio")
            for row in reader:
                if (
                    len(row) > max(7, 19, 64)
                    and row["AGLOMERADO"].isdigit()
                    and row["IV8"].isdigit()
                    and row["IX_TOT"].isdigit()
                ):
                    aglomerado = int(row["AGLOMERADO"])
                    tiene_banio = int(row["IV8"])
                    cantidad_personas = int(row["IX_TOT"])

                    if cantidad_personas > 2 and tiene_banio == 2:
                        viviendas_filtradas[aglomerado] = (
                            viviendas_filtradas.get(aglomerado, 0) + 1
                        )

        if viviendas_filtradas:
            aglomerado_max = max(viviendas_filtradas, key=viviendas_filtradas.get)
            cantidad_max = viviendas_filtradas[aglomerado_max]
            print(
                f"Aglomerado con mayor cantidad de viviendas con más de 2 ocupantes y sin baño: {aglomerado_max}"
            )
            print(f"Cantidad de viviendas: {cantidad_max}")
        else:
            print("No se encontraron viviendas que cumplan ambas condiciones.")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso7_SeccionB():
    """
    Calcula y muestra el porcentaje de personas con nivel educativo universitario o superior en cada aglomerado válido.

    La función:
    - Lee el archivo `archivo_data_out_path_individual` con delimitador `;`.
    - Evalúa el nivel educativo y el número de aglomerado de residencia  de cada persona.
    - Solo considera aglomerados específicos definidos como válidos.
    - Cuenta cuántas personas hay en total y cuántas alcanzaron un nivel universitario o superior por aglomerado.
    - Calcula el promedio de personas con nivel universitario respecto del total en cada aglomerado válido.
    - Imprime los resultados formateados con el nombre del aglomerado y el porcentaje correspondiente.

    Esta función no recibe parámetros ni devuelve valores, pero imprime en consola los resultados calculados.

    """
    # Descripcion de los campos usados:
    """ 
    Campo CH12:
        ¿Cuál es el nivel más alto que cursa o cursó?
            1 = Jardín/preescolar
            2 = Primario
            3 = EGB
            4 = Secundario
            5 = Polimodal
            6 = Terciario
            7 = Universitario
            8 = Posgrado universitario
            9 = Educación especial (discapacitado)
    """
    aglo_validos = {
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        12,
        13,
        14,
        15,
        17,
        18,
        19,
        20,
        22,
        23,
        25,
        26,
        27,
        29,
        30,
        31,
        32,
        33,
        34,
        36,
        38,
        91,
        93,
    }

    contar = {k: {"niveles": 0, "personas": 0} for k in aglo_validos}
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=";")
            try:
                next(csv_reader)  # me salto el encabezado
            except StopIteration:
                print("Archivo vacio")
            for row in csv_reader:
                aglomerado = int(row["AGLOMERADO"])
                nivel = int(row["CH12"])
                if aglomerado in contar:
                    contar[aglomerado][
                        "personas"
                    ] += 1  # cuento la cantidad de personas
                    if nivel in range(7, 9):
                        contar[aglomerado][
                            "niveles"
                        ] += 1  # cuento las personas con nivel universitario o superior
        aglomerados = {
            "2": "Gran La Plata",
            "3": "Bahía Blanca-Cerri",
            "4": "Gran Rosario",
            "5": "Gran Santa Fe",
            "6": "Gran Paraná",
            "7": "Posadas",
            "8": "Gran Resistencia",
            "9": "Comodoro Rivadavia-Rada Tilly",
            "10": "Gran Mendoza",
            "12": "Corrientes",
            "13": "Gran Córdoba",
            "14": "Concordia",
            "15": "Formosa",
            "17": "Neuquén-Plottier",
            "18": "Santiago del Estero-La Banda",
            "19": "Jujuy-Palpalá",
            "20": "Río Gallegos",
            "22": "Gran Catamarca",
            "23": "Gran Salta",
            "25": "La Rioja",
            "26": "Gran San Luis",
            "27": "Gran San Juan",
            "29": "Gran Tucumán-Tafí Viejo",
            "30": "Santa Rosa-Toay",
            "31": "Ushuaia-Río Grande",
            "32": "Ciudad Autónoma de Buenos Aires",
            "33": "Partidos del Gran Buenos Aires",
            "34": "Mar del Plata",
            "36": "Río Cuarto",
            "38": "San Nicolás-Villa Constitución",
            "91": "Rawson-Trelew",
            "93": "Viedma-Carmen de Patagones",
        }
        print("Promedio de personas que cursaron nivel universitario o superior")
        print("-" * 30)
        for aglomerado in sorted(contar):
            personas = contar[aglomerado]["personas"]
            niveles = contar[aglomerado]["niveles"]
            promedio = (
                niveles / personas if personas > 0 else 0
            )  # saca el promedio. Si persona = 0 envia 0
            nombre = aglomerados[str(aglomerado)]  # obtiene el nombre del aglomerado
            print(f" - {nombre}: {promedio:.2%}")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso8_SeccionB():
    """
    Calcula y muestra el porcentaje de personas inquilinas por región, ordenado de mayor a menor.

    La función:
    - Lee datos del archivo `archivo_data_out_path_hogar` con separador `;`.
    - Considera solo las regiones con códigos: 1 (GBA), 40 (NOA), 41 (NEA), 42 (Cuyo), 43 (Pampeana) y 44 (Patagonia).
    - Para cada región:
        - Cuenta el total de personas.
        - Cuenta cuántas viven en condición de inquilinato.
    - Calcula el porcentaje de inquilinos sobre el total de personas en cada región.
    - Ordena los resultados de mayor a menor y los imprime en consola con el nombre descriptivo de cada región.

    - En caso de que una región no tenga personas registradas, el porcentaje será 0.
    - No retorna datos, solo imprime los resultados.

    Esta función permite comparar las regiones del país según la proporción de personas que alquilan su vivienda.

    """
    # Descripcion de los campos usados:
    """ 
    Campo REGION:
        Código de región
            01 = Gran Buenos Aires
            40 = Noroeste
            41 = Noreste
            42 = Cuyo
            43 = Pampeana
            44 = Patagonia
    campo II7:
        Régimen de tenencia
            01 = Propietario de la vivienda y el terreno
            02 = Propietario de la vivienda solamente
            03 = Inquilino / arrendatario de la vivienda
            04 = Ocupante por pago de impuestos / expensas
            05 = Ocupante en relación de dependencia
            06 = Ocupante gratuito (con permiso)
            07 = Ocupante de hecho (sin permiso)
            08 = Está en sucesión
    Campo IX_Tot que indica la cantidad de personas por hogar
    """
    codigos = {1, 40, 41, 42, 43, 44}

    contar = {k: {"total": 0, "inquilinos": 0} for k in codigos}
    try:
        with archivo_data_out_path_hogar.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=";")
            try:
                next(csv_reader)  # me salto el encabezado
            except StopIteration:
                print("Archivo vacio")
            for row in csv_reader:
                region = int(row["REGION"])
                regimen = int(row["II7"])
                personas = int(row["IX_TOT"])
                if region in contar:
                    contar[region]["total"] += personas
                    if regimen == 3:
                        contar[region]["inquilinos"] += personas

        resultado = []
        for item in sorted(contar):
            personas = contar[item]["total"]
            inquilinos = contar[item]["inquilinos"]
            if personas > 0:
                porcentaje = (inquilinos / personas) * 100
            else:
                porcentaje = 0
            resultado.append((item, porcentaje))

        region_nombres = {
            1: "Gran Buenos Aires",
            40: "Noroeste",
            41: "Noreste",
            42: "Cuyo",
            43: "Pampeana",
            44: "Patagonia",
        }
        print("Orden de las regiones segun el porcentaje de inquilinos")
        print("-" * 30)
        resultados_ordenados = sorted(resultado, key=lambda x: x[1], reverse=True)
        for region_code, porcentaje in resultados_ordenados:
            nombre = region_nombres[region_code]
            print(f"Región {nombre}: {porcentaje:.2f}% inquilinos")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def procesar_persona(row, lista_datos):
    """
    Procesa la información educativa de una persona adulta y actualiza una lista acumulativa por nivel educativo.

    Parámetros:
    ----------
    row : list
        Fila del archivo CSV que contiene los datos de una persona.
    lista_datos :
        Lista de acumuladores donde se suma la ponderación de personas según su nivel educativo.
        El índice de esta lista representa el código del nivel educativo.
    index_pondera : int
        Índice en `row` que indica la columna de ponderación.
    index_CH06 : int
        Índice en `row` que indica la edad de la persona.
    index_NIVEL_ED : int
        Índice en `row` que indica el nivel educativo alcanzado (NIVEL_ED).

    Lógica:
    ------
    - Solo se procesan personas de 18 años o más.
    - Los niveles educativos con código 5 (universitario incompleto) y 6 (universitario completo) se agrupan en el
    índice 6.
    - Se ignoran los niveles con código 7 y 9.
    - Para los niveles válidos, se incrementa el valor correspondiente en `lista_datos` usando el valor de `PONDERA`.

    No retorna nada; modifica `lista_datos` en el lugar.

    """
    if int(row["CH06"]) >= 18:
        clave_nivel_educativo = int(row["NIVEL_ED"])
        if clave_nivel_educativo == 5 or clave_nivel_educativo == 6:
            clave_nivel_educativo = 5
        if clave_nivel_educativo != 7 and clave_nivel_educativo != 9:
            lista_datos[clave_nivel_educativo + 1] += int(row["PONDERA"])


def inciso9_SeccionB():
    """
    Genera una tabla que muestra la cantidad de personas mayores de edad según el nivel educativo alcanzado
    en un aglomerado urbano específico, agrupadas por año y trimestre.

    Proceso:
    --------
    - Solicita al usuario el código de un aglomerado urbano entre los disponibles.
    - Recorre el archivo CSV de personas (`archivo_data_out_path_individual`).
    - Filtra los registros correspondientes al aglomerado seleccionado.
    - Para cada año y trimestre, agrupa la cantidad de personas de 18 años o más según su nivel educativo:
        - Primario incompleto
        - Primario completo
        - Secundario incompleto
        - Secundario completo
        - Superior o universitario
    - Muestra la información agrupada en una tabla ordenada por año y trimestre.

    Condiciones:
    ------------
    - Solo se consideran personas de 18 años o más.
    - La agrupación se reinicia cuando cambia el año o trimestre.
    - La ponderación (`PONDERA`) se aplica al total de personas por nivel educativo.

    Entradas del usuario:
    ---------------------
    - Código de aglomerado urbano (entero), que se muestra previamente con su descripción.

    Salida:
    -------
    - Imprime en consola una tabla con columnas:
        ['Año', 'Trimestre', 'Primario incompleto', 'Primario completo',
         'Secundario Incompleto', 'Secundario Completo', 'Superior o universitario']
    """
    try:
        with archivo_data_out_path_individual.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            aglomerados = {
                "2": "Gran La Plata",
                "3": "Bahía Blanca-Cerri",
                "4": "Gran Rosario",
                "5": "Gran Santa Fe",
                "6": "Gran Paraná",
                "7": "Posadas",
                "8": "Gran Resistencia",
                "9": "Comodoro Rivadavia-Rada Tilly",
                "10": "Gran Mendoza",
                "12": "Corrientes",
                "13": "Gran Córdoba",
                "14": "Concordia",
                "15": "Formosa",
                "17": "Neuquén-Plottier",
                "18": "Santiago del Estero-La Banda",
                "19": "Jujuy-Palpalá",
                "20": "Río Gallegos",
                "22": "Gran Catamarca",
                "23": "Gran Salta",
                "25": "La Rioja",
                "26": "Gran San Luis",
                "27": "Gran San Juan",
                "29": "Gran Tucumán-Tafí Viejo",
                "30": "Santa Rosa-Toay",
                "31": "Ushuaia-Río Grande",
                "32": "Ciudad Autónoma de Buenos Aires",
                "33": "Partidos del Gran Buenos Aires",
                "34": "Mar del Plata",
                "36": "Río Cuarto",
                "38": "San Nicolás-Villa Constitución",
                "91": "Rawson-Trelew",
                "93": "Viedma-Carmen de Patagones",
            }
            for codigo, nombre in aglomerados.items():
                print(f"{codigo} = {nombre}")
            texto = (
                "Ingrese el codigo del aglomerado que quieras para retornar"
                " una tabla que contenga la cantidad de personas mayores"
                " de edad según su nivel de estudios alcanzados."
            )
            aglomerado = int(input(texto))
            tabla = []
            encabezado_tabla = [
                "Año",
                "Trimestre",
                "Primario incompleto",
                "Primario completo",
                "Secundario Incompleto",
                "Secundario Completo",
                "Superior o universitario",
            ]
            tabla.append(encabezado_tabla)
            csv_reader = csv.DictReader(archivo, delimiter=";")
            try:
                next(csv_reader)
            except StopIteration:
                print("Archivo vacio")
            actual_anio = 0
            actual_trimestre = 0
            for row in csv_reader:
                if int(row["AGLOMERADO"]) == aglomerado:
                    if (actual_anio == 0) and (
                        actual_trimestre == 0
                    ):  # sirve para inicializar en la 1era iteracion
                        actual_anio = int(row["ANO4"])
                        actual_trimestre = int(row["TRIMESTRE"])
                        lista_datos = [0, 0, 0, 0, 0, 0, 0]  # Año, Trim, 5 niveles
                        lista_datos[0] = actual_anio
                        lista_datos[1] = actual_trimestre
                    if (
                        int(row["ANO4"]) == actual_anio
                        and int(row["TRIMESTRE"]) == actual_trimestre
                    ):
                        # Procesa la persona
                        procesar_persona(row, lista_datos)
                    else:
                        tabla.append(lista_datos.copy())
                        actual_anio = int(row["ANO4"])
                        actual_trimestre = int(row["TRIMESTRE"])
                        lista_datos = [0, 0, 0, 0, 0, 0, 0]  # Año, Trim, 5 niveles
                        lista_datos[0] = actual_anio
                        lista_datos[1] = actual_trimestre
                        # Procesa la persona
                        procesar_persona(row, lista_datos)
            tabla.append(lista_datos)

            for fila in tabla:
                print(
                    f"| {fila[0]:<6} | {fila[1]:<9} | {fila[2]:<19} | {fila[3]:<17} | {fila[4]:<21} | {fila[5]:<19}"
                    f" | {fila[6]:<24} |"
                )
                print("-" * 137)
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def calc_porcentaje_inciso10_SeccionB(d):
    """
    Calcula el porcentaje de personas con secundario incompleto respecto al total de personas mayores de edad.
    Parámetros:
    d : dict
        Diccionario que contiene las claves 'sec_inc' (personas con secundario incompleto) y 'mayores' (total de
        personas mayores de edad).
    Retorna:
    float
        Porcentaje de personas con secundario incompleto respecto al total de personas mayores de edad.
    Lógica:
    - Si el total de personas mayores es mayor que 0, calcula el porcentaje.
    - Si no, retorna 0 para evitar división por cero.

    """
    return (d["sec_inc"] / d["mayores"] * 100) if d["mayores"] > 0 else 0


def inciso10_SeccionB():
    """

    Calcula y muestra el porcentaje de personas mayores de edad con secundario incompleto en dos aglomerados
    seleccionados por el usuario.

    La función:
    - Lee el archivo CSV de datos individuales (`archivo_data_out_path_individual`).
    - Solicita al usuario que ingrese el código de dos aglomerados.
    - Filtra los datos para incluir solo las personas mayores de 18 años en los aglomerados seleccionados.
    - Agrupa los datos por año y trimestre, y cuenta la cantidad de personas mayores de edad y las que tienen
    secundario incompleto.
    - Calcula el porcentaje de personas con secundario incompleto respecto al total de personas mayores de edad para
      cada aglomerado.
    - Imprime los resultados en una tabla ordenada por año y trimestre.

    Esta función no recibe argumentos ni devuelve valores; interactúa directamente con el usuario y muestra los
      resultados por consola.

    """

    aglomerados = {
        "2": "Gran La Plata",
        "3": "Bahía Blanca-Cerri",
        "4": "Gran Rosario",
        "5": "Gran Santa Fe",
        "6": "Gran Paraná",
        "7": "Posadas",
        "8": "Gran Resistencia",
        "9": "Comodoro Rivadavia-Rada Tilly",
        "10": "Gran Mendoza",
        "12": "Corrientes",
        "13": "Gran Córdoba",
        "14": "Concordia",
        "15": "Formosa",
        "17": "Neuquén-Plottier",
        "18": "Santiago del Estero-La Banda",
        "19": "Jujuy-Palpalá",
        "20": "Río Gallegos",
        "22": "Gran Catamarca",
        "23": "Gran Salta",
        "25": "La Rioja",
        "26": "Gran San Luis",
        "27": "Gran San Juan",
        "29": "Gran Tucumán-Tafí Viejo",
        "30": "Santa Rosa-Toay",
        "31": "Ushuaia-Río Grande",
        "32": "Ciudad Autónoma de Buenos Aires",
        "33": "Partidos del Gran Buenos Aires",
        "34": "Mar del Plata",
        "36": "Río Cuarto",
        "38": "San Nicolás-Villa Constitución",
        "91": "Rawson-Trelew",
        "93": "Viedma-Carmen de Patagones",
    }
    for codigo, nombre in aglomerados.items():
        print(f"{codigo} = {nombre}")
    print(
        "Ingrese el codigo de dos aglomerados para retornar una tabla que contenga la cantidad de personas mayores"
        " de edad con secundario incompleto:"
    )
    aglo1 = int(input("Ingrese el codigo del aglomerado A"))
    aglo2 = int(input("Ingrese el codigo del aglomerado B"))

    # Diccionario: {(año, trimestre): {aglomerado: {"mayores": int, "sec_inc": int}}}
    estadisticas = {}
    try:
        with open(
            archivo_data_out_path_individual, newline="", encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            for fila in lector:
                aglo = int(fila["AGLOMERADO"])
                if aglo == aglo1 or aglo == aglo2:
                    edad = int(fila["CH06"])
                    nivel = int(fila["NIVEL_ED"])
                    anio = fila["ANO4"]
                    trimestre = fila["TRIMESTRE"]
                    if edad > 18:
                        clave = (anio, trimestre)
                        if clave not in estadisticas:
                            estadisticas[clave] = {
                                aglo1: {"mayores": 0, "sec_inc": 0},
                                aglo2: {"mayores": 0, "sec_inc": 0},
                            }
                        estadisticas[clave][aglo]["mayores"] += int(fila["PONDERA"])
                        if nivel == 3:
                            estadisticas[clave][aglo]["sec_inc"] += int(fila["PONDERA"])

        # Imprimir resultados
        print(
            f"\n| {'Año':<6} | {'Trimestre':<10} | {f'Aglomerado {aglo1}':<20} | {f'Aglomerado {aglo2}':<20} |"
        )
        print("|" + "-" * 67 + "|")
        for clave in sorted(estadisticas):
            anio, trimestre = clave
            fila_aglo1 = estadisticas[clave][aglo1]
            fila_aglo2 = estadisticas[clave][aglo2]
            porc1 = f"{calc_porcentaje_inciso10_SeccionB(fila_aglo1):.1f}%"
            porc2 = f"{calc_porcentaje_inciso10_SeccionB(fila_aglo2):.1f}%"
            print(f"| {anio:<6} | {trimestre:<10} | {porc1:<20} | {porc2:<20} |")
            print("|" + "-" * 67 + "|")
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso11_seccionB():
    """Dado un año ingresado por el usuario, calcula e imprime el mayor y el menor porcentaje de viviendas de
    Material Precario del ultimo trimestre almacenado en ese año

    La función:
    -Crea un diccionario para guardar el maximo y el minimo y otro para guardar los porcentajes de los aglomerados.
    -Abre el archivo
    -Le pido al usuario que ingrese un año para realizar la busqueda
    -Recorro el archivo csv, si encuentro un trimestre nuevo (y es el ultimo) borro el diccionario y le cargo las
    viviendas que tienen material precario y el total de viviendas  a cada aglomerado
    -Ordeno el diccionario 'aglomerados' y calculo e imprimo el porcentaje de viviendas de material precario
    """

    max_min = {"min": None, "max": None}  # guardo max y min
    aglomerados = {}  # guardo los porcentajes de los aglomerados
    try:
        with archivo_data_out_path_hogar.open(
            "r", newline="", encoding="utf-8"
        ) as archivo:
            csv_reader = csv.DictReader(archivo, delimiter=";")
            texto = (
                "Ingrese el año para buscar los aglomerados con el menor"
                ' y el mayor porcentaje de viviendas de "material" precario:'
            )
            anio = int(input(texto))
            ult_trimestre = 0
            min = None
            max = None
            for row in csv_reader:
                if anio == int(row["ANO4"]):
                    aglo = int(row["AGLOMERADO"])
                    trimestre = int(row["TRIMESTRE"])
                    pondera = int(row["PONDERA"])
                    material = row["MATERIAL_TECHUMBRE"]
                    if trimestre > ult_trimestre:
                        aglomerados.clear()  # si hay un nuevo ult trimestre borro el contenido del diccionario
                        ult_trimestre = trimestre
                    if trimestre == ult_trimestre:
                        if aglo not in aglomerados:
                            aglomerados[aglo] = [0, 0]  # material precario y el total
                        if material == "Material precario":
                            aglomerados[aglo][0] += pondera
                        aglomerados[aglo][1] += pondera

            for aglo in sorted(aglomerados.keys()):
                mat_precario = aglomerados[aglo][0]
                total = aglomerados[aglo][1]
                porcentaje = (mat_precario / total) * 100
                if max_min["max"] is None or porcentaje > max_min["max"]["porcentaje"]:
                    max_min["max"] = {"aglomerado": aglo, "porcentaje": porcentaje}
                if max_min["min"] is None or porcentaje < max_min["min"]["porcentaje"]:
                    max_min["min"] = {"aglomerado": aglo, "porcentaje": porcentaje}
            if max_min["max"] and max_min["min"]:
                print(f"Último trimestre: {ult_trimestre}, Año: {anio}")
                print(
                    f"Aglomerado con mayor porcentaje: {max_min['max']['aglomerado']}"
                    f"({max_min['max']['porcentaje']:.2f}% )"
                )
                print(
                    f"Aglomerado con menor porcentaje: {max_min['min']['aglomerado']}"
                    f"({max_min['min']['porcentaje']:.2f}%)"
                )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso12_seccionB():
    """Utilizo último trimestre almacenado en el sistema y calculo  para cada aglomerado el porcentaje de jubilados que
    vivan en una vivienda con CONDICION_DE_HABITABILIDAD insuficiente.

    La función:
    -Creo 2 diccionarios uno para guardar el codusu y el nro de hogar de las viviendas y otro para guardar los
    porcentajes
    - Abro el archivo individual y el de hogar
    -recorro primero el de hogar guardando  codusu y el nro de hogar de las viviendas que viven en condiciones de
    habitabilidad 'Insuficientes'. Si aparece un nuevo 'ultimo año o trimestre' borro el diccionario y lo cargo con
    la info nueva
    -Recorro el archivo individual si coincidide el año y trimestre con el ultimo año y trimestre del archivo hogar y
    es jubilado guardo el contenido de pondera en estadisticas y si cumple con la condicion de habitabilidad tambien
    lo agrego
    -Calculo e imprimo el porcentaje de de jubilados que viven en condiciones insuficientes para cada aglomerado
    """
    estadisticas = {}
    hogares_insuficientes = {}
    # Leer ambos archivos con csv.reader
    try:
        with (
            archivo_data_out_path_hogar.open(
                "r", newline="", encoding="utf-8"
            ) as archivo1,
            archivo_data_out_path_individual.open(
                "r", newline="", encoding="utf-8"
            ) as archivo2,
        ):
            lector1 = csv.DictReader(archivo1, delimiter=";")
            lector2 = csv.DictReader(archivo2, delimiter=";")
            ultimo_anio = 0
            ultimo_trimestre = 0

            for row in lector1:
                anio1 = int(row["ANO4"])
                tri1 = int(row["TRIMESTRE"])
                habitabilidad = row["CONDICION_DE_HABITABILIDAD"]
                aglo = int(row["AGLOMERADO"])
                usu_hogar = row["CODUSU"]
                nro_hogar = int(row["NRO_HOGAR"])
                if anio1 > ultimo_anio:
                    hogares_insuficientes.clear()
                    ultimo_anio = anio1
                    ultimo_trimestre = tri1
                elif anio1 == ultimo_anio and tri1 > ultimo_trimestre:
                    hogares_insuficientes.clear()
                    ultimo_trimestre = tri1
                if ultimo_anio == anio1 and tri1 == ultimo_trimestre:
                    if habitabilidad == "Insuficiente":
                        hogares_insuficientes[(usu_hogar, nro_hogar)] = aglo

            for row2 in lector2:
                anio2 = int(row2["ANO4"])
                tri2 = int(row2["TRIMESTRE"])
                aglo = int(row2["AGLOMERADO"])
                pondera = int(row2["PONDERA"])
                usu_hogar = row2["CODUSU"]  # Definir usu_hogar para este archivo
                nro_hogar = int(row2["NRO_HOGAR"])
                if ultimo_anio == anio2 and tri2 == ultimo_trimestre:
                    if (
                        int(row2["CAT_INAC"]) == 1
                    ):  # si el contenido es 1 = pensionado/jubilado
                        if aglo not in estadisticas:
                            estadisticas[aglo] = [
                                0.0,
                                0.0,
                            ]  # [jubilados en hogar insuf, total jubilados]
                        if (usu_hogar, nro_hogar) in hogares_insuficientes:
                            estadisticas[aglo][
                                0
                            ] += pondera  # Jubilados en hogares insuficientes
                        estadisticas[aglo][1] += pondera  # Total jubilados

            for aglo in sorted(estadisticas.keys()):
                jub_insuf = estadisticas[aglo][0]
                jub_total = estadisticas[aglo][1]
                try:
                    porcentaje = (jub_insuf / jub_total) * 100
                except ZeroDivisionError:
                    porcentaje = 0.0
                print(
                    f"aglomerado {aglo}: {porcentaje:.2f}% de jubilados en condiciones de"
                    f" habitabilidad insuficientes"
                )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")


def inciso13_seccionB():
    hogares_insuficientes = set()
    try:
        with (
            archivo_data_out_path_hogar.open(
                "r", newline="", encoding="utf-8"
            ) as archivo1,
            archivo_data_out_path_individual.open(
                "r", newline="", encoding="utf-8"
            ) as archivo2,
        ):
            # Leer ambos archivos con csv.reader
            lector1 = csv.DictReader(archivo1, delimiter=";")
            lector2 = csv.DictReader(archivo2, delimiter=";")
            texto = (
                "ingrese el año para informar la cantidad de personas que hayan cursado "
                "nivel universitario o superior y que vivan en una vivienda con CONDICION_DE_HABITABILIDAD "
                "insuficiente en el ultimo trimestre"
            )
            anio_seleccionado = int(input(texto))
            ultimo_trimestre = 0
            cant = 0
            for row in lector1:
                anio1 = int(row["ANO4"])
                tri1 = int(row["TRIMESTRE"])
                habitabilidad = row["CONDICION_DE_HABITABILIDAD"]
                usu_hogar = row["CODUSU"]
                nro_hogar = int(row["NRO_HOGAR"])
                if anio1 == anio_seleccionado and tri1 > ultimo_trimestre:
                    hogares_insuficientes.clear()
                    ultimo_trimestre = tri1
                if anio1 == anio_seleccionado and tri1 == ultimo_trimestre:
                    if habitabilidad == "Insuficiente":
                        hogares_insuficientes.add((usu_hogar, nro_hogar))

            for row2 in lector2:
                anio2 = int(row2["ANO4"])
                tri2 = int(row2["TRIMESTRE"])
                usu_hogar = row2["CODUSU"]
                nro_hogar = int(row2["NRO_HOGAR"])
                nivel_ed = row2["NIVEL_ED_str"]
                pondera = int(row2["PONDERA"])
                if anio2 == anio_seleccionado and tri2 == ultimo_trimestre:
                    if (usu_hogar, nro_hogar) in hogares_insuficientes:
                        if nivel_ed == "Superior o Universitario":
                            cant += pondera
            print(
                f"La cantidad de personas que han cursado nivel universitario o superior y que"
                f" vivan en una vivienda con CONDICION_DE_HABITABILIDAD insuficiente es: {cant}"
            )
    except FileNotFoundError:
        print("Error: Uno de los archivos CSV no se encuentra.")
