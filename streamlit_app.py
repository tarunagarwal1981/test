import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import searoute as sr
from fuzzywuzzy import process

# Load the World Port Index data
@st.cache_data
def load_wpi_data():
    return pd.read_csv("UpdatedPub150.csv")

wpi_data = load_wpi_data()

def world_port_index(port_to_match):
    best_match = process.extractOne(port_to_match, wpi_data['Main Port Name'])
    return wpi_data[wpi_data['Main Port Name'] == best_match[0]].iloc[0]

def route_distance(origin, destination):
    origin_port = world_port_index(origin)
    destination_port = world_port_index(destination)
    
    origin_coords = [float(origin_port['Longitude']), float(origin_port['Latitude'])]
    destination_coords = [float(destination_port['Longitude']), float(destination_port['Latitude'])]
    
    sea_route = sr.searoute(origin_coords, destination_coords, units="naut")
    return int(sea_route['properties']['length'])

def plot_route(ports):
    if len(ports) < 2:
        return None

    # Calculate the center of all ports
    lats = []
    lons = []
    for port in ports:
        port_info = world_port_index(port)
        lats.append(float(port_info['Latitude']))
        lons.append(float(port_info['Longitude']))
    
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    # Add markers and route lines
    for i in range(len(ports)):
        port = ports[i]
        port_info = world_port_index(port)
        coords = [float(port_info['Latitude']), float(port_info['Longitude'])]
        folium.Marker(coords, popup=port).add_to(m)

        if i < len(ports) - 1:
            next_port = ports[i+1]
            next_port_info = world_port_index(next_port)
            next_coords = [float(next_port_info['Longitude']), float(next_port_info['Latitude'])]
            route = sr.searoute(coords[::-1], next_coords)
            folium.PolyLine(locations=[list(reversed(coord)) for coord in route['geometry']['coordinates']], 
                            color="red", weight=2, opacity=0.8).add_to(m)

    return m

st.title('Sea Route Plotter')

# Initialize session state for ports if it doesn't exist
if 'ports' not in st.session_state:
    st.session_state.ports = ['', '']

# Function to add a new port input field
def add_port():
    st.session_state.ports.append('')

# Display port input fields
for i, port in enumerate(st.session_state.ports):
    st.session_state.ports[i] = st.text_input(f'Port {i+1}:', value=port, key=f'port_{i}')

# Add port button
st.button('Add Port', on_click=add_port)

# Calculate route if we have at least two ports
if len(st.session_state.ports) >= 2 and all(st.session_state.ports):
    try:
        # Calculate total distance
        total_distance = 0
        for i in range(len(st.session_state.ports) - 1):
            distance = route_distance(st.session_state.ports[i], st.session_state.ports[i+1])
            total_distance += distance
            st.write(f"Distance from {st.session_state.ports[i]} to {st.session_state.ports[i+1]}: {distance} nautical miles")

        st.write(f"Total distance: {total_distance} nautical miles")

        # Plot the route
        m = plot_route(st.session_state.ports)
        if m:
            folium_static(m)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.write("Please enter at least two ports to plot the route.")
