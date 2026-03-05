import laspy
import os

def validate_lidar_header(file_path):
    """
    Reads and prints critical LiDAR metadata to verify USGS Spec compliance.
    """
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return

    print(f"\n--- QC Header Report: {os.path.basename(file_path)} ---")
    
    with laspy.open(file_path) as fh:
        header = fh.header
        
        # Expert Insight: USGS 3DEP usually requires LAS 1.4
        print(f"[*] LAS Version:    {header.version}")
        print(f"[*] Point Format:   {header.point_format.id}")
        print(f"[*] Point Count:    {header.point_count:,}")
        
        # Scale factors (Crucial for precision management)
        print(f"[*] Scale Factors:  X:{header.scales[0]}, Y:{header.scales[1]}, Z:{header.scales[2]}")
        
        # Bounding Box (To verify geographic extent)
        print(f"[*] Bounds (Min):   X:{header.mins[0]:.2f}, Y:{header.mins[1]:.2f}, Z:{header.mins[2]:.2f}")
        print(f"[*] Bounds (Max):   X:{header.maxs[0]:.2f}, Y:{header.maxs[1]:.2f}, Z:{header.maxs[2]:.2f}")
        
        # CRS Check (This proves the data is projected correctly)
        try:
            crs = header.parse_crs()
            print(f"[*] CRS Identified: {crs.name if crs else 'Unknown/Local'}")
        except:
            print("[!] CRS: Could not parse (may be missing or non-standard)")

    print("-" * 50)
