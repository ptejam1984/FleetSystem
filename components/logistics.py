import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_logistics(logistics_df):
    st.header("Logistics & Supply Chain Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Shipments", len(logistics_df))
    with col2:
        in_transit = len(logistics_df[logistics_df['status'] == 'In Transit'])
        st.metric("Shipments In Transit", in_transit)
    with col3:
        delayed = len(logistics_df[logistics_df['status'] == 'Delayed'])
        st.metric("Delayed Shipments", delayed)

    # Shipment status distribution
    st.subheader("Shipment Status Distribution")
    status_counts = logistics_df['status'].value_counts()
    fig = px.pie(values=status_counts.values, names=status_counts.index,
                 title="Shipment Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Temperature and humidity
    st.subheader("Temperature and Humidity")
    fig = px.scatter(logistics_df, x='temperature', y='humidity',
                    color='status', title="Temperature vs Humidity by Status")
    st.plotly_chart(fig, use_container_width=True)

    # Origin-Destination pairs
    st.subheader("Popular Routes")
    routes = logistics_df.groupby(['origin', 'destination']).size().reset_index(name='count')
    routes = routes.sort_values('count', ascending=False).head(10)
    fig = px.bar(routes, x='count', y='origin',
                 title="Top 10 Origin Cities",
                 orientation='h')
    st.plotly_chart(fig, use_container_width=True)

    # Shipment list
    st.subheader("Shipment Details")
    st.dataframe(logistics_df)
