import os
import requests
import leafmap as lm
import leafmap.maplibregl as leafmap
import streamlit as st
from rasterio.io import MemoryFile
from localtileserver import TileClient, get_leaflet_tile_layer

## Streamlit App Configurations 
st.set_page_config(layout="wide")

st.sidebar.title("About")

st.sidebar.info(
    """
    ***Justin's Mapping Corner***

    **Contact:**
    - Justin Tang | jrtang@proton.me | [GitHub](https://github.com/jntp)
    """
)

st.title("🏜️")
st.header("Land Surface Temperature of Chapman University") 

st.markdown(
    """
    A 3D interactive web map for visualizing the land surface temperature (°C) of Chapman University and the surrounding neighborhoods in 
    Orange, CA.
    """
)

st.info("Note: Buildings heights are displayed in meters (m).")

## Map Configurations
# with open("global/key.txt") as file:
  # Load and use Maptiler key
#  passkey = file.read() 
os.environ["MAPTILER_KEY"] = "ZqrhVFalxz86D81BGOGK"

# Use Titiler endpoint 
os.environ["TITILER_ENDPOINT"] = "https://titiler.xyz"

# Get the LST raster file (COG) for Orange, CA
# url = "https://github.com/jntp/HTC-for-Parkour/raw/refs/heads/main/data/LC09_ST_Celsius_Orange_magma.tif"
# url = "https://raw.githubusercontent.com/jntp/HTC-for-Parkour/refs/heads/main/data/LC09_ST_Celsius_Orange_magma.tif"
url = "https://jntp.github.io/jntp-pages/TIFF/LC09_ST_Celsius_Orange_magma.tif"

# Map view bounds (longitude, latitude)
bounds = [
  [-117.9238, 33.7452],
  [-117.7918, 33.8358],
]

# Intialize map
m = leafmap.Map(zoom=2, pitch=85, max_bounds=bounds, style="3d-terrain")  

# Fetch the COG and serve it locally
response_cog = requests.get(url)
with open("temp_cog.tif", "wb") as f:
    f.write(response_cog.content)

# client = TileClient("temp_cog.tif")
# m.add_tile_layer(client.get_tile_url(), name="COG Layer")

# Add COG
# m.add_cog_layer(url, name="Surface Temperature", opacity=0.5)
# print(lm.cog_tile(url))  
# print(lm.cog_bands(url))

# TEST Load COG using TileClient - New Code
tile_client = TileClient(url)
t = get_leaflet_tile_layer(tile_client, opacity=0.5, name="Surface Temperature")
m.add_tile_layer(url, name="Surface Temperature")

# ChapmanBoundary_url = "https://raw.githubusercontent.com/jntp/HTC-for-Parkour/refs/heads/main/data/ChapmanUniversity_pkBoundary_latlng.geojson"
ChapmanBoundary_url = "https://jntp.github.io/jntp-pages/GeoJSON/ChapmanUniversity_pkBoundary_latlng.geojson"
response = requests.get(ChapmanBoundary_url)
ChapmanUniversity_pkBoundary = response.json()

try:
  response = requests.head(url)
  st.write(f"URL status: {response.status_code}")
  st.write(f"CORS headers: {response.headers.get('Access-Control-Allow-Origin')}")
except Exception as e:
  st.error(f"Error accessing URL: {e}")

try:
  response = requests.head(ChapmanBoundary_url)
  st.write(f"URL status: {response.status_code}")
  st.write(f"CORS headers: {response.headers.get('Access-Control-Allow-Origin')}")
except Exception as e:
  st.error(f"Error accessing URL: {e}")

# paint = {"line-color": "#00baff", "line-width": 3}
# m.add_geojson(ChapmanBoundary_url, layer_type="line", paint=paint, name="Chapman University")

# Debug: Check if data loaded
print("GeoJSON loaded:", "features" in ChapmanUniversity_pkBoundary)

# Try adding as a source first
m.add_source("chapman-source", {"type": "geojson", "data": ChapmanUniversity_pkBoundary})
m.add_layer({
    "id": "chapman-line",
    "type": "line",
    "source": "chapman-source",
    "paint": {"line-color": "#00baff", "line-width": 3}
})

# Add 3D buildings
m.add_overture_3d_buildings(values=[0, 6, 12, 18, 24], colors=['lightgray', 'gray', 'darkgray', 'royalblue', 'lightblue']) 

# Add layer control
m.add_layer_control(bg_layers=True)

# Add colorbar
m.add_colorbar(
  cmap="magma", vmin=32.9, vmax=58.9, label="Land Surface Temperature (°C)", position="bottom-right"
)

# Add text
pitch_text = "Hold right click to rotate map view."
m.add_text(pitch_text, fontsize=16, bg_color="rgba(255, 255, 255, 0.6)", position="bottom-left") # half transparent bg_color 

# Convert the map to Streamlit component
m.to_streamlit(width=1200, height=600)

# How to make the fullscreen function work? 
# Figure out how to display layer-interact, may need to add rows and cols
# Left off at removing cors proxy, try creating a GitHub Pages using a new repo:
# https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
# Run Streamlit App again and work through new errors. Check Claude's answer as well.
