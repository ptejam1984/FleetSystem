import folium
import streamlit as st
from streamlit_folium import folium_static
import numpy as np
from math import sin, cos, radians

def create_vehicle_map(vehicles_df):
    # Create a map centered on the mean position of vehicles
    m = folium.Map(location=[vehicles_df['lat'].mean(), vehicles_df['lon'].mean()], 
                  zoom_start=4,
                  tiles='OpenStreetMap')

    # Add vehicles to the map
    for _, vehicle in vehicles_df.iterrows():
        # Create a custom icon with rotation based on direction
        icon_html = f'''
            <div style="transform: rotate({vehicle['direction']}deg);">
                🚛
            </div>
        '''

        # Create popup content
        popup_html = f"""
            <div style='width: 200px'>
                <b>Vehicle ID:</b> {vehicle['vehicle_id'][:8]}<br>
                <b>Driver:</b> {vehicle['driver']}<br>
                <b>Status:</b> {vehicle['status']}<br>
                <b>Speed:</b> {vehicle['speed']} km/h<br>
                <b>Fuel:</b> {vehicle['fuel_level']}%
            </div>
        """

        # Set icon color based on status
        icon_color = 'green' if vehicle['status'] == 'Active' else 'red' if vehicle['status'] == 'Maintenance' else 'orange'

        # Add custom icon marker
        folium.Marker(
            [vehicle['lat'], vehicle['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.DivIcon(
                html=icon_html,
                icon_size=(30, 30),
                icon_anchor=(15, 15),
                popup_anchor=(0, -15),
                class_name=f'vehicle-icon {icon_color}'
            )
        ).add_to(m)

    return m

def simulate_vehicle_movement(vehicles_df):
    # Update vehicle positions based on their speed and direction
    for idx in vehicles_df.index:
        if vehicles_df.loc[idx, 'status'] == 'Active':
            speed_factor = vehicles_df.loc[idx, 'speed'] / 1000  # Convert speed to coordinate changes
            direction_rad = radians(vehicles_df.loc[idx, 'direction'])

            # Calculate new position
            vehicles_df.loc[idx, 'lat'] += speed_factor * cos(direction_rad)
            vehicles_df.loc[idx, 'lon'] += speed_factor * sin(direction_rad)

            # Randomly change direction occasionally
            if np.random.random() < 0.2:  # 20% chance to change direction
                vehicles_df.loc[idx, 'direction'] += np.random.uniform(-20, 20)
                vehicles_df.loc[idx, 'direction'] %= 360  # Keep direction between 0 and 360

            # Update speed randomly
            vehicles_df.loc[idx, 'speed'] += np.random.uniform(-5, 5)
            vehicles_df.loc[idx, 'speed'] = np.clip(vehicles_df.loc[idx, 'speed'], 0, 120)

    return vehicles_df