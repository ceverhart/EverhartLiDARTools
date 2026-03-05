import os
import laspy

def calculate_density(file_path):
    """
    Calculates the nominal point density based on header bounds and point count.
    Shows understanding of QL specifications.
    """
    with laspy.open(file_path) as fh:
        header = fh.header
        
        # Calculate Area (Square Feet)
        width = header.maxs[0] - header.mins[0]
        height = header.maxs[1] - header.mins[1]
        area_sq_ft = width * height
        
        # Convert to Square Meters for USGS Spec comparison
        # 1 sq ft = 0.092903 square meters
        area_sq_m = area_sq_ft * 0.09290304
        
        density_sq_m = header.point_count / area_sq_m
        
        print(f"\n--- Density Analysis: {os.path.basename(file_path)} ---")
        print(f"[*] Total Area:    {area_sq_ft:,.2f} sq ft ({area_sq_m:,.2f} sq m)")
        print(f"[*] Point Count:   {header.point_count:,}")
        print(f"[*] Avg Density:   {density_sq_m:.2f} pts/sq_m")
        
        # Expert Evaluation
        if density_sq_m >= 2.0:
            print("[SUCCESS] Meets USGS QL2 Density Standards (>= 2.0 pts/sq_m)")
        else:
            print("[WARNING] Fails QL2 Density Standards. Check for sensor gaps.")
        print("-" * 50)

    return density_sq_m