import pandas as pd
from supabase import create_client, Client
import streamlit as st
from datetime import datetime, date, timedelta

def generate_date_range():
    start_local_time = pd.to_datetime("09:00:00").time()
    end_local_time = pd.to_datetime("20:00:00").time()

    start_date = date(2026, 1, 28)
    end_date = date(2026, 1,28)

    #start_datetime = (datetime.combine(start_date, start_local_time) + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S%z")
    #end_datetime = (datetime.combine(end_date, end_local_time) + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S%z")

    start_datetime = datetime.combine(start_date, start_local_time) 
    end_datetime = datetime.combine(end_date, end_local_time) 

    return start_datetime, end_datetime


def cargar_bbdd(table_name):

    start_date, end_date = generate_date_range()

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

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_filtered = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)] 
    return df_filtered