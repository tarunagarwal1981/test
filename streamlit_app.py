import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import random

# Set page config
st.set_page_config(
    page_title="Maritime Analytics Dashboard",
    page_icon="🚢",
    layout="wide"
)

# Custom CSS for futuristic look
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .css-1d391kg {
        background-color: #1A1C23;
    }
    .streamlit-expanderHeader {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

# Generate sample data
def generate_ship_data(days=365):
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    # Basic vessel data
    data = {
        'date': dates,
        'speed': np.random.normal(15, 2, days),  # Average speed 15 knots
        'fuel_consumption': np.random.normal(50, 5, days),  # MT/day
        'hull_fouling_index': np.cumsum(np.random.normal(0.01, 0.005, days)),  # Gradually increasing
        'main_engine_power': np.random.normal(20000, 1000, days),  # kW
        'rpm': np.random.normal(100, 5, days),
        'wind_speed': np.random.normal(15, 5, days),
        'wave_height': np.random.normal(2, 0.5, days),
        'trim': np.random.normal(0, 0.5, days),
        'co2_emissions': np.random.normal(160, 10, days),  # g/ton-mile
    }
    
    df = pd.DataFrame(data)
    
    # Add some realistic relationships
    df['fuel_consumption'] += df['speed'] * 0.5  # Higher speed = higher consumption
    df['co2_emissions'] = df['fuel_consumption'] * 3.114  # Standard conversion factor
    df['hull_fouling_index'] = np.clip(df['hull_fouling_index'], 0, 5)
    
    return df

def generate_voyage_data():
    # Sample ports
    ports = {
        'Singapore': (1.3521, 103.8198),
        'Rotterdam': (51.9225, 4.4792),
        'Shanghai': (31.2304, 121.4737),
        'Los Angeles': (33.7425, -118.2079),
        'Dubai': (25.2697, 55.3095)
    }
    
    voyages = []
    for i in range(5):
        start, end = random.sample(list(ports.items()), 2)
        voyages.append({
            'voyage_id': f'V{i+1}',
            'start_port': start[0],
            'end_port': end[0],
            'start_lat': start[1][0],
            'start_lon': start[1][1],
            'end_lat': end[1][0],
            'end_lon': end[1][1],
            'status': random.choice(['Completed', 'In Progress', 'Planned'])
        })
    
    return pd.DataFrame(voyages)

# Sidebar navigation
def sidebar():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox(
        'Select Page',
        ['Overview', 'Hull Performance', 'Emissions Tracking', 
         'Machinery Performance', 'Trim Optimization', 
         'Speed & Consumption', 'Voyage Monitoring']
    )
    return page

# Main pages
def overview_page(df):
    st.title('Maritime Analytics Overview')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Speed", f"{df['speed'].mean():.1f} knots", 
                 f"{df['speed'].mean() - df['speed'].shift(30).mean():.1f}")
    with col2:
        st.metric("Fuel Consumption", f"{df['fuel_consumption'].mean():.1f} MT/day",
                 f"{df['fuel_consumption'].mean() - df['fuel_consumption'].shift(30).mean():.1f}")
    with col3:
        st.metric("CO2 Emissions", f"{df['co2_emissions'].mean():.1f} g/ton-mile",
                 f"{df['co2_emissions'].mean() - df['co2_emissions'].shift(30).mean():.1f}")
    
    # Recent trends
    st.subheader("Recent Performance Trends")
    fig = px.line(df.tail(30), x='date', y=['speed', 'fuel_consumption', 'co2_emissions'],
                  template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # Raw data table
    st.subheader("Raw Data")
    st.dataframe(df.tail(10).style.background_gradient(cmap='Greens'))

def hull_performance_page(df):
    st.title('Hull Performance Analysis')
    
    # Hull fouling trend
    st.subheader("Hull Fouling Index Trend")
    fig = px.line(df, x='date', y='hull_fouling_index',
                  template="plotly_dark")
    fig.add_hline(y=3, line_dash="dash", line_color="red",
                  annotation_text="Critical Threshold")
    st.plotly_chart(fig, use_container_width=True)
    
    # Speed vs Power analysis
    st.subheader("Speed-Power Relationship")
    fig = px.scatter(df, x='speed', y='main_engine_power',
                    color='hull_fouling_index',
                    template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def emissions_page(df):
    st.title('Emissions & CII Tracking')
    
    # Calculate CII (simplified)
    cii = df['co2_emissions'].rolling(window=30).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=cii, name='CII Rating'))
    fig.add_hline(y=180, line_dash="dash", line_color="red", name='Threshold D')
    fig.add_hline(y=150, line_dash="dash", line_color="yellow", name='Threshold C')
    fig.add_hline(y=120, line_dash="dash", line_color="green", name='Threshold B')
    
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def main():
    page = sidebar()
    
    # Generate sample data
    df = generate_ship_data()
    voyage_df = generate_voyage_data()
    
    if page == 'Overview':
        overview_page(df)
    elif page == 'Hull Performance':
        hull_performance_page(df)
    elif page == 'Emissions Tracking':
        emissions_page(df)
    # Add other pages as needed

if __name__ == "__main__":
    main()
