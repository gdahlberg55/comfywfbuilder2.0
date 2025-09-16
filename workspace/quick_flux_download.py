#!/usr/bin/env python3
"""
Quick Flux downloader using subprocess and curl/wget
"""

import os
import subprocess
from pathlib import Path

models_dir = Path(r"C:\Users\gdahl\Documents\ComfyUI\models")

downloads = [
    {
        "name": "FLUX UNET FP8",
        "url": "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors",
        "path": models_dir / "unet" / "flux1-dev-fp8.safetensors",
        "size": "5.97 GB"
    },
    {
        "name": "Flux VAE",
        "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
        "path": models_dir / "vae" / "ae.safetensors",
        "size": "335 MB"
    }
]

print("FLUX QUICK DOWNLOADER")
print("=" * 60)

for model in downloads:
    if model["path"].exists():
        print(f"[SKIP] {model['name']} already exists")
        continue
    
    print(f"\nDownloading {model['name']} ({model['size']})")
    print(f"URL: {model['url']}")
    print(f"To: {model['path']}")
    
    # Create directory
    model["path"].parent.mkdir(parents=True, exist_ok=True)
    
    # Try curl first (faster)
    try:
        print("\nTrying curl...")
        cmd = f'curl -L -o "{model["path"]}" "{model["url"]}"'
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"[OK] Downloaded {model['name']}")
            continue
    except:
        pass
    
    # Try PowerShell as fallback
    try:
        print("\nTrying PowerShell...")
        ps_cmd = f'Invoke-WebRequest -Uri "{model["url"]}" -OutFile "{model["path"]}" -UseBasicParsing'
        cmd = f'powershell -Command "{ps_cmd}"'
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"[OK] Downloaded {model['name']}")
    except Exception as e:
        print(f"[ERROR] Failed to download {model['name']}: {e}")

print("\n" + "=" * 60)
print("Download process complete!")
print("\nTo verify models are in place, check:")
print(f"  {models_dir / 'unet'}")
print(f"  {models_dir / 'vae'}")
print(f"  {models_dir / 'clip'}")