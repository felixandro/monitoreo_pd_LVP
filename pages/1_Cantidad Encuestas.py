import streamlit as st
from src.database import cargar_bbdd
from ui.quantity_surveys import success_sampling_rate_df, resume_by_design_df

# --------------------------------------------------
# Variables de Estado
# --------------------------------------------------

if "database" not in st.session_state:
    st.session_state["database"] = cargar_bbdd("pd_lvp_verano")

#--------------------------------------------------
# Frontend Página
#--------------------------------------------------

st.header("Cantidad de Encuestas")

success_sampling_rate_df("pc", "Lugar")

success_sampling_rate_df("id_encuestador", "Encuestador")

resume_by_design_df("tj1_dis", "Diseño")
