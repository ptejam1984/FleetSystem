import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_insurance_telematics(telematics_df):
    st.header("Insurance Telematics Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_safety = round(telematics_df['safety_score'].mean(), 2)
        st.metric("Average Safety Score", avg_safety)
    with col2:
        total_distance = telematics_df['distance_driven'].sum()
        st.metric("Total Distance Driven", f"{total_distance} km")
    with col3:
        total_events = (telematics_df['harsh_braking'].sum() + 
                       telematics_df['speeding_events'].sum() + 
                       telematics_df['sharp_turns'].sum())
        st.metric("Total Safety Events", total_events)

    # Safety score distribution
    st.subheader("Safety Score Distribution")
    fig = px.histogram(telematics_df, x='safety_score', nbins=20,
                      title="Distribution of Safety Scores")
    st.plotly_chart(fig, use_container_width=True)

    # Events by type
    st.subheader("Safety Events by Type")
    events_data = {
        'Event Type': ['Harsh Braking', 'Speeding', 'Sharp Turns'],
        'Count': [
            telematics_df['harsh_braking'].sum(),
            telematics_df['speeding_events'].sum(),
            telematics_df['sharp_turns'].sum()
        ]
    }
    fig = px.bar(events_data, x='Event Type', y='Count',
                 title="Safety Events by Type")
    st.plotly_chart(fig, use_container_width=True)

    # Detailed data
    st.subheader("Telematics Data")
    st.dataframe(telematics_df)
