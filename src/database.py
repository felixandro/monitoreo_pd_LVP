import pandas as pd
from supabase import create_client, Client
import streamlit as st
from datetime import datetime, date, timedelta


def cargar_bbdd(table_name):

    # Configura tus credenciales de Supabase
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    
    # Crea el cliente
    supabase: Client = create_client(url, key)

    all_data = []
    page_size = 1000
    offset = 0

    while True:
        response = (
            supabase.table(table_name)
            .select('*')
            #.gte("hora_id", start_date)
            #.lte("hora_id", end_date)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        #print(response)
        batch = response.data
        if not batch:
            break
        all_data.extend(batch)
        offset += page_size

        df = pd.DataFrame(all_data)
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df["VAL_TPD_MIN"] = 0
    df["VAL_TPD_PRO"] = 0
    df["VAL_CHOICE"] = 0
    df["VAL"] = 0
    df["VAL2"] = 0

    return df

def filtrar_database():
    df = st.session_state["database"].copy()
    start_date = pd.to_datetime(st.session_state["start_date"]) 
    end_date = pd.to_datetime(st.session_state["end_date"]) 

    # Ensure comparable, timezone-naive datetimes
    if hasattr(df["datetime"].dt, "tz") and df["datetime"].dt.tz is not None:
        df["datetime"] = df["datetime"].dt.tz_localize(None)
    if getattr(start_date, "tzinfo", None) is not None:
        start_date = start_date.tz_localize(None)
    if getattr(end_date, "tzinfo", None) is not None:
        end_date = end_date.tz_localize(None)

    df_filtered = df[(df["datetime"] >= start_date) & (df["datetime"] <= end_date)]
    df_filtered.sort_values(by='datetime', inplace=True)
    df_filtered.reset_index(drop=True, inplace=True)

    st.session_state["database_filtered"] = df_filtered

def agregar_val_col_tpd_min():
    
    df = st.session_state["database_filtered"].copy()
    tpd_min = st.session_state["tpd_min"]

    df["VAL_TPD_MIN"] = 0

    for i in range(7, 15):
        df["VAL_TPD_MIN"] += (df[f"s{i}_seconds"] >= tpd_min).astype(int)

    df["VAL_TPD_MIN"] = (df["VAL_TPD_MIN"] == 8).astype(int)

    st.session_state["database_filtered"] = df

def agregar_val_col_tpd_pro():
    
    df = st.session_state["database_filtered"].copy()
    tpd_pro = st.session_state["tpd_pro"]

    df["VAL_TPD_PRO"] = 0

    for i in range(7, 15):
        df["VAL_TPD_PRO"] += df[f"s{i}_seconds"]

    df["VAL_TPD_PRO"] = (df["VAL_TPD_PRO"] >= 8 * tpd_pro).astype(int)

    st.session_state["database_filtered"] = df

def agregar_val_col_choice():
    
    df = st.session_state["database_filtered"].copy()

    df["VAL_CHOICE"] = 0

    for i in range(1, 9):
        df["VAL_CHOICE"] += df[f"choice_tj_{i}"].fillna(0).astype(int)

    df["VAL_CHOICE"] = ((df["VAL_CHOICE"] > 8) & (df["VAL_CHOICE"] < 16)).astype(int)

    st.session_state["database_filtered"] = df

def agregar_val_col():
    
    df = st.session_state["database_filtered"].copy()

    df["VAL"] = df["VAL_TPD_MIN"] * df["VAL_TPD_PRO"] * df["VAL_CHOICE"]

    st.session_state["database_filtered"] = df

def agregar_val2_col():
    
    df = st.session_state["database_filtered"].copy()

    df["VAL2"] = df["VAL_TPD_MIN"] + df["VAL_TPD_PRO"] + df["VAL_CHOICE"]
    df["VAL2"] = (df["VAL2"] >= 2).astype(int)

    st.session_state["database_filtered"] = df

    