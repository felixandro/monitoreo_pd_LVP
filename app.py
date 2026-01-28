import streamlit as st

from src.database import cargar_bbdd
import src.statistics as stats

from ui.encuestas_x_pc import success_sampling_rate_screen
from ui.responses_time import responses_time_screen
from ui.surveyor_location import surveyor_location_screen

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

if "databse" not in st.session_state:
    st.session_state["database"] = cargar_bbdd("pd_lvp_verano")
    #st.session_state["database"].to_csv("data/data.csv", index=False, sep = ";", encoding="utf-8")


#--------------------------------------------------
# Pantallas
#--------------------------------------------------

st.title("Monitoreo PD Tren LVP")

#--------------------------------------------------
# Encuestas por Punto de Control
#--------------------------------------------------

#surveys_by_pc_screen()

st.header("Cantidad de Encuestas")

success_sampling_rate_screen("pc", "Lugar")

success_sampling_rate_screen("id_encuestador", "Encuestador")


responses_time_screen()

surveyor_location_screen()

st.divider()

st.write(st.session_state["database"])


