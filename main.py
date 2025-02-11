import streamlit as st
from streamlit_folium import folium_static
from utils.data_generator import (
    generate_vehicle_data,
    generate_telematics_data,
    generate_iot_data,
    generate_logistics_data,
    generate_construction_data
)
from utils.map_utils import create_vehicle_map, simulate_vehicle_movement
from components.fleet_management import render_fleet_management
from components.insurance_telematics import render_insurance_telematics
from components.connected_cars import render_connected_cars
from components.logistics import render_logistics
from components.construction import render_construction
import time

st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for vehicle icons
st.markdown("""
    <style>
    .vehicle-icon {
        font-size: 24px;
        text-align: center;
        transition: all 0.5s ease;
    }
    .vehicle-icon.green { color: #00ff00; }
    .vehicle-icon.red { color: #ff0000; }
    .vehicle-icon.orange { color: #ffa500; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vehicles_df' not in st.session_state:
    st.session_state.vehicles_df = generate_vehicle_data()
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'update_counter' not in st.session_state:
    st.session_state.update_counter = 0

# Update vehicle positions every 2 seconds
current_time = time.time()
if current_time - st.session_state.last_update > 2:
    st.session_state.vehicles_df = simulate_vehicle_movement(st.session_state.vehicles_df)
    st.session_state.last_update = current_time
    st.session_state.update_counter += 1

# Main title
st.title("🚛 Fleet Management System")

# Create tabs
tabs = st.tabs([
    "Fleet Management",
    "Insurance Telematics",
    "Connected Cars & IoT",
    "Logistics & Supply Chain",
    "Construction & Heavy Equipment"
])

# Fleet Management Tab
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        # Display the map
        st.subheader("Live Vehicle Tracking")
        map_figure = create_vehicle_map(st.session_state.vehicles_df)
        folium_static(map_figure, height=400)

        # Add update counter
        st.caption(f"Last updated: {st.session_state.update_counter} times")

    with col2:
        st.subheader("Quick Stats")
        active_vehicles = len(st.session_state.vehicles_df[st.session_state.vehicles_df['status'] == 'Active'])
        st.metric("Active Vehicles", active_vehicles)
        total_distance = sum(st.session_state.vehicles_df['speed']) * 2 / 1000  # Rough estimate
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

# Construction & Heavy Equipment Tab
with tabs[4]:
    construction_data = generate_construction_data()
    render_construction(construction_data)

# Add footer
st.markdown("---")
st.markdown("Fleet Management System - Real-time monitoring and analytics")