import json
import os
from datetime import datetime

def save_qc_report(metadata, density_stats, file_path, output_folder="data/03_products"):
    """
    Consolidates QC findings into JSON. 
    Uses explicit type casting to avoid JSON serialization errors.
    """
    os.makedirs(output_folder, exist_ok=True)
    report_name = os.path.basename(file_path).replace(".laz", "_QC_Report.json")
    report_path = os.path.join(output_folder, report_name)

    # Expert Fix: Force standard Python types (float, int, bool)
    avg_density = float(density_stats['density'])
    pass_check = bool(avg_density >= 2.0) 

    report_data = {
        "report_timestamp": datetime.now().isoformat(),
        "source_file": os.path.abspath(file_path),
        "header_summary": metadata,
        "density_analysis": {
            "avg_density_pts_m2": round(avg_density, 2),
            "total_points": int(density_stats['count']),
            "area_sq_m": round(float(density_stats['area_m']), 2),
            "pass_ql2": pass_check
        },
        "artifacts": {
            "density_map_tif": report_name.replace("_QC_Report.json", "_density.tif"),
            "preview_png": report_name.replace("_QC_Report.json", "_density_preview.png")
        }
    }

    with open(report_path, 'w') as j:
        json.dump(report_data, j, indent=4)

    print(f"[+] Comprehensive JSON Report generated: {report_path}")
    return report_path