# FLUX Model Download Guide

## Required Models and Their Locations

### 1. FLUX UNET Model
**File:** `flux1-dev.safetensors` (or `flux1-schnell.safetensors`)
**Location:** `ComfyUI/models/unet/`
**Download:** 
- FLUX Dev: https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors
- FLUX Schnell (faster): https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/flux1-schnell.safetensors

### 2. Text Encoders (CLIP Models)
**Files:** 
- `t5xxl_fp8_e4m3fn.safetensors` (lower memory)
- `clip_l.safetensors`
**Location:** `ComfyUI/models/clip/`
**Download:**
- T5-XXL: https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors
- CLIP-L: https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors

### 3. VAE Model
**File:** `ae.safetensors`
**Location:** `ComfyUI/models/vae/`
**Download:** https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/ae.safetensors

### 4. Upscale Model
**File:** `4x-UltraSharp.pth`
**Location:** `ComfyUI/models/upscale_models/`
**Download:** https://huggingface.co/Kim2091/UltraSharp/blob/main/4x-UltraSharp.pth

## Quick Download Commands (Windows PowerShell)

```powershell
# Create directories if they don't exist
mkdir -p ComfyUI/models/unet
mkdir -p ComfyUI/models/clip
mkdir -p ComfyUI/models/vae
mkdir -p ComfyUI/models/upscale_models

# Download FLUX Dev model (choose one)
wget https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors -OutFile ComfyUI/models/unet/flux1-dev.safetensors

# Download text encoders
wget https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors -OutFile ComfyUI/models/clip/t5xxl_fp8_e4m3fn.safetensors
wget https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors -OutFile ComfyUI/models/clip/clip_l.safetensors

# Download VAE
wget https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors -OutFile ComfyUI/models/vae/ae.safetensors

# Download upscale model
wget https://huggingface.co/Kim2091/UltraSharp/resolve/main/4x-UltraSharp.pth -OutFile ComfyUI/models/upscale_models/4x-UltraSharp.pth
```

## Alternative: Using HuggingFace CLI

```bash
# Install huggingface-hub
pip install huggingface-hub

# Download models
huggingface-cli download black-forest-labs/FLUX.1-dev flux1-dev.safetensors --local-dir ComfyUI/models/unet
huggingface-cli download comfyanonymous/flux_text_encoders t5xxl_fp8_e4m3fn.safetensors --local-dir ComfyUI/models/clip
huggingface-cli download comfyanonymous/flux_text_encoders clip_l.safetensors --local-dir ComfyUI/models/clip
huggingface-cli download black-forest-labs/FLUX.1-dev ae.safetensors --local-dir ComfyUI/models/vae
```

## Model Sizes
- FLUX Dev UNET: ~23.8 GB
- T5-XXL (fp8): ~4.9 GB  
- CLIP-L: ~246 MB
- VAE: ~335 MB
- 4x-UltraSharp: ~67 MB

**Total Required:** ~29.3 GB disk space

## Memory Requirements
- Minimum: 12GB VRAM (with fp8 quantization)
- Recommended: 24GB VRAM
- For best quality: Use fp16 versions instead of fp8