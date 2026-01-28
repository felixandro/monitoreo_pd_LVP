import streamlit as st

import src.statistics as stats

def success_sampling_rate_screen(original_col_name, new_col_name):    

    st.divider()

    st.subheader(f"Análisis por {new_col_name}")

    df = st.session_state["database"]

    if f"{new_col_name}_analisis_df" not in st.session_state:
        df_surveys_by_pc = stats.generate_surveys_by_pc_df(df, original_col_name, new_col_name)
        st.session_state[f"{new_col_name}_analisis_df"] = df_surveys_by_pc

    st.write(st.session_state[f"{new_col_name}_analisis_df"])

    st.markdown("**Completadas:** Encuestas que cumplieron con el perfilamiento.")
    st.markdown("**Total:** Encuestas Iniciadas.")
    st.markdown("**Tasa (%):** = (Completadas / Total) * 100")