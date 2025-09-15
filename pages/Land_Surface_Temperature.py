import os
import leafmap as lm
import leafmap.maplibregl as leafmap
import streamlit as st

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
url = "https://github.com/jntp/HTC-for-Parkour/raw/refs/heads/main/data/LC09_ST_Celsius_Orange_magma.tif"

# Map view bounds (longitude, latitude)
bounds = [
  [-117.9238, 33.7452],
  [-117.7918, 33.8358],
]

# Intialize map
m = leafmap.Map(zoom=2, pitch=85, max_bounds=bounds, style="3d-terrain") 

# Add COG
m.add_cog_layer(url, name="Surface Temperature", opacity=0.5)
print(lm.cog_tile(url))  
print(lm.cog_bands(url))

# Get the Chapman University boundary geojson
url2 = "https://drive.google.com/file/d/154vW5LgvhO9aZ3zwDFr9x-5IiJkk5H_G/view?usp=drive_link"
filepath2 = "ChapmanUniversity_pkBoundary"
ChapmanUniversity_pkBoundary = leafmap.download_file(url2, filepath2)

# Add Chapman University boundary geojson to map
paint = {"line-color": "#00baff", "line-width": 3}
m.add_geojson(ChapmanUniversity_pkBoundary, layer_type="line", paint=paint, name="Chapman University")

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
