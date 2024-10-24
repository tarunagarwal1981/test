import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Maritime Digital Transformation Demo", layout="wide")

def main():
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Select Demo",
        ["Introduction",
         "IoT & Real-Time Monitoring",
         "Vessel Performance Analytics",
         "Digital Twin Simulation",
         "Predictive Maintenance",
         "CII Calculator"]
    )

    if page == "Introduction":
        show_introduction()
    elif page == "IoT & Real-Time Monitoring":
        show_iot_demo()
    elif page == "Vessel Performance Analytics":
        show_performance_analytics()
    elif page == "Digital Twin Simulation":
        show_digital_twin()
    elif page == "Predictive Maintenance":
        show_predictive_maintenance()
    elif page == "CII Calculator":
        show_cii_calculator()

def show_introduction():
    st.title("Maritime Digital Transformation")
    st.subheader("Interactive Demonstration of Maritime Analytics")

    # Key Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Trade Share", "90%", "Maritime Transport")
    with col2:
        st.metric("Annual CO2 Emissions", "1 billion tons", "2-3% Global Emissions")
    with col3:
        st.metric("Efficiency Potential", "25%", "Through Digital Solutions")

    # Regulatory Timeline
    st.subheader("Regulatory Timeline")
    timeline_data = {
        'Year': [2023, 2024, 2025, 2026],
        'Regulation': ['CII Implementation', 'EU ETS Phase 1', 'FuelEU Maritime', 'CII Rating Impact'],
        'Impact': ['Vessel Rating System', '€100/ton CO2', 'Alternative Fuel Requirements', 'Commercial Restrictions']
    }
    st.dataframe(pd.DataFrame(timeline_data))

def show_iot_demo():
    st.title("IoT & Real-Time Monitoring")
    
    # Simulated real-time sensor data
    def generate_sensor_data():
        return {
            'Engine RPM': np.random.normal(85, 2),
            'Fuel Flow (t/day)': np.random.normal(30, 1),
            'Speed (knots)': np.random.normal(15, 0.5),
            'Wind Speed (knots)': np.random.normal(12, 2),
            'Power (kW)': np.random.normal(15000, 500)
        }

    # Real-time monitoring dashboard
    st.subheader("Real-Time Vessel Monitoring")
    
    # Create columns for metrics
    cols = st.columns(5)
    sensor_data = generate_sensor_data()
    
    for i, (key, value) in enumerate(sensor_data.items()):
        cols[i].metric(key, f"{value:.1f}")

    # Historical trend simulation
    st.subheader("Performance Trends")
    
    # Generate sample historical data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='H')
    df = pd.DataFrame({
        'timestamp': dates,
        'fuel_consumption': np.random.normal(30, 2, 100),
        'speed': np.random.normal(15, 1, 100)
    })

    # Plot historical trends
    fig = px.line(df, x='timestamp', y=['fuel_consumption', 'speed'])
    st.plotly_chart(fig, use_container_width=True)

def show_performance_analytics():
    st.title("Vessel Performance Analytics")

    # Sample performance data
    st.subheader("Trim Optimization Analysis")
    
    # Generate sample trim vs. fuel consumption data
    trim_data = pd.DataFrame({
        'trim': np.linspace(-2, 2, 50),
        'fuel_consumption': 30 + 2*np.sin(np.linspace(-2, 2, 50)) + np.random.normal(0, 0.2, 50)
    })

    fig = px.scatter(trim_data, x='trim', y='fuel_consumption',
                    title='Fuel Consumption vs. Trim',
                    labels={'trim': 'Trim (m)', 'fuel_consumption': 'Fuel Consumption (t/day)'})
    st.plotly_chart(fig, use_container_width=True)

    # Efficiency metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Optimal Trim", "0.5m", "2.3% Improvement")
    with col2:
        st.metric("Fuel Savings", "1.2 t/day", "↓4%")
    with col3:
        st.metric("CO2 Reduction", "3.7 t/day", "↓4%")

