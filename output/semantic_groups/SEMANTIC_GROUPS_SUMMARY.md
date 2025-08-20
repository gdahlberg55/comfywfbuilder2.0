# Outfit Variation Workflow - Semantic Groups Summary

## Overview
This document outlines the semantic grouping strategy for the outfit variation workflow, organizing 77 nodes into 9 logical groups following the ComfyUI Gold Standard.

## Group Structure

### 🟢 (0) Model & Resource Loaders
- **Color**: `#355335` (Dark Green)
- **Position**: X: 0-2000, Y: -2200 to 600
- **Purpose**: Initialize all base models, CLIP, VAE, and vision models
- **Nodes**: 6 nodes including UnetLoader, CLIPLoader, VAELoader, CLIPVisionLoader

### 🟢 (1) LoRA Application Chain  
- **Color**: `#355335` (Dark Green)
- **Position**: X: 2500-6500, Y: -2200 to -1000
- **Purpose**: Sequential LoRA model application for outfit variations
- **Nodes**: 3 nodes for LoRA loading and patching

### 🔵 (2) Text Encoding & Conditioning
- **Color**: `#353553` (Dark Blue)
- **Position**: X: 7000-11000, Y: -1600 to 600
- **Purpose**: Process prompts and create positive/negative conditioning
- **Nodes**: 5 nodes including CLIPTextEncode, CFGGuider

### 🟣 (3) Image Preparation & Masking
- **Color**: `#453553` (Dark Purple)
- **Position**: X: 11500-15500, Y: -1200 to 1200
- **Purpose**: Prepare input images, apply masks, resize and crop
- **Nodes**: 6 nodes for image processing

### 🟠 (4) Seeds & Control Parameters
- **Color**: `#534535` (Dark Orange)
- **Position**: X: 16000-20000, Y: -800 to 1600
- **Purpose**: Control parameters, seeds, and variation settings
- **Nodes**: 6 nodes including sliders and math expressions

### 🔴 (5) Sampling & Generation
- **Color**: `#533535` (Dark Red)
- **Position**: X: 20500-24500, Y: -1600 to 800
- **Purpose**: Core image generation and sampling operations
- **Nodes**: 9 nodes including KSampler, VAEDecode

### 🩷 (6) Video Enhancement & Combination
- **Color**: `#533545` (Dark Pink)
- **Position**: X: 25000-29000, Y: -1200 to 1200
- **Purpose**: Video processing, frame interpolation, enhancement
- **Nodes**: 9 nodes for video operations

### 🟦 (7) Preview & Save Operations
- **Color**: `#355353` (Dark Teal)
- **Position**: X: 29500-32500, Y: -800 to 1600
- **Purpose**: Final outputs, previews, and save operations
- **Nodes**: 8 nodes for output handling

### ⬛ (8) Workflow Documentation
- **Color**: `#444444` (Dark Gray)
- **Position**: X: 33000-40000, Y: -2200 to 2200
- **Purpose**: Notes and documentation for workflow usage
- **Nodes**: 16 documentation notes

## Data Bus Lane Organization

The workflow uses horizontal data bus lanes for clean routing:

1. **MODEL Bus** (Y: -2000) - Pink `#FFB6C1`
2. **CLIP Bus** (Y: -1600) - Mint `#98D8C8`
3. **VAE Bus** (Y: -1200) - Yellow `#F7DC6F`
4. **IMAGE Bus** (Y: -800) - Purple `#BB8FCE`
5. **LATENT Bus** (Y: -400) - Blue `#85C1E2`
6. **CONDITIONING Bus** (Y: 0) - Orange `#F8C471`

## Key Features

- **2000px horizontal spacing** between major stages
- **400px vertical spacing** for clarity
- **120px group padding** for visual breathing room
- **Orthogonal routing** with data buses
- **Color-coded by function** following COLOR_SCHEME.md
- **Numbered stage titles** for clear workflow progression

## Benefits

1. **Clear Visual Hierarchy**: Stages progress left-to-right
2. **Easy Navigation**: Color coding and numbering guide users
3. **Reduced Clutter**: Data buses eliminate crossing connections
4. **Professional Appearance**: Consistent spacing and alignment
5. **Collapsible Groups**: Can be collapsed for overview or expanded for detail

## Implementation Notes

- All groups use `bounding` property (not `bounding_box`)
- Colors strictly follow COLOR_SCHEME.md
- Groups are non-overlapping with proper collision detection
- Supports workflow spans up to 40,000px horizontal
- Compatible with ComfyUI's group collapse feature