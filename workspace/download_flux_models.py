#!/usr/bin/env python3
"""
Flux Model Downloader with Progress Bars
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm
import hashlib

MODELS_DIR = Path(r"C:\Users\gdahl\Documents\ComfyUI\models")

def download_file(url, dest_path, description=""):
    """Download file with progress bar"""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists
    if dest_path.exists():
        print(f"[OK] {dest_path.name} already exists, skipping...")
        return True
    
    print(f"\nDownloading: {description}")
    print(f"From: {url}")
    print(f"To: {dest_path}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as file:
            with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    pbar.update(len(chunk))
        
        print(f"[OK] Downloaded: {dest_path.name}")
        return True
    except Exception as e:
        print(f"[X] Error downloading {dest_path.name}: {e}")
        return False

def main():
    print("=" * 60)
    print("FLUX MODEL DOWNLOADER FOR COMFYUI")
    print("=" * 60)
    
    # Essential models
    essential = [
        {
            "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors",
            "path": MODELS_DIR / "unet" / "flux1-dev-fp8.safetensors",
            "desc": "Flux.1 Dev UNET (11.9GB) - Main model"
        },
        {
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors",
            "path": MODELS_DIR / "clip" / "t5xxl_fp8_e4m3fn.safetensors",
            "desc": "T5-XXL Text Encoder FP8 (4.7GB)"
        },
        {
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
            "path": MODELS_DIR / "clip" / "clip_l.safetensors",
            "desc": "CLIP-L Text Encoder (246MB)"
        },
        {
            "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
            "path": MODELS_DIR / "vae" / "ae.safetensors",
            "desc": "Flux VAE (335MB)"
        }
    ]
    
    print("\nDownloading essential models...")
    for model in essential:
        download_file(model["url"], model["path"], model["desc"])
    
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE!")
    print("=" * 60)
    print(f"\nModels installed in: {MODELS_DIR}")
    print("\nYou can now use the Flux workflow in ComfyUI!")

if __name__ == "__main__":
    main()
