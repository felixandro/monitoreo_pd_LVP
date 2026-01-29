import streamlit as st
import pandas as pd

#--------------------------------------------------
# Funciones Para Generar Resumenes de Cantidad de Encuestas
#--------------------------------------------------

def generate_surveys_resume_df(df, original_col_name, new_col_name):

    df_aux = pd.DataFrame()
    df_aux[new_col_name] = df[original_col_name].copy()
    df_aux["VAL_tmin"] = df["VAL_TPD_MIN"].copy()
    df_aux["VAL_tpro"] = df["VAL_TPD_PRO"].copy()
    df_aux["VAL_choice"] = df["VAL_CHOICE"].copy()
    df_aux["VAL"] = df["VAL"].copy()
    df_aux["VAL2"] = df["VAL2"].copy()
    df_aux["Completadas"] = df["surveyor_lat"].notna().astype(int)
    df_aux["Total"] = 1
    
    df_surveys_by_pc = df_aux.groupby(new_col_name).sum().reset_index()
    df_surveys_by_pc["%"] = (df_surveys_by_pc["Completadas"] / df_surveys_by_pc["Total"].replace(0, 1) * 100).round()

    # Agregar fila de totales

    # Calcular totales
    total_tpd_min = df_surveys_by_pc["VAL_tmin"].sum()
    total_tpd_pro = df_surveys_by_pc["VAL_tpro"].sum()
    total_choice = df_surveys_by_pc["VAL_choice"].sum()
    total_val = df_surveys_by_pc["VAL"].sum()
    total_val2 = df_surveys_by_pc["VAL2"].sum()
    total_completadas = df_surveys_by_pc["Completadas"].sum()
    total_total = df_surveys_by_pc["Total"].sum()
    total_porcentaje = round((total_completadas / total_total) * 100) if total_total != 0 else 0

    # Crear fila de totales
    fila_totales = pd.DataFrame({
        new_col_name: ["TOTAL"],
        "VAL_tmin": [total_tpd_min],
        "VAL_tpro": [total_tpd_pro],
        "VAL_choice": [total_choice],
        "VAL": [total_val],
        "VAL2": [total_val2],
        "Completadas": [total_completadas],
        "Total": [total_total],
        "%": [total_porcentaje]
    })

    # Agregar fila de totales al DataFrame
    df_surveys_by_pc = pd.concat([df_surveys_by_pc, fila_totales], ignore_index=True)
    df_surveys_by_pc.set_index(new_col_name, inplace=True)
    
    return df_surveys_by_pc
    
def generate_survey_resume_by_design_df(df, original_col_name, new_col_name):

    df_aux = pd.DataFrame()
    df_aux[new_col_name] = df[original_col_name].copy()
    df_aux["VAL_tmin"] = df["VAL_TPD_MIN"].copy()
    df_aux["VAL_tpro"] = df["VAL_TPD_PRO"].copy()
    df_aux["VAL_choice"] = df["VAL_CHOICE"].copy()
    df_aux["VAL"] = df["VAL"].copy()
    df_aux["VAL2"] = df["VAL2"].copy()
    df_aux["Completadas"] = df["surveyor_lat"].notna().astype(int)
    
    df_surveys_by_design = df_aux.groupby(new_col_name).sum().reset_index()
    df_surveys_by_design.set_index(new_col_name, inplace=True)

    return df_surveys_by_design

#--------------------------------------------------
# Elementos UI
#--------------------------------------------------

def success_sampling_rate_df(original_col_name, new_col_name):    

    st.divider()

    st.subheader(f"Análisis por {new_col_name}")

    df = st.session_state["database_filtered"]

    df_surveys_by_pc = generate_surveys_resume_df(df, original_col_name, new_col_name)
    
    st.dataframe(df_surveys_by_pc, use_container_width=False)

    st.markdown("**Completadas:** Encuestas que cumplieron con el perfilamiento.")
    st.markdown("**Total:** Encuestas Iniciadas.")
    st.markdown("**Tasa (%):** = (Completadas / Total) * 100")

def resume_by_design_df(original_col_name, new_col_name):

    st.divider()

    st.subheader(f"Análisis por {new_col_name}")

    df = st.session_state["database_filtered"]

    df_surveys_by_design = generate_survey_resume_by_design_df(df, original_col_name, new_col_name)

    encuestas_completadas = df_surveys_by_design["Completadas"].sum()

    st.write(f"Distribución por Diseño de las **{encuestas_completadas}** encuestas completadas:")
    st.dataframe(df_surveys_by_design, use_container_width=False)
    st.markdown("**Completadas:** Encuestas que cumplieron con el perfilamiento.")