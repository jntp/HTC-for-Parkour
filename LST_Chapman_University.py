import json
import os
import rasterio
import leafmap as lm
import leafmap.maplibregl as leafmap
import streamlit as st
import matplotlib.cm as cm
from rio_tiler.colormap import cmap
from rio_tiler.io import Reader


st.set_page_config(layout="wide")

# Can add sidebar later

st.title("Land Surface Temperature of Chapman University")
st.markdown(
    """
    A 3D interactive web map for visualizing the land surface temperature (°C) of Chapman University and the surrounding neighborhoods in Orange, CA
    """
)

# Map Code
# with st.echo():
  
# Maptiler API Key
with open("global/key.txt") as file:
  # Load and use Maptiler key
  passkey = file.read() 
  os.environ["MAPTILER_KEY"] = passkey

  # Use Titiler endpoint 
  os.environ["TITILER_ENDPOINT"] = "https://titiler.xyz"

  # Get the LST raster file (COG) for Orange, CA
  url = "https://github.com/jntp/HTC-for-Parkour/raw/refs/heads/main/data/LC09_ST_Celsius_Orange_magma.tif"
  # filepath = "LC09_ST_Celsius_Orange.tif"
  # LST_Orange = leafmap.download_file(url, filepath)
  # print(LST_Orange)

  # Map view bounds (longitude, latitude)
  bounds = [
    [-117.9238, 33.7452],
    [-117.7918, 33.8358],
  ]

  # Intialize map and add raster
  m = leafmap.Map(zoom=2, pitch=85, max_bounds=bounds, style="3d-terrain") 
  # m.add_raster(LST_Orange, colormap="magma", opacity=0.5, name="Surface Temperature") 
  # Test add COG
  print(lm.cog_tile(url)) 
  magma_cmap = cmap.get('magma') 
 
  custom_cmap = {
    "0": "#000000",
    "1": "#008040",
    "2": "#ff0000",
    "3": "#ffff00",
    "4": "#8000ff",
    "5": "#8080ff",
    "6": "#00ff00",
    "7": "#c0c0c0",
    "8": "#16002d",
    "9": "#ff80ff",
    "10": "#b3ffb3",
    "11": "#ff8080",
    "12": "#ffffbf",
    "13": "#000080",
    "14": "#808000",
    "15": "#00ffff",
  }

  print(custom_cmap["0"])

  magma_colormap = cm.get_cmap("magma", 256)
  colors_dict = {
      str(i): f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
      for i, (r, g, b, _) in enumerate(magma_colormap.colors)
  }

  print(colors_dict["0"])
  print(lm.cog_bands(url))

  m.add_cog_layer(url, name="Surface Temperature", opacity=0.5)

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

  # Add color bar
  m.add_colorbar(
    cmap="magma", vmin=32.9, vmax=58.9, label="Land Surface Temperature (°C)", position="bottom-right"
  )

  # Add text
  pitch_text = "Hold right click to rotate map view."
  m.add_text(pitch_text, fontsize=16, bg_color="rgba(255, 255, 255, 0.6)", position="bottom-left") # half transparent bg_color

  # Convert the map to Streamlit component
  m.to_streamlit(width=1200, height=600) 

# Left off at trying to serialize JSON? Try using json.dumps()
# Can you embed a colormap in a COG? Try that out
# How to get the COG to display? Use new COG2 file (issue was with gdal_translate commands... use DeepSeek recommendation)
# Try using COG viewer to preview raster... also may need to use the "traditional method" of adding COG
# How to add a colormap to the COG layer?
# Clean up and delete unnecessary code (see if there's a more efficient way to display geojson)
# Add more to the markdown section later
# How to make the fullscreen function work? 
# Figure out how to display layer-interact, may need to add rows and cols

