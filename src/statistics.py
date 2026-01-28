import streamlit as st
import pandas as pd

def generate_surveys_by_pc_df(df, original_col_name, new_col_name):

    df_aux = pd.DataFrame()
    df_aux[new_col_name] = df[original_col_name].copy()
    df_aux["Completadas"] = df["surveyor_lat"].notna().astype(int)
    df_aux["Total"] = 1
    
    df_surveys_by_pc = df_aux.groupby(new_col_name).sum().reset_index()
    df_surveys_by_pc["%"] = (df_surveys_by_pc["Completadas"] / df_surveys_by_pc["Total"].replace(0, 1) * 100).round()

    # Agregar fila de totales

    # Calcular totales
    total_completadas = df_surveys_by_pc["Completadas"].sum()
    total_total = df_surveys_by_pc["Total"].sum()
    total_porcentaje = round((total_completadas / total_total) * 100) if total_total != 0 else 0

    # Crear fila de totales
    fila_totales = pd.DataFrame({
        new_col_name: ["TOTAL"],
        "Completadas": [total_completadas],
        "Total": [total_total],
        "%": [total_porcentaje]
    })

    # Agregar fila de totales al DataFrame
    df_surveys_by_pc = pd.concat([df_surveys_by_pc, fila_totales], ignore_index=True)
    return df_surveys_by_pc
    
