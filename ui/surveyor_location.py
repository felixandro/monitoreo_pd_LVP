import geopandas as gpd
from shapely.geometry import Point
import folium
import streamlit_folium as st_folium
import streamlit as st

def filter_df(df):

    df_filtered = df[df['surveyor_lat'].notna()]
    df_filtered = df_filtered[["id", "id_encuestador", "pc", "surveyor_lat", "surveyor_lon"]]
    return df_filtered

def generate_gdf_surveyor_locations(df):

    df_filtered = filter_df(df)

    geometry = [Point(xy) for xy in zip(df_filtered['surveyor_lon'], df_filtered['surveyor_lat'])]
    gdf = gpd.GeoDataFrame(df_filtered, geometry=geometry, crs="EPSG:4326")

    return gdf

def deploy_map():

    df = st.session_state["database"]

    gdf = generate_gdf_surveyor_locations(df)

    # Crear el mapa centrado en un punto específico
    m = folium.Map(location=[-39.30141119085401, -72.35149688469174], zoom_start=10)  # Coordenadas de Lima, Perú

    # Agregar los puntos al mapa
    for idx, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row['surveyor_lat'], row['surveyor_lon']],
            radius=6,
            popup=f"ID Encuestador: {row['id_encuestador']}<br>PC: {row['pc']}",
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.7
        ).add_to(m)

    # Mostrar el mapa en Streamlit
    st_folium.st_folium(m, width=700, height=500, returned_objects=[])

def surveyor_location_screen():

    st.divider()
    
    st.header("Ubicación de los Encuestadores")

    deploy_map()