# FLUX Workflow Success Notes
Date: 2025-08-31
User Feedback: "THAT LAST WORKFLOW WAS GREAT"

## What Made This FLUX Workflow Awesome

### 1. PROPER FLUX ARCHITECTURE ✅
- **UNETLoader** with `fp8_e4m3fn` weight dtype (memory efficient)
- **DualCLIPLoader** with both `clip_l` and `t5xxl_fp8`
- **VAELoader** with `ae.safetensors`
- **ModelSamplingFlux** with correct shift values (1.15, 0.5)

### 2. DOUBLE UPSCALING FOR 4K OUTPUT ✅
- **Stage 1**: Ultimate SD Upscale (2x with tiling)
- **Stage 2**: ImageUpscaleWithModel (2x with RealESRGAN)
- **Result**: 1024 → 2048 → 4096 pixels!

### 3. FLUX-OPTIMIZED SETTINGS ✅
- **Low CFG**: 1.0 (FLUX doesn't need high CFG)
- **Euler sampling**: Simple and effective
- **20 steps**: Sufficient for FLUX
- **Guidance**: 3.5 in CLIPTextEncodeFlux

### 4. QUALITY ENHANCEMENTS ✅
- **FreeU_V2**: Boosts quality without extra computation
- **Power LoRA Loader**: Ready for LoRAs (disabled by default)
- **Ultimate SD Upscale**: Chess tiling for seamless upscaling

### 5. CLEAN WORKFLOW DESIGN ✅
- Clear note at top explaining purpose
- Logical left-to-right flow
- Semantic groups with proper colors
- Fast Groups Bypasser for feature control
- Reroute for clean CLIP distribution

## The Winning Formula

```
FLUX fp8 + Ultimate SD Upscale + Extra 2x Upscale = Professional 4K Output
```

## Key Parameters That Work

- **Model**: flux1-dev-fp8.safetensors
- **Sampling**: euler, simple scheduler
- **Steps**: 20 base, 20 upscale
- **CFG**: 1.0 (low for FLUX)
- **Denoise**: 0.2 for upscaling
- **Tile Size**: 1024x1024 for Ultimate SD

## What NOT to Do
- Don't use high CFG (FLUX prefers 1.0-2.0)
- Don't skip ModelSamplingFlux (required for FLUX)
- Don't use regular CLIPTextEncode (use CLIPTextEncodeFlux)
- Don't forget the double upscaling for true 4K

## User Quote
> "THAT LAST WORKFLOW WAS GREAT"

This is the template to follow for future FLUX workflows!