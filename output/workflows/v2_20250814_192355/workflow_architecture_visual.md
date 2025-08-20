# SDXL Advanced Multi-Detail Enhancement Workflow Architecture

## Visual Layout (Left to Right Flow)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA BUS: MODEL (y: -200)                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                               DATA BUS: CLIP (y: -100)                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

   FOUNDATION          GENERATION         ENHANCEMENT          REFINEMENT         OUTPUT
   (x: 0-800)         (x: 1000-1600)     (x: 1800-2800)      (x: 3000-3600)    (x: 3800-4400)
   [BLUE]             [GREEN]            [PURPLE]             [ORANGE]          [RED]
   
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Checkpoint  │    │  KSampler   │    │ ADetailer   │    │  Upscale    │    │   Save      │
│  Loader     │───▶│   (Base)    │───▶│   (Face)    │    │   Model     │    │   Final     │
├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤
│ LoRA        │    │ VAE Decode  │    │  Preview    │    │  Image      │    │   Save      │
│ Stacker     │    │             │    │   (Face)    │    │  Upscale    │    │Intermediate │
├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤    └─────────────┘
│ CLIP Text   │    │  Preview    │    │ ADetailer   │    │  Image      │
│ Encode (+)  │    │   (Base)    │    │   (Nose)    │    │  Scale By   │
├─────────────┤    └─────────────┘    ├─────────────┤    ├─────────────┤
│ CLIP Text   │                       │  Preview    │    │  Preview    │
│ Encode (-)  │                       │   (Nose)    │    │ (Upscaled)  │
├─────────────┤                       ├─────────────┤    └─────────────┘
│Empty Latent │                       │ ADetailer   │           │
│   Image     │                       │   (Tits)    │           │
├─────────────┤                       ├─────────────┤           ▼
│ Primitive   │                       │  Preview    │    ┌─────────────┐
│ (Seed)      │                       │   (Tits)    │    │   VIDEO     │
├─────────────┤                       ├─────────────┤    │  BRANCH     │
│ Primitive   │                       │ ADetailer   │    │   [CYAN]    │
│ (Steps)     │                       │   (Ass)     │    ├─────────────┤
├─────────────┤                       ├─────────────┤    │SVD Img2Vid  │
│ Primitive   │                       │  Preview    │    │Conditioning │
│ (CFG)       │                       │   (Ass)     │    ├─────────────┤
└─────────────┘                       ├─────────────┤    │  KSampler   │
                                     │ ADetailer   │    │  (Video)    │
                                     │   (Feet)    │    ├─────────────┤
                                     ├─────────────┤    │ VAE Decode  │
                                     │  Preview    │    │   Video     │
                                     │   (Feet)    │    ├─────────────┤
                                     └─────────────┘    │Video Combine│
                                                        ├─────────────┤
                                                        │  Preview/   │
                                                        │Save Video   │
                                                        └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               DATA BUS: VAE (y: 1700)                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Key Architecture Features

### 1. Vertical Pillar Organization
- **Foundation Pillar**: All input and model loading components
- **Generation Pillar**: Base image generation
- **Enhancement Pillar**: Multi-region detail enhancement (vertical stack)
- **Refinement Pillar**: Upscaling operations
- **Output Pillar**: Save operations
- **Extension Pillar**: Video generation branch (offset below main flow)

### 2. Data Bus Implementation
- **MODEL Bus**: Carries model data across all processing stages
- **CLIP Bus**: Distributes text conditioning
- **VAE Bus**: Shares VAE decoder across stages

### 3. Progressive Enhancement Flow
1. Base generation at standard resolution
2. Sequential detail enhancement (Face → Nose → Tits → Ass → Feet)
3. Final upscaling
4. Optional video generation branch

### 4. Preview Points
- After base generation
- After each detail enhancement
- After upscaling
- Video preview

### 5. Efficiency Features
- LoRA stacker for batch processing
- Shared resources via data buses
- Modular design for easy modification
- Conditional branches (video can be disabled)

## Color Coding Schema
- **Blue**: Input/Foundation components
- **Green**: Generation components
- **Purple**: Enhancement components
- **Orange**: Refinement components
- **Red**: Output components
- **Cyan**: Extension/Video components

## Spacing Guidelines
- Intra-group spacing: 60px
- Inter-group spacing: 200px
- Pillar spacing: 900px
- Vertical stack spacing: 300px (for detailers)
- Grid alignment: 20px