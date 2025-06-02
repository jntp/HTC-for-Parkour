import json
import os
import leafmap.maplibregl as leafmap
import streamlit as st

st.set_page_config(layout="wide")

# Can add sidebar later

st.title("Land Surface Temperature of Chapman University")
st.markdown(
    """
    A 3D interactive web map for visualizing the land surface temperature (°C) of Chapman University and the surrounding neighborhoods in Orange, CA
    """
)

# Map Code
with st.echo():
  # Maptiler API Key
  with open("global/key.txt") as file:
    passkey = file.read() 
    print(passkey) # test; remove later
    os.environ["MAPTILER_KEY"] = passkey

  # Get the LST raster file for Orange, CA
  url = "https://drive.google.com/file/d/1yBrdkK1MOuvFCL0KismdfZmFr8QlViHU/view?usp=drive_link"
  filepath = "LC09_ST_Celsius_Orange.tif"
  LST_Orange = leafmap.download_file(url, filepath)

  # Map view bounds (longitude, latitude)
  bounds = [
    [-117.9238, 33.7452],
    [-117.7918, 33.8358],
  ]

  # Intialize map and add raster
  m = leafmap.Map(zoom=2, pitch=85, max_bounds=bounds, style="3d-terrain") 
  m.add_raster(LST_Orange, colormap="magma", opacity=0.5, name="Surface Temperature") 

  # Get the Chapman University boundary geojson
  url2 = "https://drive.google.com/file/d/1IfImbYAKVDFhmnWa1ADCh2cm_c3OPrMy/view?usp=sharing"
  filepath2 = "ChapmanUniversity_pkBoundary"
  ChapmanUniversity_pkBoundary = leafmap.download_file(url2, filepath2)

  # Add Chapman University boundary geojson to map
  paint = {"line-color": "#00baff", "line-width": 3}
  m.add_geojson(ChapmanUniversity_pkBoundary, layer_type="line", paint=paint, name="Chapman University")

  # Add 3D buildings
  m.add_overture_3d_buildings(values=[0, 6, 12, 18, 24], colors=['lightgray', 'gray', 'darkgray', 'royalblue', 'lightblue']) 

  # Add layer control
  m.add_layer_control(bg_layers=True)

  # Add color bar
  m.add_colorbar(
    cmap="magma", vmin=32.9, vmax=58.9, label="Land Surface Temperature (°C)", position="bottom-right"
  )

  # Add text
  pitch_text = "Hold right click to rotate map view."
  m.add_text(pitch_text, fontsize=16, bg_color="rgba(255, 255, 255, 0.6)", position="bottom-left") # half transparent bg_color


# Add more to the markdown section later
# Left off at finding how to test this code! (see streamlit tutorial) 
# Figure out how to display layer-interact, may need to add rows and cols

