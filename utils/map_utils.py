import folium
import streamlit as st
from streamlit_folium import folium_static
import numpy as np
from math import sin, cos, radians

def create_vehicle_map(vehicles_df):
    # Create a map centered on UK
    uk_center = [54.2361, -4.5481]  # Center of UK
    m = folium.Map(location=uk_center,
                  zoom_start=6,
                  tiles='OpenStreetMap')

    # UK boundary coordinates for keeping vehicles in bounds
    uk_bounds = {
        'lat_min': 50.10319,  # Southern England
        'lat_max': 58.44377,  # Northern Scotland
        'lon_min': -7.64133,  # Western Ireland
        'lon_max': 1.75159    # Eastern England
    }

    # Add vehicles to the map
    for _, vehicle in vehicles_df.iterrows():
        # Create popup content
        popup_html = f"""
            <div style='width: 200px'>
                <b>Vehicle ID:</b> {vehicle['vehicle_id'][:8]}<br>
                <b>Driver:</b> {vehicle['driver']}<br>
                <b>Status:</b> {vehicle['status']}<br>
                <b>Speed:</b> {vehicle['speed']} km/h<br>
                <b>Fuel:</b> {vehicle['fuel_level']}%<br>
                <b>Near:</b> {vehicle['current_city']}
            </div>
        """

        # Set icon color based on status
        icon_color = 'green' if vehicle['status'] == 'Active' else 'red' if vehicle['status'] == 'Maintenance' else 'orange'

        # Add custom icon marker
        folium.Marker(
            [float(vehicle['lat']), float(vehicle['lon'])],  # Convert to float explicitly
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.DivIcon(
                html=f'<div class="vehicle-icon {icon_color}">🚛</div>',
                icon_size=(30, 30),
                icon_anchor=(15, 15),
                popup_anchor=(0, -15),
                class_name=f'vehicle-icon {icon_color}'
            )
        ).add_to(m)

    return m

def simulate_vehicle_movement(vehicles_df):
    # UK boundary coordinates
    uk_bounds = {
        'lat_min': 50.10319,
        'lat_max': 58.44377,
        'lon_min': -7.64133,
        'lon_max': 1.75159
    }

    # Update vehicle positions based on their speed and direction
    for idx in vehicles_df.index:
        if vehicles_df.loc[idx, 'status'] == 'Active':
            # Convert to float explicitly
            speed = float(vehicles_df.loc[idx, 'speed'])
            speed_factor = speed / 100  # Increased speed factor (was 1000)
            direction_rad = radians(float(vehicles_df.loc[idx, 'direction']))

            # Calculate new position
            lat = float(vehicles_df.loc[idx, 'lat'])
            lon = float(vehicles_df.loc[idx, 'lon'])

            new_lat = lat + speed_factor * cos(direction_rad)
            new_lon = lon + speed_factor * sin(direction_rad)

            # Keep vehicles within UK bounds
            if (new_lat < uk_bounds['lat_min'] or new_lat > uk_bounds['lat_max'] or 
                new_lon < uk_bounds['lon_min'] or new_lon > uk_bounds['lon_max']):
                # If vehicle would go out of bounds, reverse direction
                vehicles_df.at[idx, 'direction'] = (float(vehicles_df.loc[idx, 'direction']) + 180) % 360
            else:
                vehicles_df.at[idx, 'lat'] = new_lat
                vehicles_df.at[idx, 'lon'] = new_lon

            # Randomly change direction occasionally
            if np.random.random() < 0.1:  # Reduced chance to change direction
                new_direction = float(vehicles_df.loc[idx, 'direction']) + np.random.uniform(-30, 30)
                vehicles_df.at[idx, 'direction'] = new_direction % 360

            # Update speed randomly
            new_speed = speed + np.random.uniform(-5, 5)
            vehicles_df.at[idx, 'speed'] = np.clip(new_speed, 40, 120)  # Increased minimum speed

    return vehicles_df