def show_digital_twin():
    st.title("Digital Twin Simulation")

    # Simulation parameters
    st.sidebar.subheader("Simulation Parameters")
    speed = st.sidebar.slider("Speed (knots)", 10, 20, 15)
    draft = st.sidebar.slider("Draft (m)", 8, 14, 11)
    wind_speed = st.sidebar.slider("Wind Speed (knots)", 0, 30, 15)

    # Calculate simulated performance
    power = 1000 * (0.3 * speed**3 + 100)
    fuel_consumption = power * 0.00021
    emission = fuel_consumption * 3.114

    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Power (kW)", f"{power:,.0f}")
    with col2:
        st.metric("Fuel Consumption (t/day)", f"{fuel_consumption:.1f}")
    with col3:
        st.metric("CO2 Emissions (t/day)", f"{emission:.1f}")

    # Simulation visualization
    st.subheader("Performance Simulation")
    
    # Create sample simulation data
    sim_speeds = np.linspace(10, 20, 50)
    sim_power = 1000 * (0.3 * sim_speeds**3 + 100)
    
    fig = px.line(x=sim_speeds, y=sim_power,
                 labels={'x': 'Speed (knots)', 'y': 'Power (kW)'},
                 title='Speed-Power Curve')
    fig.add_scatter(x=[speed], y=[power], mode='markers',
                   name='Current Operation')
    st.plotly_chart(fig, use_container_width=True)

def show_predictive_maintenance():
    st.title("Predictive Maintenance Demo")

    # Generate sample engine data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    normal_pattern = np.sin(np.linspace(0, 4*np.pi, 100)) * 2 + 80
    engine_data = pd.DataFrame({
        'date': dates,
        'temperature': normal_pattern + np.random.normal(0, 1, 100),
        'vibration': np.random.normal(5, 0.5, 100),
        'pressure': np.random.normal(4, 0.2, 100)
    })

    # Add anomaly
    engine_data.loc[80:, 'temperature'] += np.linspace(0, 5, 20)

    # Plot engine parameters
    st.subheader("Engine Parameters Monitoring")
    fig = px.line(engine_data, x='date', y=['temperature', 'vibration', 'pressure'],
                 title='Engine Parameters Over Time')
    
    # Add warning threshold
    fig.add_hline(y=85, line_dash="dash", line_color="red",
                 annotation_text="Warning Threshold")
    st.plotly_chart(fig, use_container_width=True)

    # Maintenance prediction
    if engine_data['temperature'].iloc[-1] > 83:
        st.warning('⚠️ Maintenance Required: High temperature trend detected')
        st.info('Recommended Action: Schedule maintenance within next 7 days')
    else:
        st.success('✅ Equipment operating within normal parameters')

def show_cii_calculator():
    st.title("CII Calculator")

    # Input parameters
    st.subheader("Vessel Parameters")
    col1, col2 = st.columns(2)
    with col1:
        dwt = st.number_input("Deadweight Tonnage", value=50000)
        distance = st.number_input("Distance Travelled (nm)", value=5000)
    with col2:
        fuel_consumption = st.number_input("Annual Fuel Consumption (tons)", value=3000)
        cargo_carried = st.number_input("Cargo Carried (tons)", value=40000)

    # Calculate CII
    if st.button("Calculate CII"):
        # Simplified CII calculation
        co2_emissions = fuel_consumption * 3.114
        cii = (co2_emissions * 1000000) / (dwt * distance)
        
        # Determine rating (simplified thresholds)
        rating = "A" if cii < 10 else "B" if cii < 12 else "C" if cii < 15 else "D" if cii < 18 else "E"
        
        # Display results
        st.subheader("CII Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CII Value", f"{cii:.2f}")
        with col2:
            st.metric("CO2 Emissions", f"{co2_emissions:.0f} tons")
        with col3:
            st.metric("CII Rating", rating)
        
        # Recommendations
        if rating in ["D", "E"]:
            st.warning("⚠️ Vessel requires immediate efficiency improvements")
            st.info("""
            Recommended Actions:
            1. Optimize speed profile
            2. Implement trim optimization
            3. Consider hull cleaning
            4. Review route optimization opportunities
            """)
        elif rating == "C":
            st.info("ℹ️ Consider efficiency improvements to maintain competitiveness")
        else:
            st.success("✅ Vessel operating at good efficiency levels")

if __name__ == "__main__":
    main()
