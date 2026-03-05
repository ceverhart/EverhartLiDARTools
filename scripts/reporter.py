import rasterio
import matplotlib.pyplot as plt
import os
import numpy as np

def generate_qc_thumbnail(tif_path):
    """
    Converts a density GeoTIFF into a polished PNG for portfolio display.
    """
    output_png = tif_path.replace(".tif", "_preview.png")
    
    with rasterio.open(tif_path) as src:
        # Read the first band (Point Counts)
        data = src.read(1)
        
        # Mask out '0' values (no data) so they don't skew the colors
        data = np.where(data == 0, np.nan, data)

        plt.figure(figsize=(10, 8))
        
        # Use 'viridis' or 'plasma' - perceptually uniform colormaps
        im = plt.imshow(data, cmap='viridis')
        
        # Add a colorbar with a label
        cbar = plt.colorbar(im)
        cbar.set_label('Points per 2m Cell')
        
        plt.title(f"Spatial Density QC: {os.path.basename(tif_path)}")
        plt.axis('off') # Hide pixel coordinates for a cleaner look
        
        plt.savefig(output_png, bbox_inches='tight', dpi=150)
        plt.close()
        
    print(f"[+] Portfolio Thumbnail Generated: {output_png}")
    return output_png
