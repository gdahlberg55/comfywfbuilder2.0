#!/usr/bin/env python3
"""
Direct Flux Model Downloader - Actually downloads the files
"""

import os
import sys
import urllib.request
import time
from pathlib import Path

def download_with_progress(url, filepath):
    """Download file with simple progress indicator"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.exists():
        print(f"[SKIP] {filepath.name} already exists")
        return True
    
    print(f"\nDownloading: {filepath.name}")
    print(f"From: {url[:80]}...")
    print(f"To: {filepath}")
    
    try:
        def download_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            mb_downloaded = downloaded / 1024 / 1024
            mb_total = total_size / 1024 / 1024
            sys.stdout.write(f'\rProgress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)')
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filepath, reporthook=download_hook)
        print(f"\n[OK] Downloaded: {filepath.name}\n")
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to download {filepath.name}: {e}\n")
        return False

def main():
    print("="*60)
    print("FLUX MODEL DOWNLOADER - DIRECT DOWNLOAD")
    print("="*60)
    print("\nThis will download the 3 essential missing Flux models")
    print("Total size: ~12.5 GB\n")
    
    models_dir = Path(r"C:\Users\gdahl\Documents\ComfyUI\models")
    
    # Essential models to download
    downloads = [
        {
            "name": "FLUX UNET Model",
            "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors",
            "path": models_dir / "unet" / "flux1-dev-fp8.safetensors",
            "size": "11.9 GB"
        },
        {
            "name": "CLIP-L Text Encoder",
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
            "path": models_dir / "clip" / "clip_l.safetensors",
            "size": "246 MB"
        },
        {
            "name": "Flux VAE",
            "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
            "path": models_dir / "vae" / "ae.safetensors",
            "size": "335 MB"
        }
    ]
    
    print("Models to download:")
    for i, model in enumerate(downloads, 1):
        print(f"{i}. {model['name']} ({model['size']})")
    
    print("\n" + "="*60)
    response = input("\nStart download? (y/n): ")
    if response.lower() != 'y':
        print("Download cancelled")
        return
    
    print("\n" + "="*60)
    print("DOWNLOADING MODELS")
    print("="*60)
    
    success = []
    failed = []
    
    for i, model in enumerate(downloads, 1):
        print(f"\n[{i}/{len(downloads)}] {model['name']} ({model['size']})")
        print("-"*40)
        
        if download_with_progress(model['url'], model['path']):
            success.append(model['name'])
        else:
            failed.append(model['name'])
    
    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    
    if success:
        print(f"\n[OK] Successfully downloaded {len(success)} models:")
        for name in success:
            print(f"  - {name}")
    
    if failed:
        print(f"\n[FAILED] Could not download {len(failed)} models:")
        for name in failed:
            print(f"  - {name}")
        print("\nFor failed downloads, try:")
        print("1. Check your internet connection")
        print("2. Download manually from the links in flux_model_links.txt")
        print("3. Use a download manager like IDM or wget")
    else:
        print("\n[SUCCESS] All models downloaded!")
        print("\nYou can now load the Flux workflow in ComfyUI:")
        print("  flux_inpaint_workflow_with_clipskip.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user")
        sys.exit(1)