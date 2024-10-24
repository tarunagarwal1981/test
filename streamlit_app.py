#```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.figure_factory as ff
from scipy.stats import norm
from scipy import stats
import numpy.polynomial.polynomial as poly

# Enhanced styling with darker theme
CUSTOM_CSS = """
<style>
    /* Main app styling */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .css-1d391kg {
        background-color: #0A0C10;
    }
    .stMetric {
        background-color: #161B22;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #21262D;
    }
    .chart-container {
        background-color: #0D1117;
        border-radius: 5px;
        padding: 10px;
        border: 1px solid #21262D;
    }
    h1 {
        color: #00FF88 !important;
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
    }
    h2, h3 {
        color: #58A6FF !important;
        text-shadow: 0 0 8px rgba(88,166,255,0.5);
    }
    .stButton button {
        background-color: #238636;
        color: #FFFFFF;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #2EA043;
        box-shadow: 0 0 10px rgba(46,160,67,0.5);
    }
    .stSelectbox > div > div {
        background-color: #161B22;
        border: 1px solid #21262D;
    }
    .stSelectbox > div > div > div {
        background-color: #161B22;
        color: #FFFFFF;
    }
</style>
"""

# Enhanced color scheme
COLORS = {
    'primary': '#00FF88',    # Neon Green
    'secondary': '#FF00FF',  # Neon Pink
    'tertiary': '#00FFFF',   # Neon Cyan
    'warning': '#FF0000',    # Neon Red
    'background': '#0D1117', # Darker background
    'grid': '#21262D',       # Darker grid
    'text': '#FFFFFF',       # White text
    'accent1': '#58A6FF',    # GitHub blue
    'accent2': '#FF7B72',    # GitHub red
    'accent3': '#FFA657'     # GitHub orange
}

def create_chart_template():
    """Create a consistent dark theme template for charts"""
    return {
        'layout': {
            'paper_bgcolor': COLORS['background'],
            'plot_bgcolor': COLORS['background'],
            'font': {
                'color': COLORS['text'],
                'family': 'Arial, sans-serif'
            },
            'xaxis': {
                'gridcolor': COLORS['grid'],
                'showgrid': True,
                'zeroline': False,
                'linecolor': COLORS['grid'],
                'title_font': {'color': COLORS['text']},
                'tickfont': {'color': COLORS['text']}
            },
            'yaxis': {
                'gridcolor': COLORS['grid'],
                'showgrid': True,
                'zeroline': False,
                'linecolor': COLORS['grid'],
                'title_font': {'color': COLORS['text']},
                'tickfont': {'color': COLORS['text']}
            },
            'legend': {
                'bgcolor': 'rgba(13,17,23,0.8)',
                'font': {'color': COLORS['text']}
            }
        }
    }

# Data generation functions
def generate_vessel_data(days=30):
    """Generate realistic vessel performance data"""
    dates = pd.date_range(end=datetime.now(), periods=days)
    base_speed = 15 + np.sin(np.linspace(0, 4*np.pi, days)) * 2
    
    # Add realistic noise and trends
    speed = base_speed + np.random.normal(0, 0.5, days)
    fuel_consumption = 3.5 * speed**2 + np.random.normal(0, 5, days)
    engine_load = 65 + speed/20*100 + np.random.normal(0, 3, days)
    hull_efficiency = 100 - np.linspace(0, 5, days) + np.random.normal(0, 0.5, days)
    
    # Generate trim data
    trim_range = np.linspace(-2, 2, days)
    trim = np.random.choice(trim_range, days)
    trim_effect = -2 * trim**2 + np.random.normal(0, 0.5, days)
    
    # Calculate CII
    distance = speed * 24  # nautical miles per day
    cii = (fuel_consumption * 3.114) / (distance * 25000/100000)
    
    return pd.DataFrame({
        'date': dates,
        'speed': speed,
        'fuel_consumption': fuel_consumption,
        'engine_load': engine_load,
        'hull_efficiency': hull_efficiency,
        'trim': trim,
        'trim_effect': trim_effect,
        'cii': cii,
        'distance': distance
    })

def create_speed_power_analysis(data):
    """Create sophisticated speed-power analysis with polynomial fit"""
    fig = go.Figure()
    
    # Scatter plot of actual data
    fig.add_trace(go.Scatter(
        x=data['speed'],
        y=data['fuel_consumption'],
        mode='markers',
        name='Operating Points',
        marker=dict(
            size=8,
            color=data['engine_load'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Engine Load (%)')
        )
    ))
    
    # Calculate polynomial fit
    coefs = poly.polyfit(data['speed'], data['fuel_consumption'], 2)
    speed_range = np.linspace(data['speed'].min(), data['speed'].max(), 100)
    fuel_fit = poly.polyval(speed_range, coefs)
    
    # Add polynomial fit line
    fig.add_trace(go.Scatter(
        x=speed_range,
        y=fuel_fit,
        mode='lines',
        name='Best Fit Curve',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    fig.update_layout(
        template=create_chart_template(),
        title="Speed-Power Analysis with Best Fit Curve",
        xaxis_title="Speed (knots)",
        yaxis_title="Fuel Consumption (t/day)",
        height=500
    )
    
    return fig

def create_digital_twin_simulation(data):
    """Create digital twin simulation visualization"""
    # Create subplots for different aspects of the digital twin
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Real-time Performance",
            "Efficiency Analysis",
            "Trim Optimization",
            "Power Analysis"
        )
    )
    
    # Real-time performance plot
    fig.add_trace(
        go.Scatter(
            x=data['date'],
            y=data['hull_efficiency'],
            name="Hull Efficiency",
            line=dict(color=COLORS['primary'])
        ),
        row=1, col=1
    )
    
    # Efficiency analysis
    fig.add_trace(
        go.Scatter(
            x=data['speed'],
            y=data['fuel_consumption'],
            mode='markers',
            name="Operating Points",
            marker=dict(color=COLORS['secondary'])
        ),
        row=1, col=2
    )
    
    # Trim optimization
    fig.add_trace(
        go.Scatter(
            x=data['trim'],
            y=data['trim_effect'],
            mode='markers',
            name="Trim Effect",
            marker=dict(color=COLORS['tertiary'])
        ),
        row=2, col=1
    )
    
    # Power analysis
    fig.add_trace(
        go.Scatter(
            x=data['date'],
            y=data['engine_load'],
            name="Engine Load",
            line=dict(color=COLORS['accent1'])
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        template=create_chart_template(),
        height=800,
        title_text="Digital Twin Simulation",
        showlegend=True
    )
    
    return fig
#```
