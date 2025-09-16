# IPAdapter Fix for FLUX Workflows

## The Error
"IPAdapter model not present in the pipeline. Please load the models with the IPAdapterUnifiedLoader node."

## The Solution

### Option 1: Remove IPAdapter (Quick Fix)
- Simply bypass/delete the IPAdapterApply node
- Workflow will run without style transfer

### Option 2: Use IPAdapterUnifiedLoader (Proper Fix)
Replace the separate loaders with a single unified loader:

1. **Remove these nodes:**
   - IPAdapterModelLoader
   - IPAdapterApply

2. **Add instead:**
   - **IPAdapterUnifiedLoader** node with these settings:
     - model: Your FLUX model
     - preset: FLUX.1 or PLUS (FLUX)
     
3. **Required Model Files:**
   - Download CLIP Vision model: `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`
   - Download IPAdapter model: `ip-adapter-flux.1-dev.safetensors` 
   - Place in: `ComfyUI/models/clip_vision/` and `ComfyUI/models/ipadapter/`

4. **Connection Flow:**
   ```
   MODEL → IPAdapterUnifiedLoader → MODEL (with IPAdapter)
           ↑                    ↓
       image input          to sampler
   ```

## For SEGS/Enhancement Nodes

If using DetailerForEach or similar:

1. **Add Detection Chain:**
   ```
   UltralyticsDetectorProvider → bbox_detector
                                      ↓
   IMAGE → BboxDetectorSEGS → SEGS → DetailerForEach
               ↑
           threshold (0.5)
   ```

2. **Required Models:**
   - Face detection: `bbox/face_yolov8n.pt`
   - SAM model: `sam_vit_b_01ec64.pth`

## Working Workflow Available
The v7 workflow in `workspace/output/workflows/v7_20250901_005112_flux_fixed/` has these issues fixed and works without IPAdapter errors.