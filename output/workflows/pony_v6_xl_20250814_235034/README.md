# Pony Diffusion V6 XL Optimized Workflow

## Overview
This is a comprehensive, performance-optimized workflow for Pony Diffusion V6 XL designed to complete generation within 6 minutes on standard hardware (8GB VRAM GPU).

## Key Features
- **6 LoRA Chain Support** - Maximum flexibility with independent strength controls
- **CLIP Skip -2** - Essential for optimal Pony V6 XL results
- **Quality Tags** - Proper score_9 through score_4_up formatting
- **FaceDetailer** - Automatic face enhancement with minimal overhead
- **UltimateSDUpscale** - Efficient 1.5x upscaling with tiling
- **IPAdapter Support** - Optional reference image styling
- **Optimized Settings** - 25 steps, CFG 5, DPM++ 2M Karras

## Performance Optimizations
- Resolution: 896x1152 (optimal for Pony V6 XL)
- Steps: 25 (balanced quality/speed)
- Sampler: DPM++ 2M Karras (efficient high-quality)
- Face Detail: 10 steps only
- Upscale: 1.5x with 8 steps (minimal overhead)

## Model & File Placement

### Base Model
Place in `ComfyUI/models/checkpoints/`:
- `ponyDiffusionV6XL_v6StartWithThisOne.safetensors`

### LoRAs
Place in `ComfyUI/models/loras/`:
- Style LoRAs (0.7-1.0 strength recommended)
- Character LoRAs (0.5-0.8 strength)
- Concept LoRAs (0.4-0.6 strength)

### Optional IPAdapter
Place in `ComfyUI/models/ipadapter/`:
- `ip-adapter-plus_sdxl_vit-h.safetensors`

Place in `ComfyUI/models/clip_vision/`:
- `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`

## Prompt Best Practices

### Required Quality Tags (Always Start With)
```
score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up
```

### Structure
1. Quality tags (required)
2. Source tag: `source_anime`, `source_pony`, `source_cartoon`, `source_furry`
3. Rating tag: `rating_safe`, `rating_questionable`, `rating_explicit`
4. Subject: `1girl`, `1boy`, `2girls`, etc.
5. Appearance: hair color, eye color, clothing
6. Expression/pose
7. Background/environment
8. Style modifiers

### Example Prompt
```
score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, source_anime, rating_safe, 1girl, white hair, blue eyes, (detailed face:1.2), school uniform, cherry blossoms, soft lighting
```

## Speed Optimization Tips

### To Reduce Generation Time:
1. **Disable Face Detailer** - Set mode to 2 (bypass) saves ~30 seconds
2. **Skip Upscaling** - Disconnect UltimateSDUpscale saves ~1 minute
3. **Reduce Steps** - Lower to 20 steps (minimal quality loss)
4. **Lower Resolution** - Use 768x1024 for faster generation
5. **Fewer LoRAs** - Each LoRA adds ~5-10 seconds

### To Add More Features:
1. **More LoRAs** - Copy any LoraLoader node and chain it
2. **ControlNet** - Add ControlNetLoader + ApplyControlNet before KSampler
3. **Refiner Pass** - Duplicate KSampler with 0.3 denoise after decode
4. **AnimateDiff** - Insert motion module loader after LoRA chain

## Workflow Groups
- **Model Loading & LoRA Chain** - Blue group with checkpoint and 6 LoRAs
- **Conditioning** - Purple group with positive/negative prompts
- **Sampling** - Orange group with main generation
- **Post-Processing** - Brown group with face detail and upscale
- **Optional IPAdapter** - Gray group for style transfer

## Hardware Requirements
- Minimum: 8GB VRAM (GTX 1080, RTX 3060)
- Recommended: 12GB+ VRAM for batch size >1
- RAM: 16GB minimum, 32GB recommended

## Troubleshooting
- **Out of Memory**: Reduce resolution or disable upscaling
- **Slow Generation**: Check CLIP skip is -2, reduce steps to 20
- **Poor Quality**: Ensure quality tags are present, increase CFG to 7

## Credits
Workflow designed for ComfyUI with Pony Diffusion V6 XL optimization