import requests
import os
from tqdm import tqdm

def download_usgs_lidar(url, dest_folder):
    """
    Downloads a .laz file with professional stream handling and User-Agent headers.
    """
    os.makedirs(dest_folder, exist_ok=True)
    
    filename = url.split('/')[-1]
    file_path = os.path.join(dest_folder, filename)
    
    # Identify as a browser to avoid 403/429 errors from federal servers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status() # Check for HTTP errors
        
        total_size = int(response.headers.get('content-length', 0))
        
        print(f"[*] Downloading: {filename}")
        
        with open(file_path, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                size = f.write(data)
                bar.update(size)
                
        print(f"[+] Download complete: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"[!] Error downloading file: {e}")
        return None
