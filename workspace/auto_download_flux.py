#!/usr/bin/env python3
"""
Auto-download Flux models without user input
"""

import os
import sys
import urllib.request
from pathlib import Path

def download_file(url, filepath):
    """Download with simple progress"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.exists():
        print(f"[SKIP] {filepath.name} already exists")
        return True
    
    print(f"\nDownloading: {filepath.name}")
    print(f"To: {filepath}")
    
    try:
        def hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            mb = downloaded / 1024 / 1024
            total_mb = total_size / 1024 / 1024
            sys.stdout.write(f'\r{percent:.1f}% ({mb:.1f}/{total_mb:.1f} MB)')
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filepath, reporthook=hook)
        print(f"\n[OK] Downloaded\n")
        return True
    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        return False

print("FLUX MODEL AUTO-DOWNLOADER")
print("="*60)
print("Starting automatic download of missing models...")

models_dir = Path(r"C:\Users\gdahl\Documents\ComfyUI\models")

# Only download what's missing
downloads = []

# Check UNET - Using alternative FP8 version that's confirmed working
unet_path = models_dir / "unet" / "flux1-dev-fp8.safetensors"
if not unet_path.exists():
    downloads.append({
        "name": "FLUX UNET FP8 (5.97GB)",
        "url": "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors",
        "path": unet_path
    })

# Check CLIP-L
clip_path = models_dir / "clip" / "clip_l.safetensors"
if not clip_path.exists():
    downloads.append({
        "name": "CLIP-L (246MB)",
        "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
        "path": clip_path
    })

# Check VAE
vae_path = models_dir / "vae" / "ae.safetensors"
if not vae_path.exists():
    downloads.append({
        "name": "Flux VAE (335MB)",
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
        "path": vae_path
    })

if not downloads:
    print("\n[OK] All models already installed!")
else:
    print(f"\nFound {len(downloads)} missing models to download")
    print("="*60)
    
    for i, model in enumerate(downloads, 1):
        print(f"\n[{i}/{len(downloads)}] {model['name']}")
        print("-"*40)
        download_file(model['url'], model['path'])
    
    print("="*60)
    print("DOWNLOAD COMPLETE")

print("\nWorkflow ready: flux_inpaint_workflow_with_clipskip.json")