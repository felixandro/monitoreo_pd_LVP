import streamlit as st
from src.database import cargar_bbdd
import ui.responses_time as rt

# --------------------------------------------------
# Variables de Estado
# --------------------------------------------------

if "database" not in st.session_state:
    st.session_state["database"] = cargar_bbdd("pd_lvp_verano")

#--------------------------------------------------
# Frontend Página
#--------------------------------------------------

st.header("Tiempos de Respuesta")

rt.responses_time_screen()

encuestador_selected = rt.surveyors_selectbox()

rt.responses_time_screen(encuestador_selected)

rt.mean_time_figure(encuestador_selected)

pd_multiselect = rt.pd_multiselect()

rt.evolucion_time_figure(encuestador_selected, pd_multiselect)