import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_fleet_management(vehicles_df):
    st.header("Fleet Management Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Vehicles", len(vehicles_df))
    with col2:
        active_vehicles = len(vehicles_df[vehicles_df['status'] == 'Active'])
        st.metric("Active Vehicles", active_vehicles)
    with col3:
        avg_fuel = round(vehicles_df['fuel_level'].mean(), 2)
        st.metric("Average Fuel Level", f"{avg_fuel}%")
    with col4:
        avg_speed = round(vehicles_df['speed'].mean(), 2)
        st.metric("Average Speed", f"{avg_speed} km/h")

    # Vehicle status distribution
    st.subheader("Vehicle Status Distribution")
    status_counts = vehicles_df['status'].value_counts()
    fig = px.pie(values=status_counts.values, names=status_counts.index, 
                 title="Vehicle Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Vehicle model distribution
    st.subheader("Fleet Composition")
    model_counts = vehicles_df['model'].value_counts()
    fig = px.bar(x=model_counts.index, y=model_counts.values,
                 title="Vehicle Models in Fleet")
    st.plotly_chart(fig, use_container_width=True)

    # Vehicle list
    st.subheader("Vehicle List")
    st.dataframe(vehicles_df[['vehicle_id', 'model', 'driver', 'status', 'fuel_level', 'speed']])
