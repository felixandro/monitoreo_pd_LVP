import streamlit as st
from src.database import cargar_bbdd
import ui.config_inicio as ci

# --------------------------------------------------
# Configuración general de la app
# --------------------------------------------------
st.set_page_config(
    page_title = "Monitoreo PD",
    layout="centered",
    initial_sidebar_state="auto"
)

# --------------------------------------------------
# Variables de Estado
# --------------------------------------------------

if "database" not in st.session_state:
    st.session_state["database"] = cargar_bbdd("pd_lvp_verano")

if "database_filtered" not in st.session_state:
    st.session_state["database_filtered"] = st.session_state["database"].copy()

if "t_pd_min" not in st.session_state:
    st.session_state["tpd_min"] = 0

#--------------------------------------------------
# Pantalla de Configuración
#--------------------------------------------------

st.title("Monitoreo PD Tren LVP")

ci.generate_date_inputs()

ci.validation_times_ui()

ci.filter_button()

st.divider()

st.write("## Base de Datos Completa")
st.write(st.session_state["database"])

st.write("## Base de Datos Filtrada")
st.write(st.session_state["database_filtered"])

