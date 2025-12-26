import streamlit as st
from pathlib import Path

import sys
# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.fechas import obtener_desde_fecha, obtener_hasta_fecha


def obtener_fechas():
    desdeFecha = obtener_desde_fecha()
    hastaFecha = obtener_hasta_fecha()

    st.write(f'El sistema contiene información desde el {desdeFecha} hasta el {hastaFecha}.')

obtener_fechas()
#boton de reinicio
#from src.button import reiniciar
from src.main import cargar_dataset
def reiniciar():
    if st.button("Forzar actualización del dataset"):
        cargar_dataset()
        st.rerun()
reiniciar()