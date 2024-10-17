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

def plot_route(origin, destination):
    origin_port = world_port_index(origin)
    destination_port = world_port_index(destination)
    
    origin_coords = [float(origin_port['Latitude']), float(origin_port['Longitude'])]
    destination_coords = [float(destination_port['Latitude']), float(destination_port['Longitude'])]
    
    m = folium.Map(location=[(origin_coords[0] + destination_coords[0])/2, 
                             (origin_coords[1] + destination_coords[1])/2], 
                   zoom_start=3)
    
    folium.Marker(origin_coords, popup=origin).add_to(m)
    folium.Marker(destination_coords, popup=destination).add_to(m)
    
    route = sr.searoute(origin_coords[::-1], destination_coords[::-1])
    folium.PolyLine(locations=[list(reversed(coord)) for coord in route['geometry']['coordinates']], 
                    color="red", weight=2, opacity=0.8).add_to(m)
    
    return m

st.title('Sea Route Plotter')

origin = st.text_input('Enter origin port:')
destination = st.text_input('Enter destination port:')

if origin and destination:
    try:
        distance = route_distance(origin, destination)
        st.write(f"The distance between {origin} and {destination} is approximately {distance} nautical miles.")
        
        m = plot_route(origin, destination)
        folium_static(m)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.write("Please enter both origin and destination ports to plot the route.")
