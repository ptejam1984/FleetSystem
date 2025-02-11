import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_construction(construction_df):
    st.header("Construction & Heavy Equipment Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Equipment", len(construction_df))
    with col2:
        avg_util = round(construction_df['utilization_rate'].mean(), 2)
        st.metric("Average Utilization", f"{avg_util}%")
    with col3:
        avg_fuel = round(construction_df['fuel_consumption'].mean(), 2)
        st.metric("Average Fuel Consumption", f"{avg_fuel}L/hr")

    # Equipment type distribution
    st.subheader("Equipment Type Distribution")
    type_counts = construction_df['type'].value_counts()
    fig = px.pie(values=type_counts.values, names=type_counts.index,
                 title="Equipment Type Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Utilization rates
    st.subheader("Equipment Utilization Rates")
    fig = px.box(construction_df, x='type', y='utilization_rate',
                 title="Utilization Rates by Equipment Type")
    st.plotly_chart(fig, use_container_width=True)

    # Fuel consumption by type
    st.subheader("Fuel Consumption by Equipment Type")
    avg_fuel = construction_df.groupby('type')['fuel_consumption'].mean().reset_index()
    fig = px.bar(avg_fuel, x='type', y='fuel_consumption',
                 title="Average Fuel Consumption by Equipment Type")
    st.plotly_chart(fig, use_container_width=True)

    # Equipment list
    st.subheader("Equipment Details")
    st.dataframe(construction_df)
