import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # First request to get the direct download URL
    print("Getting download URL...")
    response = requests.get(url, headers=headers, allow_redirects=True)
    download_url = response.url
    
    # Now download the actual file
    print(f"Starting download from {download_url}")
    response = requests.get(download_url, headers=headers, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    if total_size < 1_000_000_000:  # Less than 1GB
        print(f"Warning: File size ({total_size / 1_000_000:.2f}MB) seems too small for a model!")
        user_input = input("Continue anyway? (y/n): ")
        if user_input.lower() != 'y':
            print("Download cancelled.")
            return
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=8192):
            size = file.write(data)
            progress_bar.update(size)

def main():
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    os.makedirs(models_dir, exist_ok=True)

    # Model URL from Civitai
    model_url = "https://civitai.com/api/download/models/1502008"  # EpicJuggernautXL VXV+XI
    model_path = os.path.join(models_dir, "epicjuggernautxl_vxvXI.safetensors")

    print(f"Downloading EpicJuggernautXL model to {model_path}...")
    download_file(model_url, model_path)
    print("Download complete!")

if __name__ == "__main__":
    main() 