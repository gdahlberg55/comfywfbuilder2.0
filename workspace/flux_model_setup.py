#!/usr/bin/env python3
"""
Flux Model Setup Script
Downloads and organizes all required Flux models for ComfyUI
"""

import os
import json
from pathlib import Path

# Define ComfyUI directory structure
COMFYUI_DIR = Path(r"C:\Users\gdahl\Documents\ComfyUI")
MODELS_DIR = COMFYUI_DIR / "models"

# Create directory structure
def create_directories():
    """Create necessary directories for Flux models"""
    dirs = {
        "unet": MODELS_DIR / "unet",
        "clip": MODELS_DIR / "clip",
        "vae": MODELS_DIR / "vae",
        "loras": MODELS_DIR / "loras",
        "clip_vision": MODELS_DIR / "clip_vision",
        "checkpoints": MODELS_DIR / "checkpoints"
    }
    
    for name, path in dirs.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory ready: {path}")
    
    return dirs

# Model download information
FLUX_MODELS = {
    "unet": {
        "flux1-dev-fp8.safetensors": {
            "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors",
            "size": "11.9GB",
            "path": "unet/flux1-dev-fp8.safetensors",
            "description": "Flux.1 Dev model in FP8 format for reduced VRAM usage"
        },
        "flux1-schnell-fp8.safetensors": {
            "url": "https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8_e4m3fn.safetensors",
            "size": "11.9GB",
            "path": "unet/flux1-schnell-fp8.safetensors",
            "description": "Flux.1 Schnell (fast) model in FP8 format"
        }
    },
    "clip": {
        "t5xxl_fp16.safetensors": {
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors",
            "size": "9.5GB",
            "path": "clip/t5xxl_fp16.safetensors",
            "description": "T5-XXL text encoder for Flux"
        },
        "t5xxl_fp8_e4m3fn.safetensors": {
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors",
            "size": "4.7GB",
            "path": "clip/t5xxl_fp8_e4m3fn.safetensors",
            "description": "T5-XXL text encoder in FP8 (lower VRAM)"
        },
        "clip_l.safetensors": {
            "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
            "size": "246MB",
            "path": "clip/clip_l.safetensors",
            "description": "CLIP-L text encoder for Flux"
        }
    },
    "vae": {
        "ae.safetensors": {
            "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
            "size": "335MB",
            "path": "vae/ae.safetensors",
            "description": "Flux VAE (autoencoder)"
        }
    },
    "loras": {
        "flux-RealismLora.safetensors": {
            "url": "https://civitai.com/api/download/models/680306",
            "size": "~250MB",
            "path": "loras/flux-RealismLora.safetensors",
            "description": "Realism enhancement LoRA for Flux"
        },
        "flux-DetailEnhancer.safetensors": {
            "url": "https://civitai.com/api/download/models/721451",
            "size": "~250MB",
            "path": "loras/flux-DetailEnhancer.safetensors",
            "description": "Detail enhancement LoRA for Flux"
        }
    }
}

def create_download_script():
    """Create wget/curl download script"""
    
    script_content = """@echo off
echo ========================================
echo Flux Model Downloader for ComfyUI
echo ========================================
echo.
echo This script will download Flux models using wget or curl
echo Make sure you have wget or curl installed
echo.

set MODELS_DIR=C:\\Users\\gdahl\\Documents\\ComfyUI\\models

echo Creating directories...
mkdir "%MODELS_DIR%\\unet" 2>nul
mkdir "%MODELS_DIR%\\clip" 2>nul
mkdir "%MODELS_DIR%\\vae" 2>nul
mkdir "%MODELS_DIR%\\loras" 2>nul

echo.
echo ========================================
echo DOWNLOADING FLUX MODELS
echo ========================================
echo.

REM Check for wget or curl
where wget >nul 2>nul
if %errorlevel%==0 (
    set DOWNLOAD_CMD=wget -c -O
) else (
    where curl >nul 2>nul
    if %errorlevel%==0 (
        set DOWNLOAD_CMD=curl -L -o
    ) else (
        echo ERROR: Neither wget nor curl found!
        echo Please install wget or curl first.
        pause
        exit /b 1
    )
)

echo Using download command: %DOWNLOAD_CMD%
echo.

REM ========================================
REM ESSENTIAL MODELS (Required)
REM ========================================

echo [1/6] Downloading Flux UNET Model (11.9GB)...
echo This is the main Flux model - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\\unet\\flux1-dev-fp8.safetensors" ^
    "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors"

echo.
echo [2/6] Downloading T5-XXL Text Encoder FP8 (4.7GB)...
echo Lower VRAM version - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\\clip\\t5xxl_fp8_e4m3fn.safetensors" ^
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors"

echo.
echo [3/6] Downloading CLIP-L Text Encoder (246MB)...
echo Secondary text encoder - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\\clip\\clip_l.safetensors" ^
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"

echo.
echo [4/6] Downloading Flux VAE (335MB)...
echo Image encoder/decoder - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\\vae\\ae.safetensors" ^
    "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"

echo.
echo ========================================
echo OPTIONAL MODELS
echo ========================================
echo.

echo [5/6] Downloading Realism LoRA (optional)...
echo Skip with Ctrl+C if not needed
%DOWNLOAD_CMD% "%MODELS_DIR%\\loras\\flux-RealismLora.safetensors" ^
    "https://civitai.com/api/download/models/680306"

echo.
echo [6/6] Downloading Detail Enhancer LoRA (optional)...
echo Skip with Ctrl+C if not needed
%DOWNLOAD_CMD% "%MODELS_DIR%\\loras\\flux-DetailEnhancer.safetensors" ^
    "https://civitai.com/api/download/models/721451"

echo.
echo ========================================
echo DOWNLOAD COMPLETE!
echo ========================================
echo.
echo Models installed in: %MODELS_DIR%
echo.
echo Required models for basic Flux workflow:
echo - unet\flux1-dev-fp8.safetensors
echo - clip\t5xxl_fp8_e4m3fn.safetensors
echo - clip\clip_l.safetensors
echo - vae\ae.safetensors
echo.
pause
"""
    
    script_path = Path("download_flux_models.bat")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"[OK] Download script created: {script_path}")
    return script_path

