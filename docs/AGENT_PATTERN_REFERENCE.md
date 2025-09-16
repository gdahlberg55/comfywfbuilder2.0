# Agent-Specific Pattern Reference
## Based on User's 4.5 Ultimate Workflow (Gold Standard)

## CRITICAL: Learning Source Policy
- **ONLY LEARN FROM:** User-provided workflows (currently: `C:\Users\gdahl\Downloads\4.5 ultimate.json`)
- **NEVER REFERENCE:** Claude/Orchestrator-generated workflows (not professional grade)
- **ALWAYS CHECK:** User's reference workflows FIRST before creating anything new
- **NEW CAPABILITY:** Extract workflows from PNG metadata when user provides screenshots

## Updated Patterns (2025-01-31)

### Workflow Extraction Pattern
**Method**: Extract embedded workflows from PNG files
```python
# Check PNG for tEXt chunks with "workflow" keyword
# Parse JSON from metadata
# Validate Frontend/UI format
```

### CLIPSetLastLayer Integration
**Standard Pattern for All Workflows:**
1. Insert between CLIP source and text encoders
2. Position in clear space (typically [250, 500])
3. Default value: -2 (adjustable -1 to -12)
4. Title: "[CLIP] Skip Last Layers"
5. Preserve all existing node positions

---

## Pattern Reference for Each Agent

### 1. Parameter-Extractor Agent
**Patterns to Extract:**
- Resolution: Look for SDXL preset resolutions (832x1216 portrait)
- Sampling steps: Base=30, refinement=20
- Denoise values: 1.0 for base, 0.2 for refinement
- Sampler preference: "deis"
- Scheduler: "simple" for base, "normal" for refinement
- Guidance scale: 3.0 for Flux

### 2. Asset-Finder Agent
**Required Assets from 4.5 Ultimate:**
- Models: flux1-dev-fp8.safetensors (UNETLoader)
- CLIP: clipLCLIPGFullFP32_zer0intVisionCLIPL.safetensors + t5xxl_fp16.safetensors
- VAE: ae.safetensors
- LoRAs: Check Power Lora Loader for up to 7 slots
- Upscale models: SwinIR models for Ultimate SD Upscale

### 3. Prompt-Crafter Agent
**Prompt Structure Patterns:**
- Use CLIPTextEncodeFlux with separate clip_l and t5xxl
- ImpactWildcardProcessor with populated_text fallback
- Guidance value: 3.0
- Support for wildcard paths: C:\\Users\\gdahl\\Documents\\ComfyUI\\wildcards\\

### 4. Workflow-Architect Agent
**Architecture Requirements:**
- 4-Pass System:
  * Pass 1: Base generation
  * Pass 2: Hi-res fix (LatentUpscaleBy → SamplerCustomAdvanced)
  * Pass 3: Ultimate SD Upscale (2x upscale)
  * Pass 4: Ultimate SD Upscale No Upscale (refinement)
- Save points after each pass

### 5. Node-Curator Agent
**MANDATORY Node Preferences:**
```json
{
  "model_loading": {
    "primary": "UNETLoader",
    "clip": "DualCLIPLoader",
    "vae": "VAELoader",
    "sampling": "ModelSamplingFlux"
  },
  "lora_management": {
    "required": "Power Lora Loader (rgthree)",
    "avoid": "standard LoraLoader chains"
  },
  "latent_generation": {
    "preferred": "SDXL Empty Latent Image (rgthree)",
    "dimensions": "preset resolutions"
  },
  "sampling": {
    "primary": "SamplerCustomAdvanced",
    "scheduler": "BasicScheduler",
    "enhancement": "DetailDaemonSamplerNode"
  },
  "upscaling": {
    "primary": "UltimateSDUpscale",
    "refinement": "UltimateSDUpscaleNoUpscale"
  },
  "workflow_control": {
    "required": "Fast Groups Bypasser (rgthree)"
  }
}
```

### 6. Graph-Engineer Agent
**Connection Patterns:**
- Model flow: UNETLoader → Power Lora Loader → ModelSamplingFlux → Samplers
- CLIP flow: DualCLIPLoader → Power Lora Loader → CLIPTextEncodeFlux
- Multi-pass connections: Each pass feeds into the next
- Parallel saves: Connect to SaveImage after each decode

### 7. Graph-Analyzer Agent
**Analysis Checklist:**
- Verify 4-pass architecture present
- Check for Power Lora Loader centralization
- Confirm rgthree nodes usage
- Validate Ultimate SD Upscale chain

### 8. Layout-Strategist Agent
**Layout Patterns from 4.5 Ultimate:**
- Node spacing: Proper spacing between functional groups
- Vertical arrangement for passes
- Group nodes by function, not just connection
- Data bus for common connections (MODEL, CLIP, VAE)

