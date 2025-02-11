import folium
import streamlit as st
from streamlit_folium import folium_static
import numpy as np

def create_vehicle_map(vehicles_df):
    m = folium.Map(location=[vehicles_df['lat'].mean(), vehicles_df['lon'].mean()], zoom_start=4)
    
    for _, vehicle in vehicles_df.iterrows():
        popup_html = f"""
            <div style='width: 200px'>
                <b>Vehicle ID:</b> {vehicle['vehicle_id'][:8]}<br>
                <b>Driver:</b> {vehicle['driver']}<br>
                <b>Status:</b> {vehicle['status']}<br>
                <b>Speed:</b> {vehicle['speed']} km/h<br>
                <b>Fuel:</b> {vehicle['fuel_level']}%
            </div>
        """
        
        icon_color = 'green' if vehicle['status'] == 'Active' else 'red' if vehicle['status'] == 'Maintenance' else 'orange'
        
        folium.Marker(
            [vehicle['lat'], vehicle['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)
    
    return m

def simulate_vehicle_movement(vehicles_df):
    vehicles_df['lat'] = vehicles_df['lat'] + np.random.uniform(-0.01, 0.01, size=len(vehicles_df))
    vehicles_df['lon'] = vehicles_df['lon'] + np.random.uniform(-0.01, 0.01, size=len(vehicles_df))
    return vehicles_df
