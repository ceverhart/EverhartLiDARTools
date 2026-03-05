import pdal
import json
import os
from scripts.reporter import generate_qc_thumbnail

def create_density_map(file_path, output_folder="data/03_products"):
    """
    Uses PDAL to create a GeoTIFF where each pixel value = point density.
    This reveals sensor gaps that 'Average Density' might hide.
    """
    os.makedirs(output_folder, exist_ok=True)
    out_raster = os.path.join(output_folder, os.path.basename(file_path).replace(".laz", "_density.tif"))

    # PDAL Pipeline: Read -> Compute Density (Filters.stats) -> Write Raster
    # We use a 2-meter resolution for the grid to see fine-grained gaps
    pipeline_json = {
        "pipeline": [
            file_path,
            {
                "type": "writers.gdal",
                "filename": out_raster,
                "resolution": 2.0, 
                "output_type": "count",
                "data_type": "float"
            }
        ]
    }

    print(f"[*] Generating Spatial Density Grid: {out_raster}")
    
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    
    # NEW: Automatically generate the PNG after the TIF is ready
    generate_qc_thumbnail(out_raster)
    
    print(f"[+] Spatial QC Complete.")
    return out_raster
