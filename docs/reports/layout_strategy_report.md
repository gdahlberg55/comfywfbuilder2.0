# Engineering-Style Layout Strategy for ComfyUI Workflow

## Analysis Summary

The workflow "Wan 2.1 - seamless loop workflow v1.2" is a complex video generation pipeline with:
- **77 nodes** spanning 6750px horizontally
- **90 connections** across 6 major data types
- **7 processing stages** from input to output

## Recommended Layout Parameters

### 1. Horizontal Spacing: **1500px**
- Based on the current workflow spanning 6750px with scattered nodes
- Provides ample room for straight-line routing channels
- Allows clear visual separation between processing stages

### 2. Data Bus Lane Definitions

| Data Type | Routing Channel Y | Color | Priority | Line Width |
|-----------|------------------|-------|----------|------------|
| MODEL | -2600 | #FF6B6B | 1 | 3px |
| CLIP | -2580 | #4ECDC4 | 2 | 2px |
| VAE | -2560 | #45B7D1 | 3 | 2px |
| CONDITIONING | -2540 | #96CEB4 | 4 | 2px |
| LATENT | -2520 | #DDA0DD | 5 | 2px |
| IMAGE | -2500 | #FFD93D | 6 | 3px |

### 3. Node Positioning Strategy

**Processing Stages:**
1. **Input/Loaders** (X=-2000): Model, CLIP, VAE loaders
2. **Model Enhancement** (X=-1000): LoRA application, sampling config
3. **Conditioning** (X=0): Text encoding, image encoding
4. **Sampling** (X=1500): KSampler nodes, noise generation
5. **Decode/Process** (X=3000): VAE decode, color correction
6. **Interpolation** (X=4500): Frame interpolation, batching
7. **Output** (X=6000): Video combine, preview

**Vertical Organization:**
- Primary flow nodes: Centered at Y=-1700
- Secondary nodes: Offset ±200px
- Control nodes: Top row at Y=-2200
- Utility nodes: Bottom row at Y=-1000

### 4. Routing Channel Layout

**Engineering-Style Straight-Line Routing:**

```
Node Output → ↓ → Routing Channel → → → → ↑ → Target Input
                  ═══════════════════════
```

**Nested Channel Structure:**
- Primary buses: Y=-2600 to -2500 (20px separation)
- Secondary connections: Direct L-shaped routes
- Breakout angles: Always 90 degrees
- Minimum parallel separation: 40px

**Connection Rules:**
1. **Long-distance connections** (>3000px): Use dedicated routing channels
2. **Medium connections** (1000-3000px): L-shaped direct routing
3. **Short connections** (<1000px): Straight horizontal lines
4. **Vertical stacking**: When multiple connections overlap, stack with 20px gaps

### 5. Implementation Guidelines

1. **Exit/Entry Points:**
   - Nodes exit from bottom edge for bus connections
   - Enter from bottom edge for bus connections
   - Use side connections for local links

2. **Channel Assignment:**
   - Assign by connection length (longer = lower channel)
   - Group similar data types in adjacent channels
   - Maintain consistent color coding

3. **Visual Hierarchy:**
   - Primary data flow: 3px solid lines
   - Secondary connections: 2px solid lines
   - Utility connections: 1px dashed lines

4. **Grid Alignment:**
   - All positions snap to 20px grid
   - Routing channels aligned to grid
   - 90-degree turns only

This engineering approach eliminates the "spaghetti" effect of spline routing and creates a clean, professional layout that clearly shows data flow and processing stages.