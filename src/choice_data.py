import pandas as pd
from adjustText import adjust_text  
import matplotlib.pyplot as plt
import streamlit as st
import random

def format_database(df):

    rows_list = []

    for index, row in df.iterrows():
        row_copy = row.to_dict()

        row_copy.pop("surveyor_lat", None)
        row_copy.pop("surveyor_lon", None)
        row_copy.pop("surveyor_acc", None)

        for i in range(2, 16):
            row_copy.pop(f"s{i}_seconds", None)

        for i in range(1, 9):
            row_copy.pop(f"tj{i}", None)
            row_copy.pop(f"choice_tj_{i}", None)
            row_copy.pop(f"choice_tj_{i}_label", None)


        for i in range(1, 9):
            new_row = row_copy.copy()
            new_row["dis"] = row[f"tj{i}_dis"]
            new_row["tj"] = i
            new_row["choice"] = row[f"choice_tj_{i}"]
            new_row["choice_label"] = row[f"choice_tj_{i}_label"]
            new_row["alt1"] = row[f"tj{i}_label1"]
            new_row["tv1"] = row[f"tj{i}_tv1"]
            new_row["c1"] = row[f"tj{i}_c1"]
            new_row["f1"] = row[f"tj{i}_f1"]
            new_row["ta1"] = row[f"tj{i}_ta1"]
            new_row["alt2"] = row[f"tj{i}_label2"]
            new_row["tv2"] = row[f"tj{i}_tv2"]
            new_row["c2"] = row[f"tj{i}_c2"]
            new_row["f2"] = row[f"tj{i}_f2"]
            new_row["ta2"] = row[f"tj{i}_ta2"]

            rows_list.append(new_row)

    df_formatted = pd.DataFrame(rows_list)

    df_formatted = add_diferences(df_formatted)

    return df_formatted

def add_diferences(df):

    output_df = df.copy()

    output_df["delta_tv"] = output_df["tv2"] - output_df["tv1"]
    output_df["delta_c"] = output_df["c2"] - output_df["c1"]
    output_df["delta_ta"] = output_df["ta2"] - output_df["ta1"]
    output_df["delta_f"] = output_df["f2"].str.extract('(\d+)').astype(int)

    return output_df

def process_choice_data(df):

    df_aux = df.groupby(['dis', 'tj', 'delta_tv', 'delta_c', 'delta_ta', 'delta_f', 'choice_label']).size().reset_index(name='count')
    
    pivot_df = df_aux.pivot_table(index=['dis', 'tj', 'delta_tv', 'delta_c', 'delta_ta', 'delta_f'], columns='choice_label', values='count', fill_value=0)

    pivot_df = pivot_df.reset_index()
    
    if "Auto" not in pivot_df.columns:
        pivot_df["Auto"] = 0
    
    if "Bus" not in pivot_df.columns:
        pivot_df["Bus"] = 0

    pivot_df = add_total_column(pivot_df)
    pivot_df = add_proportion_columns(pivot_df)

    output_df = pivot_df[["dis", "tj", "delta_tv", "delta_c", "delta_ta", "delta_f", "Auto", "Bus", "Tren", "Total", "% Auto", "% Bus", "% Tren"]]

    return output_df

def add_total_column(df):
    output_df = df.copy()
    output_df["Total"] = output_df["Auto"] + output_df["Bus"] + output_df["Tren"]
    return output_df

def add_proportion_columns(df):
    output_df = df.copy()
    output_df["% Auto"] = (output_df["Auto"] / output_df["Total"]) * 100
    output_df["% Bus"] = (output_df["Bus"] / output_df["Total"]) * 100
    output_df["% Tren"] = (output_df["Tren"] / output_df["Total"]) * 100
    return output_df

def generate_quantity_df(df, dis):

    quantity_df = df[df["dis"] == dis].copy()
    quantity_df = quantity_df[["tj", "Auto", "Bus", "Tren", "Total"]].set_index("tj")

    dummy_auto = quantity_df["Auto"].sum()
    if dummy_auto == 0:
        quantity_df.drop("Auto", axis=1, inplace=True)
    else:
        quantity_df.drop("Bus", axis=1, inplace=True)
    
    return quantity_df

def generate_proportions_df(df):

    output_df = pd.DataFrame()

    for col in df.columns:
        output_df[f"% {col}"] = (df[col] / df["Total"]) * 100
    
    return output_df


def generate_grafico_barras_prop_tren(df_proporciones):

    df_proporciones = df_proporciones[["% Tren"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    df_proporciones.plot(kind='bar', ax=ax)
    ax.set_title('% Elección Tren')
    ax.set_xlabel('Tarjeta')
    ax.set_ylabel('Porcentaje (%)')
    ax.set_ylim(0, 100)
    ax.legend(title='Modo')
    fig.tight_layout()
    
    return fig

def get_label_grafico_dispersion(col):
    labels_dict = {
        "delta_tv": "Delta Tiempo Viaje (Tren - Modo Actual) (minutos)",
        "delta_c": "Delta Costo (Tren - Modo Actual) (pesos)",
        "delta_ta": "Delta Tiempo Acceso/Egreso (Tren - Modo Actual) (minutos)",
        "delta_f": "Frecuencia Tren (Salidas Diarias)"
    }
    return labels_dict[col]

def generate_filter(df, ref_dict):
        
    filtro = pd.Series([True] * len(df), index=df.index)
    for key, value in ref_dict.items():
        if value == "All":
            continue
        else:
            filtro &= (df[key] == int(value))
    
    return filtro

def generate_grafico_dispersion(df, ref_dict, col1, col2):
        
        filtro = generate_filter(df, ref_dict)
        df_filtered = df[filtro]

        fig, ax = plt.subplots(figsize=(10, 6))
        sizes = df_filtered["% Tren"] * 40  # Ajusta el factor de multiplicación según sea necesario
        ax.scatter(df_filtered[col1], df_filtered[col2], s=sizes, alpha=0.6)
        ax.scatter(df_filtered[col1], df_filtered[col2], alpha=0.6)
        ax.set_xlabel(get_label_grafico_dispersion(col1))
        ax.set_ylabel(get_label_grafico_dispersion(col2))
        ax.set_xlim(min(df_filtered[col1].min()*1.1,0), max(0,df_filtered[col1].max()*1.5))
        ax.set_ylim(min(df_filtered[col2].min()*1.1,0), max(0,df_filtered[col2].max()*1.1))

        texts = []
        for idx, row in df_filtered.iterrows():
            texts.append(ax.annotate(f"T{int(row['tj'])} ({int(row['% Tren'])})%", (row[col1], row[col2]), fontsize=10, alpha=0.7))

        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red', lw=1.5), force_text=(0.8, 0.8))

        ax.set_title(f'Dispersión: {col1} vs {col2}')

        fig.tight_layout()

        ax.legend(['% Elección Tren'], loc='best')
        return fig

def generate_delta_selectbox(df, level_name, n_levels, key_suffix):

    if n_levels > 1:        
        level_ref = st.selectbox(
            f"Nivel {level_name}",
            options=["All"] + df[level_name].unique().tolist(),
            key=f"selectbox_{level_name}_{key_suffix}"
        )
        return level_ref
    else:
        return "All"