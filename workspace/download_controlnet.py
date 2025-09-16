#!/usr/bin/env python3
"""
Download Flux ControlNet models for ComfyUI
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# Model URLs and paths
MODELS = {
    "flux_controlnet_canny": {
        "url": "https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3/resolve/main/flux-canny-controlnet-v3.safetensors",
        "filename": "flux-canny-controlnet-v3.safetensors",
        "size": "3.58GB"
    },
    "flux_controlnet_depth": {
        "url": "https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3/resolve/main/flux-depth-controlnet-v3.safetensors", 
        "filename": "flux-depth-controlnet-v3.safetensors",
        "size": "3.58GB"
    }
}

def download_file(url, dest_path, chunk_size=8192):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=dest_path.name) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    pbar.update(len(chunk))

def main():
    # ComfyUI models directory
    base_path = Path(r"C:\Users\gdahl\Documents\ComfyUI\models\controlnet")
    base_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("FLUX CONTROLNET MODEL DOWNLOADER")
    print("=" * 60)
    print(f"\nTarget directory: {base_path}")
    print("\nAvailable models:")
    
    for idx, (key, model) in enumerate(MODELS.items(), 1):
        print(f"{idx}. {model['filename']} ({model['size']})")
    
    print("\nOptions:")
    print("1. Download Canny ControlNet only")
    print("2. Download Depth ControlNet only")  
    print("3. Download both models")
    print("4. Skip download (models already exist)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    models_to_download = []
    if choice == "1":
        models_to_download = ["flux_controlnet_canny"]
    elif choice == "2":
        models_to_download = ["flux_controlnet_depth"]
    elif choice == "3":
        models_to_download = ["flux_controlnet_canny", "flux_controlnet_depth"]
    elif choice == "4":
        print("Skipping download. Assuming models are already in place.")
        return
    else:
        print("Invalid choice. Exiting.")
        return
    
    for model_key in models_to_download:
        model = MODELS[model_key]
        dest_file = base_path / model['filename']
        
        if dest_file.exists():
            print(f"\n✓ {model['filename']} already exists, skipping...")
            continue
            
        print(f"\n📥 Downloading {model['filename']}...")
        print(f"URL: {model['url']}")
        print(f"Size: {model['size']}")
        
        try:
            download_file(model['url'], dest_file)
            print(f"✓ Successfully downloaded {model['filename']}")
        except Exception as e:
            print(f"✗ Error downloading {model['filename']}: {e}")
    
    print("\n" + "=" * 60)
    print("Download process complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()