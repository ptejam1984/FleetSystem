import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_connected_cars(iot_df):
    st.header("Connected Cars & IoT Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Connected Devices", len(iot_df))
    with col2:
        avg_temp = round(iot_df['temperature'].mean(), 2)
        st.metric("Average Temperature", f"{avg_temp}°F")
    with col3:
        avg_battery = round(iot_df['battery_level'].mean(), 2)
        st.metric("Average Battery Level", f"{avg_battery}%")

    # Engine health distribution
    st.subheader("Engine Health Distribution")
    health_counts = iot_df['engine_health'].value_counts()
    fig = px.pie(values=health_counts.values, names=health_counts.index,
                 title="Engine Health Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Temperature vs Battery Level
    st.subheader("Temperature vs Battery Level")
    fig = px.scatter(iot_df, x='temperature', y='battery_level',
                    color='engine_health', title="Temperature vs Battery Level")
    st.plotly_chart(fig, use_container_width=True)

    # Diagnostic codes
    st.subheader("Diagnostic Codes")
    diagnostic_counts = iot_df['diagnostic_code'].value_counts()
    fig = px.bar(x=diagnostic_counts.index, y=diagnostic_counts.values,
                 title="Distribution of Diagnostic Codes")
    st.plotly_chart(fig, use_container_width=True)

    # Device list
    st.subheader("Connected Devices")
    st.dataframe(iot_df)