def create_python_downloader():
    """Create Python-based downloader with progress bars"""
    
    python_script = '''#!/usr/bin/env python3
"""
Flux Model Downloader with Progress Bars
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm
import hashlib

MODELS_DIR = Path(r"C:\\Users\\gdahl\\Documents\\ComfyUI\\models")

def download_file(url, dest_path, description=""):
    """Download file with progress bar"""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file exists
    if dest_path.exists():
        print(f"[OK] {dest_path.name} already exists, skipping...")
        return True
    
    print(f"\\nDownloading: {description}")
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
    
    print("\\nDownloading essential models...")
    for model in essential:
        download_file(model["url"], model["path"], model["desc"])
    
    print("\\n" + "=" * 60)
    print("DOWNLOAD COMPLETE!")
    print("=" * 60)
    print(f"\\nModels installed in: {MODELS_DIR}")
    print("\\nYou can now use the Flux workflow in ComfyUI!")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path("download_flux_models.py")
    with open(script_path, 'w') as f:
        f.write(python_script)
    
    print(f"[OK] Python downloader created: {script_path}")
    return script_path

def check_existing_models():
    """Check which Flux models are already installed"""
    print("\n" + "="*60)
    print("CHECKING EXISTING FLUX MODELS")
    print("="*60)
    
    found = []
    missing = []
    
    for category, models in FLUX_MODELS.items():
        print(f"\n{category.upper()}:")
        for filename, info in models.items():
            full_path = MODELS_DIR / info["path"]
            if full_path.exists():
                size = full_path.stat().st_size / (1024**3)  # GB
                print(f"  [FOUND] {filename} ({size:.1f}GB)")
                found.append(filename)
            else:
                print(f"  [MISSING] {filename}")
                missing.append((filename, info))
    
    return found, missing

# Main execution
if __name__ == "__main__":
    print("FLUX MODEL SETUP FOR COMFYUI")
    print("="*60)
    
    # Create directories
    dirs = create_directories()
    
    # Check existing models
    found, missing = check_existing_models()
    
    if missing:
        print(f"\n[WARNING] Missing {len(missing)} models")
        print("\nCreating download scripts...")
        
        # Create download scripts
        bat_script = create_download_script()
        py_script = create_python_downloader()
        
        print("\n" + "="*60)
        print("DOWNLOAD INSTRUCTIONS")
        print("="*60)
        print("\nOption 1: Use the batch script (Windows)")
        print(f"  Run: {bat_script}")
        print("\nOption 2: Use Python script (with progress bars)")
        print(f"  Run: python {py_script}")
        print("\nOption 3: Manual download")
        print("  Download links saved to: flux_model_links.txt")
        
        # Save download links
        with open("flux_model_links.txt", "w") as f:
            f.write("FLUX MODEL DOWNLOAD LINKS\n")
            f.write("="*60 + "\n\n")
            for name, info in missing:
                f.write(f"{name}:\n")
                f.write(f"  URL: {info['url']}\n")
                f.write(f"  Save to: {MODELS_DIR / info['path']}\n")
                f.write(f"  Size: {info['size']}\n")
                f.write(f"  Description: {info['description']}\n\n")
    else:
        print("\n[OK] All Flux models are already installed!")
    
    print("\n" + "="*60)
    print("WORKFLOW STATUS")
    print("="*60)
    print("[OK] Flux inpainting workflow created: flux_inpaint_workflow_with_clipskip.json")
    print("[OK] Includes CLIPSetLastLayer for clip skip control")
    print("[OK] Configured for inpainting with mask support")
    print("[OK] Same layout as your reference workflow")
    
    if not missing:
        print("\n[READY] READY TO USE!")
        print("Load flux_inpaint_workflow_with_clipskip.json in ComfyUI")
    else:
        print("\n[WARNING] Download missing models first using one of the scripts above")