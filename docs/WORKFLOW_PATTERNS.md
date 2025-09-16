# ComfyUI Workflow Patterns Reference

## Purpose
This document captures successful patterns and techniques for ComfyUI workflow generation and modification.

---

## Workflow Extraction Patterns

### PNG Metadata Extraction
**Pattern**: Extract embedded workflows from ComfyUI-generated PNG files
**Implementation**:
```python
def extract_workflow_from_png(png_path):
    # Read PNG chunks
    # Find tEXt chunk with keyword "workflow"
    # Parse JSON and return workflow
```
**Use Cases**:
- User provides screenshot with embedded workflow
- Recovering workflows from generated images
- Analyzing community workflows

### Workflow Validation
**Pattern**: Validate extracted workflows before modification
**Checks**:
- Node type identification (CheckpointLoaderSimple, LoraLoader, etc.)
- Widget values inspection (model names, settings)
- Layout metadata verification (pos, size, groups)

---

## Node Integration Patterns

### CLIPSetLastLayer (Clip Skip) Integration
**Pattern**: Insert clip skip functionality without disrupting layout
**Steps**:
1. Identify CLIP flow: Source → Text Encoders
2. Find clear space between groups (typically 250-500px spacing)
3. Insert CLIPSetLastLayer node
4. Update connections:
   - Redirect CLIP output to CLIPSetLastLayer
   - Connect CLIPSetLastLayer to all text encoders
5. Preserve all existing positions

**Example Position Calculation**:
```python
# Position between Lora Stack and Conditioning
clipskip_pos = [
    lora_stack_x + lora_stack_width + 50,  # 50px gap
    (lora_stack_y + conditioning_y) / 2    # Vertically centered
]
```

**Default Settings**:
- stop_at_clip_layer: -2 (common default)
- Range: -1 to -12 (model dependent)

### Reroute Node Patterns
**Pattern**: Use reroute nodes as data buses
**Implementation**:
- VAE Bus: Central distribution of VAE connections
- Model Bus: Distribute model to multiple samplers
- CLIP Bus: Distribute CLIP to multiple encoders
**Properties**:
```json
{
    "title": "VAE Bus",
    "properties": {
        "showOutputText": false,
        "horizontal": true
    }
}
```

---

## Layout Preservation Patterns

### Node Position Management
**Pattern**: Maintain exact positions during modifications
**Rules**:
1. Never change existing node positions unless requested
2. Find clear spaces for new nodes
3. Respect group boundaries
4. Maintain visual flow (left-to-right typical)

### Group Management
**Pattern**: Preserve group structure and styling
**Properties to Maintain**:
- `bounding`: [x, y, width, height] (NOT "bounding_box")
- `color`: Preserve exact color codes
- `font_size`: Maintain consistency (usually 24)
- `title`: Keep descriptive names

### Link Management
**Pattern**: Proper link array updates
**Structure**: `[link_id, source_node, source_slot, target_node, target_slot, "TYPE"]`
**Update Process**:
1. Increment last_link_id for new links
2. Update source node's output links array
3. Update target node's input link reference
4. Add new link to links array

---

## Model-Specific Patterns

### Pony Model Workflows
**Characteristics**:
- Multiple Lora Stack nodes (rgthree)
- Wildcard processors for prompt variation
- Specific score tags in prompts
- Usually SDXL-based

**Typical Flow**:
```
Checkpoint → Lora Stack 1 → Lora Stack 2 → [CLIPSetLastLayer] → Text Encoders → Sampler
```

### Flux Model Workflows
**Characteristics**:
- UNETLoader with fp8_e4m3fn weight dtype
- DualCLIPLoader (clip_l + t5xxl)
- ModelSamplingFlux node
- Separate VAE loading (ae.safetensors)

**Typical Settings**:
- Guidance: 3.0-3.5
- Max shift: 1.15
- Base shift: 0.5

