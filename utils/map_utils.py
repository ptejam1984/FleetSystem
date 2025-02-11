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

    # UK mainland boundary coordinates (more precise)
    uk_bounds = {
        'lat_min': 50.10319,  # Southern England
        'lat_max': 58.44377,  # Northern Scotland
        'lon_min': -5.5,      # Adjusted for mainland
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
            [float(vehicle['lat']), float(vehicle['lon'])],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.DivIcon(
                html=f'<div class="vehicle-icon {icon_color}">🚛</div>',
                icon_size=(50, 50),
                icon_anchor=(25, 25),
                popup_anchor=(0, -25),
                class_name=f'vehicle-icon {icon_color}'
            )
        ).add_to(m)

    return m

def simulate_vehicle_movement(vehicles_df, speed_multiplier=1.0):
    # UK mainland boundary coordinates (more precise)
    uk_bounds = {
        'lat_min': 50.10319,  # Southern England
        'lat_max': 58.44377,  # Northern Scotland
        'lon_min': -5.5,      # Adjusted for mainland
        'lon_max': 1.75159    # Eastern England
    }

    # Major UK cities for reference points
    uk_cities = [
        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
        {'name': 'Manchester', 'lat': 53.4808, 'lon': -2.2426},
        {'name': 'Birmingham', 'lat': 52.4862, 'lon': -1.8904},
        {'name': 'Leeds', 'lat': 53.8008, 'lon': -1.5491},
        {'name': 'Glasgow', 'lat': 55.8642, 'lon': -4.2518},
        {'name': 'Liverpool', 'lat': 53.4084, 'lon': -2.9916}
    ]

    # Update vehicle positions based on their speed and direction
    for idx in vehicles_df.index:
        if vehicles_df.loc[idx, 'status'] == 'Active':
            # Convert to float explicitly
            speed = float(vehicles_df.loc[idx, 'speed'])
            # Increased base movement speed and apply multiplier
            speed_factor = (speed / 25.0) * speed_multiplier * 0.1  # More significant movement

            lat = float(vehicles_df.loc[idx, 'lat'])
            lon = float(vehicles_df.loc[idx, 'lon'])
            direction_rad = radians(float(vehicles_df.loc[idx, 'direction']))

            # Calculate new position with larger movement
            new_lat = lat + speed_factor * cos(direction_rad)
            new_lon = lon + speed_factor * sin(direction_rad)

            # Check if new position would be outside mainland UK
            if (new_lat < uk_bounds['lat_min'] or new_lat > uk_bounds['lat_max'] or 
                new_lon < uk_bounds['lon_min'] or new_lon > uk_bounds['lon_max']):
                # Find nearest city
                nearest_city = min(uk_cities, 
                    key=lambda c: abs(c['lat'] - lat) + abs(c['lon'] - lon))

                # Update current city
                vehicles_df.at[idx, 'current_city'] = nearest_city['name']

                # Calculate direction to nearest city
                delta_lon = nearest_city['lon'] - lon
                delta_lat = nearest_city['lat'] - lat
                new_direction = np.degrees(np.arctan2(delta_lon, delta_lat))
                vehicles_df.at[idx, 'direction'] = new_direction
            else:
                vehicles_df.at[idx, 'lat'] = new_lat
                vehicles_df.at[idx, 'lon'] = new_lon

            # Update speed randomly within reasonable bounds
            new_speed = speed + np.random.uniform(-5, 5)
            vehicles_df.at[idx, 'speed'] = np.clip(new_speed, 40, 120)

    return vehicles_df