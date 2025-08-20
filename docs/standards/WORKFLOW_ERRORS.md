# ComfyUI Workflow Common Errors & Solutions

## Error Log - FLUX Workflow Issues

### 1. TypeError: Cannot convert undefined or null to object
**Cause**: Invalid bounding box format in groups
- **Wrong**: `"bounding_box": [70, 70, 375, 418]`
- **Correct**: `"bounding": [70, 70, 375, 418]`

### 2. Missing slot_index in outputs
**Cause**: ComfyUI requires explicit slot_index for outputs when multiple outputs exist
- Always add `"slot_index": 0` for single outputs
- Number sequentially for multiple outputs

### 3. Invalid Reroute connections
**Cause**: Reroute nodes with empty links arrays or invalid connections
- Reroute nodes must have valid input AND output connections
- Remove reroute nodes if not properly connected

### 4. Incorrect Group Colors
**Standard Color Codes** (from COLOR_SCHEME.md):
- Green `#355335`: Loaders (checkpoints, models, VAE, LoRA)
- Blue `#353553`: Conditioning (CLIP, prompts)
- Red `#533535`: Sampling (KSampler)
- Yellow `#535335`: Latent operations (EmptyLatentImage, VAE encode/decode)
- Purple `#453553`: Post-processing (image operations)
- Teal `#355353`: Image I/O (SaveImage, LoadImage)
- Gray/Black `#444444`: Utility nodes (reroutes, primitives)

### 5. Missing Properties
**Required node properties**:
- `"flags": {}` - Even if empty
- `"order": <number>` - Execution order
- `"mode": 0` - Node mode (0 = normal)
- `"properties": {"Node name for S&R": "NodeType"}`

### 6. Link Format Issues
**Correct link format**: `[link_id, source_node, source_slot, target_node, target_slot, "TYPE"]`
- All 6 elements required
- TYPE must match the connection type exactly

## Prevention Checklist
- [ ] Use "bounding" not "bounding_box" for groups
- [ ] Add slot_index to all outputs
- [ ] Verify all reroute connections are complete
- [ ] Use correct color codes from COLOR_SCHEME.md
- [ ] Include all required node properties
- [ ] Ensure links have all 6 elements