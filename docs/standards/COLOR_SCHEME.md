# ComfyUI Workflow Color Scheme Reference

This document defines the standard color scheme for organizing ComfyUI workflows into logical groups.

## Node Group Colors

### 1. Loaders (Green)
- **Color**: `#355335` (Dark Green)
- **Nodes**: CheckpointLoaderSimple, VAELoader, LoraLoader, CLIPLoader
- **Purpose**: Model and resource loading

### 2. Conditioning (Blue)
- **Color**: `#353553` (Dark Blue)
- **Nodes**: CLIPTextEncode, ConditioningCombine, ConditioningSetArea
- **Purpose**: Prompt encoding and conditioning manipulation

### 3. Sampling (Red)
- **Color**: `#533535` (Dark Red)
- **Nodes**: KSampler, KSamplerAdvanced, SamplerCustom
- **Purpose**: Image generation and sampling processes

### 4. Latent Operations (Yellow)
- **Color**: `#535335` (Dark Yellow/Olive)
- **Nodes**: VAEEncode, VAEDecode, LatentUpscale, EmptyLatentImage
- **Purpose**: Latent space operations and transformations

### 5. Post-Processing (Purple)
- **Color**: `#453553` (Dark Purple)
- **Nodes**: ImageUpscaleWithModel, ImageScale, ImageComposite
- **Purpose**: Image enhancement and post-processing

### 6. Utility (Black/Dark Gray)
- **Color**: `#444444` (Dark Gray)
- **Nodes**: PrimitiveNode, Note, Reroute, IntegerInput
- **Purpose**: Helper nodes and workflow organization

## Additional Color Guidelines

### Control Networks (Orange)
- **Color**: `#534535` (Dark Orange)
- **Nodes**: ControlNetApply, ControlNetLoader
- **Purpose**: ControlNet operations

### Image Input/Output (Teal)
- **Color**: `#355353` (Dark Teal)
- **Nodes**: LoadImage, SaveImage, PreviewImage
- **Purpose**: Image I/O operations

### Custom Nodes (Pink)
- **Color**: `#533545` (Dark Pink)
- **Nodes**: Third-party and custom nodes
- **Purpose**: Extended functionality

## Visual Hierarchy

1. **Primary Flow**: Loaders → Conditioning → Sampling → Latent → Output
2. **Secondary Elements**: Utilities, Controls, Reroutes
3. **Grouping**: Related nodes should be grouped with 50px padding
4. **Spacing**: Maintain 80px minimum between groups

## Accessibility Notes

- All colors chosen for sufficient contrast
- Group titles should be in white text
- Font size: 24px for group titles
- Add descriptive labels for color-blind users