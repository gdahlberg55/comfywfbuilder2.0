# FLUX NSFW Workflow - Model Requirements & Setup Guide

## Folder Structure Created ✅
```
C:\Users\gdahl\Documents\ComfyUI\models\
├── unet\           # FLUX UNET models
├── clip\           # CLIP text encoders
├── vae\            # VAE models (existing)
├── ultralytics\
│   └── bbox\       # Detection models for ADetailer
└── sams\           # SAM segmentation models
```

## Required Model Downloads

### 1. FLUX Core Models (ESSENTIAL)
Download from HuggingFace or CivitAI:

#### UNET Model (place in models/unet/)
- **File**: `flux1-dev-fp8.safetensors` (~11.9GB)
- **Source**: https://huggingface.co/black-forest-labs/FLUX.1-dev

#### CLIP Models (place in models/clip/)
- **File 1**: `clip_l.safetensors` (~246MB)
- **File 2**: `t5xxl_fp8_e4m3fn.safetensors` (~4.9GB)
- **Source**: https://huggingface.co/comfyanonymous/flux_text_encoders

#### VAE Model (place in models/vae/)
- **File**: `ae.safetensors` (~335MB)
- **Source**: https://huggingface.co/black-forest-labs/FLUX.1-dev

### 2. Detection Models for ADetailer (place in models/ultralytics/bbox/)
- **face_yolov8n.pt** - Face detection
- **hand_yolov8n.pt** - Hand detection
- **person_yolov8m-seg.pt** - Full body segmentation
- **eye_detect.pt** - Eye detection (if available)
- **mouth_detect.pt** - Mouth detection (if available)

**Source**: https://github.com/Bing-su/adetailer/releases

### 3. SAM Models (place in models/sams/)
- **sam_vit_b_01ec64.pth** (~375MB)
- **sam_vit_h_4b8939.pth** (~2.4GB)

**Source**: https://github.com/facebookresearch/segment-anything

### 4. Custom Node Installation Required
Install via ComfyUI Manager or git clone:

```bash
cd C:\Users\gdahl\Documents\ComfyUI\custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-Impact-Pack
```

## NSFW-Specific Recommendations

### Optional NSFW-Optimized Models
Consider these for better anatomical accuracy:
- **Breast/Nipple Detection Models**: Check specialized NSFW detection model repositories
- **NSFW LoRAs**: Place anatomical improvement LoRAs in models/loras/

### Workflow Will Use:
✅ **rgthree-comfy** - Already installed (Fast Groups Bypasser)
✅ **ComfyUI_UltimateSDUpscale** - Already installed
❌ **ComfyUI-Impact-Pack** - NEEDS INSTALLATION for ADetailer

## Quick Setup Commands

1. Create remaining directories:
```bash
mkdir -p "C:\Users\gdahl\Documents\ComfyUI\models\ultralytics\segm"
mkdir -p "C:\Users\gdahl\Documents\ComfyUI\models\controlnet"
```

2. After downloading models, verify:
```bash
ls -la "C:\Users\gdahl\Documents\ComfyUI\models\unet\"
ls -la "C:\Users\gdahl\Documents\ComfyUI\models\clip\"
ls -la "C:\Users\gdahl\Documents\ComfyUI\models\ultralytics\bbox\"
```

## Status Summary
- ✅ Folder structure created and organized
- ❌ FLUX models need to be downloaded
- ❌ Detection models need to be downloaded
- ❌ ComfyUI-Impact-Pack needs installation
- ✅ Other required custom nodes already present