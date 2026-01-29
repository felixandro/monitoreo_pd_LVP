import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#--------------------------------------------------
# Funciones Para Generar Resumenes de Tiempos de Respuesta
#--------------------------------------------------

def get_seconds_df(encuestador = "Todos"):

    df = st.session_state["database_filtered"]

    if encuestador == "Todos":
        df_filtered = df[df['surveyor_lat'].notna()]

    else:
        df_filtered = df[df['surveyor_lat'].notna() & (df['id_encuestador'] == encuestador)]

    seconds_cols = [f"s{i}_seconds" for i in range(2, 16)]

    df_filtered = df_filtered[seconds_cols]
    return df_filtered

def mean_response_times(df_seconds):
    output_df = pd.DataFrame()

    output_df["Promedio"] = df_seconds.mean().round(1)
    output_df["Mínimo"] = df_seconds.min().round(1)
    output_df["Q1"] = df_seconds.quantile(0.25).round(1)
    output_df["Mediana"] = df_seconds.median().round(1)
    output_df["Q3"] = df_seconds.quantile(0.75).round(1)
    output_df["Máximo"] = df_seconds.max().round(1)

    output_df["Pantalla"] = output_df.index.map(get_screen_names())
    output_df.set_index("Pantalla", inplace=True)

    return output_df

def get_screen_names():

    screen_names_dict = {
        "s2_seconds": "Caract Usuario",
        "s3_seconds": "Caract Viaje",
        "s4_seconds": "Ubi. Encuestador",
        "s5_seconds": "Niveles PR",
        "s6_seconds": "Intro PD",
        "s7_seconds": "PD 1",
        "s8_seconds": "PD 2",
        "s9_seconds": "PD 3",
        "s10_seconds": "PD 4",
        "s11_seconds": "PD 5",
        "s12_seconds": "PD 6",
        "s13_seconds": "PD 7",
        "s14_seconds": "PD 8",
        "s15_seconds": "Categ. Usuario",
    }

    return screen_names_dict

#--------------------------------------------------
# Elementos UI
#--------------------------------------------------

def surveyors_selectbox():

    st.divider()
    encuestadores_list = st.session_state["database_filtered"]["id_encuestador"].unique().tolist()
    encuestador_selected = st.selectbox("Seleccione un Encuestador", options =  encuestadores_list)
    return encuestador_selected

def responses_time_screen(encuestador = "Todos"):

    df_seconds = get_seconds_df(encuestador) # Datos

    st.divider()

    st.write(f"### Tiempos por Pantalla - Encuestador: {encuestador}")
    st.write( mean_response_times(df_seconds))


def mean_time_figure(encuestador):

    df_seconds_all = get_seconds_df()

    df_seconds_surveyor = get_seconds_df(encuestador)

    mean_all = mean_response_times(df_seconds_all)["Promedio"]
    mean_surveyor = mean_response_times(df_seconds_surveyor)["Promedio"]

    screen_labels = mean_all.index.tolist()
    # Separar índices: primeras 3 y última
    indices_fig1 = [0, 1, 2, 3, -1]
    labels_fig1 = [screen_labels[i] for i in indices_fig1]
    mean_all_fig1 = [mean_all.values[i] for i in indices_fig1]
    mean_surveyor_fig1 = [mean_surveyor.values[i] for i in indices_fig1]

    # Figura 1: Primeras 3 y última
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(labels_fig1, mean_all_fig1, alpha=0.7, label="Todos")
    ax1.plot(labels_fig1, mean_surveyor_fig1, marker='o', linewidth=3, markersize=8, label=f"Encuestador: {encuestador}", color='red')
    ax1.set_xlabel("Pantalla")
    ax1.set_ylabel("Tiempo (segundos)")
    ax1.set_title("Promedio de Tiempos de Respuesta - Pantallas Iniciales y Final")
    ax1.legend()
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)

    # Separar índices: intermedias (del 3 al 12)
    indices_fig2 = list(range(4, len(screen_labels) - 1))
    labels_fig2 = [screen_labels[i] for i in indices_fig2]
    mean_all_fig2 = [mean_all.values[i] for i in indices_fig2]
    mean_surveyor_fig2 = [mean_surveyor.values[i] for i in indices_fig2]

    # Figura 2: Pantallas intermedias
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.bar(labels_fig2, mean_all_fig2, alpha=0.7, label="Todos")
    ax2.plot(labels_fig2, mean_surveyor_fig2, marker='o', linewidth=3, markersize=8, label=f"Encuestador: {encuestador}", color='red')
    ax2.set_xlabel("Pantalla")
    ax2.set_ylabel("Tiempo (segundos)")
    ax2.set_title("Promedio de Tiempos de Respuesta - Experimentos PD")
    ax2.legend()
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)

def pd_multiselect():
    st.divider()
    pd_options = [f"PD {i}" for i in range(1, 9)]
    selected_pds = st.multiselect("Seleccione las Pantallas PD", options=pd_options)
    return selected_pds

def evolucion_time_figure(encuestador, pd_columns):

    st.write("## Evolución Tiempos PD")

    df_seconds_surveyor = get_seconds_df(encuestador)
    df_seconds_surveyor.rename(columns=get_screen_names(), inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    for col in pd_columns:
        ax.plot(df_seconds_surveyor[col].values, marker='o', label=col, linewidth=2)
    
    ax.set_xlabel("Número de Respuesta")
    ax.set_ylabel("Tiempo (segundos)")
    ax.set_title(f"Evolución de Tiempos - Encuestador: {encuestador}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

