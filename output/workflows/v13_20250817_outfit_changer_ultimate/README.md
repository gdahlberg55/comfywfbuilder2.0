# Outfit Changer Ultimate Workflow

## Overview
The **Outfit Changer Ultimate** workflow represents the pinnacle of outfit transformation technology in ComfyUI, combining FLUX model architecture with professional workflow organization standards.

## Version Information
- **Version**: v13_20250817
- **Architecture**: FLUX-based
- **Node Count**: 28 optimized nodes
- **Spacing Standard**: 70px grid with 150px section gaps

## Key Features

### 🎯 Core Capabilities
- **FLUX Model Integration**: Latest FLUX Dev FP8 for superior quality
- **Dual CLIP Encoding**: Combined clip_l and t5xxl for enhanced understanding
- **Power LoRA Stack**: 3-slot dynamic LoRA management
- **Pose Preservation**: ControlNet-based pose maintenance
- **Wildcard System**: Automatic outfit variation generation

### 📐 Professional Organization
- **6 Semantic Groups**: Logical workflow sections
- **Consistent Spacing**: 70px grid alignment
- **Left-to-Right Flow**: Natural progression
- **Color-Coded Sections**: Visual clarity

### 🚀 Advanced Features
- **Masked Compositing**: Preserve original image areas
- **AI Upscaling**: 4x quality enhancement
- **Guidance Control**: Fine-tuned generation parameters
- **Resolution Flexibility**: 1024x1024 base resolution

## Workflow Structure

```
[Model Loading] → [Input Processing] → [Text Conditioning] → 
[FLUX Generation] → [Sampling] → [Output & Save]
```

### Group Organization:
1. **Model & LoRA Loading** (Blue) - Base models and enhancements
2. **Input Processing** (Orange) - Image inputs and references
3. **Text Conditioning** (Green) - Prompt engineering
4. **FLUX Generation** (Purple) - Core generation pipeline
5. **Sampling & Processing** (Violet) - Image generation
6. **Output & Save** (Brown) - Final processing and export

## Required Components

### Models
- `flux1-dev-fp8.safetensors` - Main FLUX model
- `clip_l.safetensors` - CLIP text encoder
- `t5xxl_fp16.safetensors` - T5 text encoder
- `ae.safetensors` - VAE model

### Optional LoRAs
- `outfit_transformer_flux.safetensors` - Outfit transformation
- `clothing_detail_flux.safetensors` - Detail enhancement
- `style_transfer_flux.safetensors` - Style control

### Custom Nodes
- rgthree-comfy (Power LoRA Loader)
- ComfyUI-Impact-Pack (Wildcard Processor)

## Usage Instructions

### Quick Start
1. Load `outfit_changer_ultimate.json` in ComfyUI
2. Place your person image in node (5)
3. Add outfit reference in node (6)
4. Customize outfit description in node (10)
5. Queue prompt to generate

### Parameter Tuning
- **Seed** (Node 7): Control randomization
- **Steps** (Node 8): 20-30 recommended
- **Guidance** (Node 9): 3.5 default, 2-5 range
- **LoRA Strength**: Adjust in node (4)

### Optimization Tips
- Start with 20 steps for testing
- Disable upscaling for previews
- Use wildcards for batch variations
- Adjust ControlNet strength for pose flexibility

## Performance Specifications

| Metric | Value |
|--------|-------|
| VRAM Usage | 12-16GB |
| Generation Time | 30-60 seconds |
| Quality | Professional |
| Stability | High |

## Comparison with Previous Versions

| Feature | v12 Pro | v11 FLUX | v13 Ultimate |
|---------|---------|----------|--------------|
| Model | SD 1.5 | FLUX | FLUX Optimized |
| Nodes | 29 | 30 | 28 |
| Spacing | Variable | Dense | 70px Standard |
| Groups | 6 | 6 | 6 Optimized |
| Quality | Good | Better | Best |

## Troubleshooting

### Common Issues
1. **Out of Memory**: Reduce batch size or use CPU offloading
2. **Slow Generation**: Enable xformers or SageAttention
3. **Poor Quality**: Check model paths and increase steps
4. **Wrong Outfit**: Adjust LoRA strengths and prompts

### Support
For issues or improvements, check:
- KNOWN_ISSUES_TRACKER.md
- docs/protocols/WORKFLOW_ERRORS.md

## Credits
Created with ComfyUI Agentic Workflow Generator v2.0
Based on analysis of multiple workflow versions for optimal performance