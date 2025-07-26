import numpy as np
from matplotlib import colormaps

# Generate magma colormap (256 colors)
magma = colormaps["magma"]
colors = magma(np.linspace(0, 1, 256)) # RGBA array

# Write to GDAL-compatible color table file
with open("data/magma_colormap.txt", "w") as f:
  for i, (r, g, b, _) in enumerate(colors):
    f.write(f"{i} {int(r*255)} {int(g*255)} {int(b*255)}\n")
