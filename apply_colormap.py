import rasterio
from rio_tiler.colormap import cmap
from rasterio.enums import ColorInterp

## Get colormap from rio-tiler
cm = cmap.get("magma")

# Open the input file and prepare COG
with rasterio.open("data/LC09_ST_Celsius_Orange_COG3.tif") as src:
  profile = src.profile.copy()

  # Ensure the output is a COG (GeoTIFF with internal tiling)
  profile.update(
      driver="GTiff",
      tiled=True,
      blockxsize=512,
      blockysize=512,
      compress="LZW",
      interleave="band"
  )

  # Create the output COG with magma colormap
  with rasterio.open("data/LC09_ST_Celsius_Orange_COG3_magma.tif", "w", **profile) as dst:
    # Write data (assuming single-band input)
    dst.write(src.read(1), 1) # Band 1

    # Apply colormap (256 RGB entries)
    dst.write_colormap(1, cm) # Assign to band 1

    # Set color interpretation (critical for GIS software)
    dst.colorinterp = [ColorInterp.palette] # For single-band palettes

print("COG with magma colormap created successfully!")
