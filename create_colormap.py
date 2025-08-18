import numpy as np
from matplotlib import colormaps

## Functions

def apply_colormap(colormap, min_value=0, max_value=1, classes=52):
  colors = colormap(np.linspace(min_value, max_value, num=classes))

  return colors # return RGBA tuples of floats

def create_txt_file(filepath, colors, min_elev, max_elev, classes=52):
  elev_values = np.linspace(min_elev, max_elev, classes)

  with open(filepath, "w") as f:
    for i, (r, g, b, _) in enumerate(colors):
      f.write(f"{elev_values[i]} {int(r*255)} {int(g*255)} {int(b*255)}\n")

## Main Code

# Generate magma colormap (256 colors)
magma = colormaps["magma"]
fp = "data/magma_LST_colormap.txt" 

# colors = magma(np.linspace(0, 1, 256)) # RGBA array
colors = apply_colormap(magma)

create_txt_file(fp, colors, 32.76, 58.87)