### 9. Reroute-Engineer Agent
**Routing Requirements:**
- Use reroute nodes for long-distance connections
- Create horizontal/vertical highways
- Group reroutes by type (MODEL, CLIP, VAE, CONDITIONING)
- Avoid diagonal connections

### 10. Layout-Refiner Agent
**Refinement Standards:**
- Minimum 50px between nodes
- 35px clearance below group headers
- Snap to 20px grid
- No overlapping nodes or connections

### 11. Group-Coordinator Agent
**Grouping Patterns:**
- Group 1: Model Loading (UNETLoader, DualCLIPLoader, VAELoader)
- Group 2: LoRA Management (Power Lora Loader)
- Group 3: Prompt Processing (Wildcards, CLIPTextEncodeFlux)
- Group 4: Pass 1 - Base Generation
- Group 5: Pass 2 - Hi-Res Fix
- Group 6: Pass 3 - Upscale
- Group 7: Pass 4 - Refinement
- Group 8: Output Management

### 12. Nomenclature-Specialist Agent
**Naming Conventions:**
- Nodes: "(#) Purpose - Details"
- Groups: Descriptive function names
- Examples from 4.5 Ultimate:
  * "Load Diffusion Model"
  * "Power Lora Loader (rgthree)"
  * "Detail Daemon Sampler"
  * "Ultimate SD Upscale"

### 13. Workflow-Validator Agent
**Validation Checklist:**
- ✓ UNETLoader with fp8_e4m3fn
- ✓ DualCLIPLoader present
- ✓ Power Lora Loader (rgthree) used
- ✓ ModelSamplingFlux configured
- ✓ 4-pass architecture complete
- ✓ Fast Groups Bypasser included
- ✓ Save points after each pass

### 14. Templating-Enforcer Agent
**Gold Standard Requirements:**
- Must match 4.5 Ultimate patterns
- rgthree suite nodes required
- Clear group organization
- Proper naming conventions

### 15. Workflow-Serializer Agent
**Serialization Standards:**
- Maintain all rgthree-specific properties
- Preserve widget configurations
- Include _meta titles
- Proper link arrays with 6 elements

### 16. Learning-Agent
**Key Patterns to Remember:**
- User prefers rgthree node suite
- Power Lora Loader is mandatory for LoRA management
- 4-pass architecture is standard
- Fast Groups Bypasser for workflow control

### 17. Issue-Tracker Agent
**Common Issues from User Workflows:**
- Missing Fast Groups Bypasser (must be added back)
- Not using Power Lora Loader
- Missing Ultimate SD Upscale passes

### 18. Memory-Monitor Agent
**Memory Patterns:**
- Large workflows use 50+ nodes
- Multiple LoRAs active simultaneously
- High-resolution processing (2x, 4x upscales)
- Monitor Ultimate SD Upscale memory usage

### 19. Visualizer Agent
**Visualization Requirements:**
- Show 4-pass flow clearly
- Highlight rgthree nodes
- Display group organization
- Mark save points

### 20. Context Agents
**Context Requirements:**
- Maintain model/clip/vae references
- Track pass numbers
- Preserve LoRA settings
- Remember sampling configurations

---

## Critical Implementation Notes

### ALWAYS Use These Patterns:
1. **UNETLoader + DualCLIPLoader + VAELoader** (separate loading)
2. **Power Lora Loader (rgthree)** for ALL LoRA management
3. **ModelSamplingFlux** after model loading
4. **4-Pass Architecture** minimum
5. **Ultimate SD Upscale** for quality upscaling
6. **Fast Groups Bypasser** for workflow control

### NEVER Use These:
1. Single LoraLoader chains (use Power Lora Loader instead)
2. Simple upscaling (use Ultimate SD Upscale)
3. Single-pass generation

### Settings to Memorize:
```json
{
  "model_sampling_flux": {
    "max_shift": 1.15,
    "base_shift": 0.5
  },
  "sampling": {
    "base_steps": 30,
    "refinement_steps": 20,
    "base_denoise": 1.0,
    "refinement_denoise": 0.2
  },
  "ultimate_sd_upscale": {
    "mode": "Chess",
    "tile_width": 1024,
    "tile_height": 1024,
    "mask_blur": 16,
    "force_uniform_tiles": true
  },
  "detail_daemon": {
    "detail_amount": 0.5,
    "start": 0.1,
    "end": 0.7,
    "bias": 0.2
  }
}
```

---

## Agent Communication Protocol

All agents MUST:
1. Check this reference before generating
2. Use patterns from user's workflows ONLY
3. Implement rgthree nodes where available
4. Follow 4-pass architecture
5. Include Fast Groups Bypasser

## Updates
- Last Updated: [Current Session]
- Source Workflow: 4.5 ultimate.json
- Status: Active Reference Document