### SDXL Workflows
**Characteristics**:
- Standard CheckpointLoaderSimple
- SDXL-specific VAE (sdxl_vae.safetensors)
- Resolution: 1024x1024 base
- Often includes refiner model

---

## Workflow Modification Patterns

### Adding Features to Existing Workflows
**Pattern**: Layer new features without disrupting existing functionality
**Process**:
1. Load and analyze current workflow
2. Identify integration points
3. Find clear space for new nodes
4. Add nodes with minimal link changes
5. Preserve all existing features

### Safe Modification Script Pattern
**Template**:
```python
import json

# Load workflow
with open("workflow.json", 'r') as f:
    workflow = json.load(f)

# Track IDs
last_node_id = workflow.get("last_node_id", 0)
last_link_id = workflow.get("last_link_id", 0)

# Add new node
new_node = {
    "id": last_node_id + 1,
    "type": "NodeType",
    "pos": [x, y],
    "size": [width, height],
    # ... node configuration
}

# Update workflow
workflow["nodes"].append(new_node)
workflow["last_node_id"] = last_node_id + 1

# Save with new name
with open("workflow_modified.json", 'w') as f:
    json.dump(workflow, f, indent=2)
```

---

## Professional Layout Standards

### Spacing Guidelines
**Minimum Spacing**:
- Between groups: 100px minimum, 400px+ preferred
- Between nodes in group: 50px horizontal, 30px vertical
- From group edge: 35px (accounts for header)

**Professional Spacing** (Complex Workflows):
- Major group separation: 1500-2000px horizontal
- Vertical group spacing: 250px minimum
- Data bus lanes: 100px dedicated space

### Visual Organization
**Left-to-Right Flow**:
1. Input/Loading (leftmost)
2. Processing/Conditioning
3. Generation/Sampling
4. Post-processing
5. Output/Save (rightmost)

**Vertical Arrangement**:
- Primary flow: Middle horizontal band
- Utilities: Top or bottom
- Reroutes/Buses: Clear lanes between groups

---

## Common Integration Points

### CLIP Pipeline
**Integration Points**:
1. After CheckpointLoader CLIP output
2. After Lora Stack CLIP output
3. Before Text Encoder inputs
4. Between CLIP processors

### Model Pipeline
**Integration Points**:
1. After CheckpointLoader MODEL output
2. After Lora loaders
3. Before/After ModelSampling nodes
4. Before Sampler model input

### VAE Pipeline
**Integration Points**:
1. After VAE Loader
2. Before VAE Decode
3. Before VAE Encode
4. At reroute/bus nodes

---

## Debugging Patterns

### Connection Verification
**Check List**:
- All node inputs have valid links
- Output links array matches actual connections
- Link types match (MODEL, CLIP, VAE, etc.)
- No orphaned links in links array

### Common Issues and Fixes
1. **Missing Connections**: Check link IDs match
2. **Wrong Property Names**: "bounding" not "bounding_box"
3. **Invalid Node IDs**: Ensure unique, incremental IDs
4. **Type Mismatches**: Verify connection compatibility

---

## Script Utilities

### Workflow Analysis
```python
def analyze_workflow(workflow):
    """Analyze workflow structure"""
    return {
        "node_count": len(workflow.get("nodes", [])),
        "link_count": len(workflow.get("links", [])),
        "group_count": len(workflow.get("groups", [])),
        "node_types": list(set(n["type"] for n in workflow.get("nodes", []))),
        "has_clip_skip": any(n["type"] == "CLIPSetLastLayer" for n in workflow.get("nodes", []))
    }
```

### Safe Node Addition
```python
def add_node_safely(workflow, node_type, position, connections):
    """Add node with proper ID management"""
    new_id = workflow.get("last_node_id", 0) + 1
    # Create node with new_id
    # Update connections
    # Update last_node_id
    return workflow
```

---

*Last Updated: 2025-01-31*
*Version: 1.0.0*