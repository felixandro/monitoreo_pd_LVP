import streamlit as st
import src.choice_data as cd

st.write("# Análisis Elecciones por Tarjeta")

nro_dis = st.number_input(
    "Ingrese el número de diseño",
    min_value=1,
    max_value=16,
    value=1,
    step=1
)

#st.write(st.session_state["formatted_database"])

resume_choice_data_df = cd.process_choice_data(st.session_state["formatted_database"])
#st.write(resume_choice_data_df)

elecciones_df = cd.generate_quantity_df(resume_choice_data_df, nro_dis)
proporciones_df = cd.generate_proportions_df(elecciones_df)
grafico_barra_proporciones = cd.generate_grafico_barras_prop_tren(proporciones_df)

st.write(f"## Encuestas Válidas: {int(elecciones_df['Total'].sum()/8)}")

st.pyplot(grafico_barra_proporciones)

st.subheader(f"Elecciones por Tarjeta")
st.write(elecciones_df)

st.subheader(f"Proporciones por Tarjeta")
st.write(proporciones_df)


st.write("## Dispersión de Diferencias y % Elección Tren")

resume_choice_data_DIS = resume_choice_data_df[resume_choice_data_df["dis"] == nro_dis]
n_levels_tv = resume_choice_data_DIS["delta_tv"].nunique()
n_levels_c = resume_choice_data_DIS["delta_c"].nunique()
n_levels_ta = resume_choice_data_DIS["delta_ta"].nunique()
n_levels_f = resume_choice_data_DIS["delta_f"].nunique()

#st.write(resume_choice_data_DIS)

if n_levels_tv > 1 and n_levels_c > 1:

    st.write(f"### T.Viaje vs Costo")

    delta_ta_ref = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_ta", n_levels_ta, 1)
    delta_f_ref = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_f", n_levels_f, 1)

    grafico_dispersion_tv_c = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_ta":delta_ta_ref, "delta_f":delta_f_ref} ,
                                                            "delta_tv", 
                                                            "delta_c")
    
    st.pyplot(grafico_dispersion_tv_c)

if n_levels_tv > 1 and n_levels_ta > 1:

    st.write(f"### T.Viaje vs T.Acceso/Egreso")

    delta_c_ref = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_c", n_levels_c, 1)
    delta_f_ref_2 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_f", n_levels_f, 2)

    grafico_dispersion_tv_ta = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_c":delta_c_ref, "delta_f":delta_f_ref_2} ,
                                                            "delta_tv", 
                                                            "delta_ta")
    
if n_levels_tv > 1 and n_levels_f > 1:

    st.write(f"### T.Viaje vs Frecuencia")

    delta_c_ref_2 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_c", n_levels_c, 2)
    delta_ta_ref_2 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_ta", n_levels_ta, 2)

    grafico_dispersion_tv_f = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_c":delta_c_ref_2, "delta_ta":delta_ta_ref_2} ,
                                                            "delta_tv", 
                                                            "delta_f")
    
    st.pyplot(grafico_dispersion_tv_f)

if n_levels_c > 1 and n_levels_ta > 1:

    st.write(f"### Costo vs T.Acceso/Egreso")

    delta_tv_ref = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_tv", n_levels_tv, 1)
    delta_f_ref_3 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_f", n_levels_f, 3)

    grafico_dispersion_c_ta = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_tv":delta_tv_ref, "delta_f":delta_f_ref_3} ,
                                                            "delta_c", 
                                                            "delta_ta")
    
    st.pyplot(grafico_dispersion_c_ta)

if n_levels_c > 1 and n_levels_f > 1:

    st.write(f"### Costo vs Frecuencia")

    delta_tv_ref_2 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_tv", n_levels_tv, 2)
    delta_ta_ref_3 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_ta", n_levels_ta, 3)

    grafico_dispersion_c_f = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_tv":delta_tv_ref_2, "delta_ta":delta_ta_ref_3} ,
                                                            "delta_c", 
                                                            "delta_f")
    
    st.pyplot(grafico_dispersion_c_f)

if n_levels_ta > 1 and n_levels_f > 1:

    st.write(f"### T.Acceso/Egreso vs Frecuencia")

    delta_tv_ref_3 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_tv", n_levels_tv, 3)
    delta_c_ref_3 = cd.generate_delta_selectbox(resume_choice_data_DIS, "delta_c", n_levels_c, 3)

    grafico_dispersion_ta_f = cd.generate_grafico_dispersion(resume_choice_data_DIS, 
                                                            {"delta_tv":delta_tv_ref_3, "delta_c":delta_c_ref_3} ,
                                                            "delta_ta", 
                                                            "delta_f")
    
    st.pyplot(grafico_dispersion_ta_f)
