import streamlit as st
from streamlit_folium import folium_static
from utils.data_generator import (
    generate_vehicle_data,
    generate_telematics_data,
    generate_iot_data,
    generate_logistics_data
)
from utils.map_utils import create_vehicle_map, simulate_vehicle_movement
from components.fleet_management import render_fleet_management
from components.insurance_telematics import render_insurance_telematics
from components.connected_cars import render_connected_cars
from components.logistics import render_logistics
import time

st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for vehicle icons with animation
st.markdown("""
    <style>
    .vehicle-icon {
        font-size: 36px !important;  /* Increased size significantly */
        text-align: center;
        transition: all 0.2s ease;  /* Faster transition */
        transform-origin: center;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50px !important;  /* Explicit width */
        height: 50px !important;  /* Explicit height */
    }
    .vehicle-icon.green { color: #00ff00; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .vehicle-icon.red { color: #ff0000; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .vehicle-icon.orange { color: #ffa500; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vehicles_df' not in st.session_state:
    st.session_state.vehicles_df = generate_vehicle_data(n_vehicles=20)
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'update_counter' not in st.session_state:
    st.session_state.update_counter = 0
if 'speed_multiplier' not in st.session_state:
    st.session_state.speed_multiplier = 1.0

# Sidebar controls
st.sidebar.title("Map Controls")
speed_multiplier = st.sidebar.slider(
    "Vehicle Movement Speed",
    min_value=0.1,
    max_value=5.0,
    value=st.session_state.speed_multiplier,
    step=0.1,
    help="Adjust the speed of vehicle movement on the map"
)
st.session_state.speed_multiplier = speed_multiplier

# Update vehicle positions every 0.2 seconds (increased frequency)
current_time = time.time()
if current_time - st.session_state.last_update > 0.2:  # Even faster updates
    st.session_state.vehicles_df = simulate_vehicle_movement(
        st.session_state.vehicles_df,
        speed_multiplier=st.session_state.speed_multiplier
    )
    st.session_state.last_update = current_time
    st.session_state.update_counter += 1

# Main title
st.title("🚛 Fleet Management System")

# Create tabs
tabs = st.tabs([
    "Fleet Management",
    "Insurance Telematics",
    "Connected Cars & IoT",
    "Logistics & Supply Chain"
])

# Fleet Management Tab
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        # Display the map
        st.subheader("Live Vehicle Tracking")
        map_figure = create_vehicle_map(st.session_state.vehicles_df)
        folium_static(map_figure, height=500)  # Increased map height

        # Add update counter and current speed
        st.caption(f"Map updates: {st.session_state.update_counter} | Speed multiplier: {st.session_state.speed_multiplier}x")

    with col2:
        st.subheader("Quick Stats")
        active_vehicles = len(st.session_state.vehicles_df[st.session_state.vehicles_df['status'] == 'Active'])
        st.metric("Active Vehicles", active_vehicles)
        total_distance = sum(st.session_state.vehicles_df['speed'].astype(float)) * 0.2 / 1000  # Adjusted for new update frequency
        st.metric("Total Distance Today", f"{total_distance:.2f} km")

    render_fleet_management(st.session_state.vehicles_df)

# Insurance Telematics Tab
with tabs[1]:
    telematics_data = generate_telematics_data()
    render_insurance_telematics(telematics_data)

# Connected Cars & IoT Tab
with tabs[2]:
    iot_data = generate_iot_data()
    render_connected_cars(iot_data)

# Logistics & Supply Chain Tab
with tabs[3]:
    logistics_data = generate_logistics_data()
    render_logistics(logistics_data)

# Add footer
st.markdown("---")
st.markdown("Fleet Management System - Real-time monitoring and analytics")