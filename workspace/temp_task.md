# Task: Parameter Extraction for Flux ADetailer ClipSkip Workflow

## Source Context
Building upon existing v3 Flux Ultimate workflow (42 nodes) from:
`C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\output\workflows\v3_20250827_163000_flux_ultimate\flux_ultimate_42_nodes_workflow.json`

## NEW FEATURES TO ADD:
1. **CLIPSetLastLayer** for clip skip control (-1 to -12)
2. **ADetailer** with FaceDetailer using face_yolov8m.pt
3. **Ultimate SD Upscale** with 4x-UltraSharp.pth
4. **Multi-pass rendering** (base -> upscale -> hi-res fix)
5. **Professional layout** from 4.5 ultimate pattern (1500-2000px spacing)

## Available Models (verified):
- FLUX: flux1-dev-fp8.safetensors
- CLIP: clip_l.safetensors, t5xxl_fp8_e4m3fn.safetensors  
- VAE: ae.safetensors
- Detection: face_yolov8m.pt, hand_yolov8s.pt (in ultralytics/bbox/)
- Upscale: 4x-UltraSharp.pth, RealESRGAN_x2.pth

## Workflow Structure Required:
- Base generation at 1024x1024
- Face detection and enhancement via ADetailer
- 2x upscale with model
- Hi-res fix pass with 0.3 denoise
- Separate outputs for each stage
- Power Lora Loader as central hub

## Output Format:
Frontend/UI format with full visual metadata including positions, sizes, widgets_values

## Critical Requirement:
MAINTAIN ALL EXISTING FEATURES from v3 workflow and ADD these new features on top.