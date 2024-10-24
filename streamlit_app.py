```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.figure_factory as ff
from scipy.stats import norm

# Custom CSS for dark theme and styling
CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #32383E;
    }
    .chart-container {
        background-color: #1E1E1E;
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #32383E;
    }
    h1, h2, h3 {
        color: #00FF88 !important;
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
    }
    .stButton button {
        background-color: #00FF88;
        color: #0E1117;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #00CC6A;
        box-shadow: 0 0 10px rgba(0,255,136,0.5);
    }
</style>
"""

# Color scheme
COLORS = {
    'primary': '#00FF88',    # Neon Green
    'secondary': '#FF00FF',  # Neon Pink
    'tertiary': '#00FFFF',   # Neon Cyan
    'warning': '#FF0000',    # Neon Red
    'background': '#1E1E1E', # Dark background
    'grid': '#333333'        # Dark grid
}

# Chart template
def create_chart_template():
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#FFFFFF'},
            'xaxis': {
                'gridcolor': COLORS['grid'],
                'showgrid': True,
                'zeroline': False
            },
            'yaxis': {
                'gridcolor': COLORS['grid'],
                'showgrid': True,
                'zeroline': False
            }
        }
    }

# Utility functions for data generation
def generate_vessel_data(days=30):
    dates = pd.date_range(end=datetime.now(), periods=days)
    return pd.DataFrame({
        'date': dates,
        'speed': np.random.normal(15, 1, days),
        'fuel_consumption': np.random.normal(50, 5, days),
        'engine_load': np.random.normal(75, 5, days),
        'hull_efficiency': 100 - np.linspace(0, 5, days) + np.random.normal(0, 0.5, days)
    })

def create_performance_gauge(value, title, min_val=0, max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'color': COLORS['primary']}},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': COLORS['primary']},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': COLORS['primary'],
            'steps': [
                {'range': [0, max_val/3], 'color': 'rgba(255,0,0,0.1)'},
                {'range': [max_val/3, 2*max_val/3], 'color': 'rgba(255,255,0,0.1)'},
                {'range': [2*max_val/3, max_val], 'color': 'rgba(0,255,0,0.1)'}
            ]
        }
    ))
    fig.update_layout(template=create_chart_template(), height=200)
    return fig

def create_hull_performance_chart(data):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['hull_efficiency'],
        name='Hull Efficiency',
        line=dict(color=COLORS['primary'], width=2),
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=data['date'],
        y=[100] * len(data),
        name='Reference',
        line=dict(color=COLORS['tertiary'], dash='dash'),
        mode='lines'
    ))

    fig.update_layout(
        template=create_chart_template(),
        title="Hull Performance Trend",
        height=400
    )
    return fig

def create_speed_consumption_chart(data):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['speed'],
        y=data['fuel_consumption'],
        mode='markers',
        marker=dict(
            size=8,
            color=data['engine_load'],
            colorscale='Viridis',
            showscale=True
        ),
        name='Operating Points'
    ))

    fig.update_layout(
        template=create_chart_template(),
        title="Speed vs. Fuel Consumption",
        height=400,
        xaxis_title="Speed (knots)",
        yaxis_title="Fuel Consumption (t/day)"
    )
    return fig

def create_engine_performance_chart(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=data['date'],
            y=data['engine_load'],
            name="Engine Load",
            line=dict(color=COLORS['primary']),
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=data['date'],
            y=data['fuel_consumption'],
            name="Fuel Consumption",
            line=dict(color=COLORS['secondary']),
        ),
        secondary_y=True
    )

    fig.update_layout(
        template=create_chart_template(),
        title="Engine Performance Analysis",
        height=400
    )
    return fig

def main():
    # Page config
    st.set_page_config(page_title="Maritime Analytics Platform", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Module",
        ["Dashboard", "Hull Performance", "Engine Analytics", "Voyage Analysis"]
    )

    vessel = st.sidebar.selectbox(
        "Select Vessel",
        ["Vessel 001", "Vessel 002", "Vessel 003"]
    )

    # Generate sample data
    data = generate_vessel_data()

    if page == "Dashboard":
        st.title("Maritime Analytics Dashboard")
        
        # Key Performance Indicators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.plotly_chart(create_performance_gauge(87, "Hull Performance"), use_container_width=True)
        with col2:
            st.plotly_chart(create_performance_gauge(92, "Engine Efficiency"), use_container_width=True)
        with col3:
            st.plotly_chart(create_performance_gauge(95, "Propeller Efficiency"), use_container_width=True)
        with col4:
            st.plotly_chart(create_performance_gauge(78, "Fuel Efficiency"), use_container_width=True)

        # Main charts
        st.plotly_chart(create_hull_performance_chart(data), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_speed_consumption_chart(data), use_container_width=True)
        with col2:
            st.plotly_chart(create_engine_performance_chart(data), use_container_width=True)

    elif page == "Hull Performance":
        st.title("Hull Performance Analysis")
        
        # Hull performance metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Hull Efficiency", "87%", "-2.3%")
            st.metric("Estimated Fuel Penalty", "3.5%", "1.2%")
        with col2:
            st.metric("Days Since Last Cleaning", "145 days", None)
            st.metric("Recommended Cleaning", "In 35 days", None)

        # Hull performance chart
        st.plotly_chart(create_hull_performance_chart(data), use_container_width=True)

    elif page == "Engine Analytics":
        st.title("Engine Performance Analytics")
        
        # Engine metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Load", "75%", "2.1%")
        with col2:
            st.metric("SFOC", "176 g/kWh", "-0.8%")
        with col3:
            st.metric("Efficiency", "92%", "0.5%")

        # Engine performance chart
        st.plotly_chart(create_engine_performance_chart(data), use_container_width=True)

    elif page == "Voyage Analysis":
        st.title("Voyage Analysis")
        
        # Voyage metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Speed", "14.5 knots", "0.3 knots")
            st.metric("Distance Covered", "3,521 nm", None)
        with col2:
            st.metric("Fuel Consumption", "45.2 mt/day", "-2.1 mt/day")
            st.metric("CO2 Emissions", "141 t/day", "-6.5 t/day")

        # Speed consumption chart
        st.plotly_chart(create_speed_consumption_chart(data), use_container_width=True)

if __name__ == "__main__":
    main()
```
