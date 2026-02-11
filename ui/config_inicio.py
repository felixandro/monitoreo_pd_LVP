import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from src.database import filtrar_database, agregar_val_col_tpd_min, agregar_val_col_tpd_pro, agregar_val_col_choice, agregar_val_col, agregar_val2_col
from src.choice_data import format_database

def generate_date_inputs():

    st.divider()

    st.write("## Definir Periodo a Monitorear")
    
    fecha_inicio = st.date_input("Día Inicio", value=datetime.now().date())
    hora_inicio_local = st.time_input("Hora de Inicio", value=pd.to_datetime("09:00:00").time())
    fecha_fin = st.date_input("Día Fin", value=datetime.now().date())
    hora_fin_local = st.time_input("Hora de Fin", value=pd.to_datetime("20:00:00").time())

    def combinar_y_formatear_fecha_hora(fecha, hora):
        return datetime.combine(fecha, hora).strftime("%Y-%m-%dT%H:%M:%S%z") + "+00:00"

    start_date = combinar_y_formatear_fecha_hora(fecha_inicio, hora_inicio_local)
    end_date = combinar_y_formatear_fecha_hora(fecha_fin, hora_fin_local)

    st.session_state["start_date"] = start_date
    st.session_state["end_date"] = end_date

def filter_button():
    st.divider()

    filter_button = st.button("Filtrar Datos")
    if filter_button:
        filtrar_database()
        agregar_val_col_tpd_min()
        agregar_val_col_tpd_pro()
        agregar_val_col_choice()
        agregar_val_col()
        agregar_val2_col()
        format_valid_database()
        biogeme_format_database()
        st.success("Datos filtrados correctamente.")

def validation_times_ui():
    st.divider()
        
    tpd_min = st.number_input(
        "Tiempo Mínimo por PD (en segundos)",
        value=2,
        min_value=0,
        step=1,
        key="tpd_min_input"
    )

    st.session_state["tpd_min"] = tpd_min

    tpd_pro = st.number_input(
        "Tiempo Promedio Mínimo por PD (en segundos)",
        value=4,
        min_value=0,
        step=1,
        key="tpd_pro_input"
    )

    st.session_state["tpd_pro"] = tpd_pro

def format_valid_database():
    df = st.session_state["database_filtered"].copy()
    df_valid = df[df["VAL2"] == 1].copy()
    format_df = format_database(df_valid)
    st.session_state["formatted_database"] = format_df

def biogeme_format_database():
    df = st.session_state["formatted_database"].copy()
    biogeme_df = df[["tv1","c1","ta1","f1",
                     "tv2","c2","ta2","f2",]]
    st.session_state["biogeme_database"] = biogeme_df

