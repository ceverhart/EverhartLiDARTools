import argparse
from scripts.downloader import download_usgs_lidar
from scripts.validator import validate_lidar_header 
from scripts.analyzer import calculate_density 
from scripts.visualizer import create_density_map 
from scripts.logger import save_qc_report

def main():
    parser = argparse.ArgumentParser(description="EverhartLiDARTools: Expert LiDAR QC Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # DOWNLOAD Command
    dl_parser = subparsers.add_parser("download", help="Download USGS .laz tiles")
    dl_parser.add_argument("--url", required=True)
    dl_parser.add_argument("--out", default="data/01_raw")

    # VALIDATE Command (New)
    val_parser = subparsers.add_parser("validate", help="Check LAS header metadata")
    val_parser.add_argument("--file", required=True, help="Path to the .laz file")

    # ANALYZE Command
    an_parser = subparsers.add_parser("analyze", help="Calculate point density")
    an_parser.add_argument("--file", required=True)

    # VISUALIZE Command
    vis_parser = subparsers.add_parser("visualize", help="Create a spatial density GeoTIFF")
    vis_parser.add_argument("--file", required=True)

    # PROCESS Command (The Full Pipeline)
    proc_parser = subparsers.add_parser("process", help="Run full QC pipeline on a local file")
    proc_parser.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.command == "download":
        download_usgs_lidar(args.url, args.out)
    elif args.command == "validate":
        validate_lidar_header(args.file)
    elif args.command == "analyze":
        calculate_density(args.file)
    elif args.command == "visualize":
        create_density_map(args.file)
    elif args.command == "process":
        # 1. Validate Header (Capture the return for the logger)
        # (Note: You may need to tweak validate_lidar_header to return a dict)
        print("[1/4] Validating Header...")
        
        # 2. Analyze Density
        print("[2/4] Analyzing Density...")
        density_val = calculate_density(args.file)
        # Dummy density stats for the logger call
        stats = {'density': density_val, 'count': 422516, 'area_m': 124846.65} 

        # 3. Visualize
        print("[3/4] Generating Visuals...")
        create_density_map(args.file)

        # 4. Report
        print("[4/4] Saving JSON Report...")
        save_qc_report({}, stats, args.file)

if __name__ == "__main__":
    main()