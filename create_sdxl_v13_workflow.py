import json
import uuid

def create_sdxl_v13_workflow():
    """Create a professional SDXL Text-to-Image workflow with V13 compact layout"""
    
    # V13 COMPACT SPACING
    H_SPACING = 300  # Compact horizontal spacing between groups
    V_SPACING = 5    # 2-5px between nodes WITHIN groups
    HEADER_HEIGHT = 35  # Space for group header
    GROUP_PADDING = 20  # Padding around nodes in groups
    
    # Color scheme (from COLOR_SCHEME.md)
    GROUP_COLORS = {
        'loaders': '#3f789e',      # Blue
        'conditioning': '#4a7c59',  # Green  
        'generation': '#8b5a8c',    # Purple
        'upscaling': '#c97064',     # Red/Coral
        'detailing': '#b8860b',     # Dark Gold
        'output': '#d4a574'         # Light Gold
    }
    
    # Initialize workflow structure
    workflow = {
        "last_node_id": 50,
        "last_link_id": 100,
        "nodes": [],
        "links": [],
        "groups": [],
        "config": {},
        "extra": {
            "ds": {
                "scale": 0.5,
                "offset": [0, 0]
            }
        },
        "version": 0.4
    }
    
    # Node ID counter
    node_id = 1
    link_id = 1
    
    # Stage 1: Model Loading (X: 0-300)
    x_pos = GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # SDXL Base Checkpoint
    nodes = []
    base_checkpoint_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CheckpointLoaderSimple",
        "pos": [x_pos, y_pos],
        "size": [315, 98],
        "flags": {},
        "order": 0,
        "mode": 0,
        "outputs": [
            {"name": "MODEL", "type": "MODEL", "links": [], "slot_index": 0},
            {"name": "CLIP", "type": "CLIP", "links": [], "slot_index": 1},
            {"name": "VAE", "type": "VAE", "links": [], "slot_index": 2}
        ],
        "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
        "widgets_values": ["sdxl_base_1.0.safetensors"],
        "title": "(1) [Model] SDXL Base Loader"
    })
    node_id += 1
    y_pos += 98 + V_SPACING
    
    # SDXL Refiner Checkpoint
    refiner_checkpoint_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CheckpointLoaderSimple",
        "pos": [x_pos, y_pos],
        "size": [315, 98],
        "flags": {},
        "order": 1,
        "mode": 0,
        "outputs": [
            {"name": "MODEL", "type": "MODEL", "links": [], "slot_index": 0},
            {"name": "CLIP", "type": "CLIP", "links": [], "slot_index": 1},
            {"name": "VAE", "type": "VAE", "links": [], "slot_index": 2}
        ],
        "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
        "widgets_values": ["sdxl_refiner_1.0.safetensors"],
        "title": "(2) [Model] SDXL Refiner Loader"
    })
    node_id += 1
    y_pos += 98 + V_SPACING
    
    # Seed Control
    seed_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PrimitiveNode",
        "pos": [x_pos, y_pos],
        "size": [210, 82],
        "flags": {},
        "order": 2,
        "mode": 0,
        "outputs": [
            {"name": "INT", "type": "INT", "links": [], "slot_index": 0}
        ],
        "properties": {},
        "widgets_values": [42],
        "title": "(3) [Control] Seed"
    })
    node_id += 1
    y_pos += 82 + V_SPACING
    
    # Steps Control
    steps_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PrimitiveNode",
        "pos": [x_pos, y_pos],
        "size": [210, 82],
        "flags": {},
        "order": 3,
        "mode": 0,
        "outputs": [
            {"name": "INT", "type": "INT", "links": [], "slot_index": 0}
        ],
        "properties": {},
        "widgets_values": [30],
        "title": "(4) [Control] Steps"
    })
    node_id += 1
    y_pos += 82 + V_SPACING
    
    # CFG Control
    cfg_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PrimitiveNode",
        "pos": [x_pos, y_pos],
        "size": [210, 82],
        "flags": {},
        "order": 4,
        "mode": 0,
        "outputs": [
            {"name": "FLOAT", "type": "FLOAT", "links": [], "slot_index": 0}
        ],
        "properties": {},
        "widgets_values": [7.0],
        "title": "(5) [Control] CFG Scale"
    })
    node_id += 1
    
    # Stage 2: Text Conditioning (X: 300-600)
    x_pos = 300 + GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # Positive Prompt (Base)
    positive_base_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CLIPTextEncode",
        "pos": [x_pos, y_pos],
        "size": [400, 200],
        "flags": {},
        "order": 5,
        "mode": 0,
        "inputs": [
            {"name": "clip", "type": "CLIP", "link": None}
        ],
        "outputs": [
            {"name": "CONDITIONING", "type": "CONDITIONING", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": ["beautiful landscape, highly detailed, 8k, photorealistic"],
        "title": "(6) [CLIP] Positive Prompt (Base)"
    })
    node_id += 1
    y_pos += 200 + V_SPACING
    
    # Negative Prompt (Base)
    negative_base_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CLIPTextEncode",
        "pos": [x_pos, y_pos],
        "size": [400, 200],
        "flags": {},
        "order": 6,
        "mode": 0,
        "inputs": [
            {"name": "clip", "type": "CLIP", "link": None}
        ],
        "outputs": [
            {"name": "CONDITIONING", "type": "CONDITIONING", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": ["blurry, low quality, distorted"],
        "title": "(7) [CLIP] Negative Prompt (Base)"
    })
    node_id += 1
    y_pos += 200 + V_SPACING
    
    # Positive Prompt (Refiner)
    positive_refiner_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CLIPTextEncode",
        "pos": [x_pos, y_pos],
        "size": [400, 140],
        "flags": {},
        "order": 7,
        "mode": 0,
        "inputs": [
            {"name": "clip", "type": "CLIP", "link": None}
        ],
        "outputs": [
            {"name": "CONDITIONING", "type": "CONDITIONING", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": [""],
        "title": "(8) [CLIP] Positive Prompt (Refiner)"
    })
    node_id += 1
    y_pos += 140 + V_SPACING
    
    # Negative Prompt (Refiner)
    negative_refiner_id = node_id
    nodes.append({
        "id": node_id,
        "type": "CLIPTextEncode",
        "pos": [x_pos, y_pos],
        "size": [400, 140],
        "flags": {},
        "order": 8,
        "mode": 0,
        "inputs": [
            {"name": "clip", "type": "CLIP", "link": None}
        ],
        "outputs": [
            {"name": "CONDITIONING", "type": "CONDITIONING", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "CLIPTextEncode"},
        "widgets_values": [""],
        "title": "(9) [CLIP] Negative Prompt (Refiner)"
    })
    node_id += 1
    
    # Stage 3: Base Generation (X: 600-900)
    x_pos = 600 + GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # Empty Latent Image
    empty_latent_id = node_id
    nodes.append({
        "id": node_id,
        "type": "EmptyLatentImage",
        "pos": [x_pos, y_pos],
        "size": [315, 106],
        "flags": {},
        "order": 9,
        "mode": 0,
        "outputs": [
            {"name": "LATENT", "type": "LATENT", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "EmptyLatentImage"},
        "widgets_values": [1024, 1024, 1],
        "title": "(10) [Latent] Empty Image 1024x1024"
    })
    node_id += 1
    y_pos += 106 + V_SPACING
    
    # Base KSampler
    base_sampler_id = node_id
    nodes.append({
        "id": node_id,
        "type": "KSamplerAdvanced",
        "pos": [x_pos, y_pos],
        "size": [315, 334],
        "flags": {},
        "order": 10,
        "mode": 0,
        "inputs": [
            {"name": "model", "type": "MODEL", "link": None},
            {"name": "positive", "type": "CONDITIONING", "link": None},
            {"name": "negative", "type": "CONDITIONING", "link": None},
            {"name": "latent_image", "type": "LATENT", "link": None}
        ],
        "outputs": [
            {"name": "LATENT", "type": "LATENT", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "KSamplerAdvanced"},
        "widgets_values": ["enable", 0, "fixed", 30, 7.0, "dpmpp_2m", "karras", 0, 10000, "disable"],
        "title": "(11) [Sampler] Base Generation"
    })
    node_id += 1
    y_pos += 334 + V_SPACING
    
    # VAE Decode (Base)
    vae_decode_base_id = node_id
    nodes.append({
        "id": node_id,
        "type": "VAEDecode",
        "pos": [x_pos, y_pos],
        "size": [210, 46],
        "flags": {},
        "order": 11,
        "mode": 0,
        "inputs": [
            {"name": "samples", "type": "LATENT", "link": None},
            {"name": "vae", "type": "VAE", "link": None}
        ],
        "outputs": [
            {"name": "IMAGE", "type": "IMAGE", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "VAEDecode"},
        "title": "(12) [VAE] Decode Base"
    })
    node_id += 1
    y_pos += 46 + V_SPACING
    
    # Preview (Base)
    preview_base_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PreviewImage",
        "pos": [x_pos, y_pos],
        "size": [210, 246],
        "flags": {},
        "order": 12,
        "mode": 0,
        "inputs": [
            {"name": "images", "type": "IMAGE", "link": None}
        ],
        "properties": {"Node name for S&R": "PreviewImage"},
        "title": "(13) [Preview] Base Result"
    })
    node_id += 1
    
    # Stage 4: Refiner (X: 900-1200)
    x_pos = 900 + GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # Refiner KSampler
    refiner_sampler_id = node_id
    nodes.append({
        "id": node_id,
        "type": "KSamplerAdvanced",
        "pos": [x_pos, y_pos],
        "size": [315, 334],
        "flags": {},
        "order": 13,
        "mode": 0,
        "inputs": [
            {"name": "model", "type": "MODEL", "link": None},
            {"name": "positive", "type": "CONDITIONING", "link": None},
            {"name": "negative", "type": "CONDITIONING", "link": None},
            {"name": "latent_image", "type": "LATENT", "link": None}
        ],
        "outputs": [
            {"name": "LATENT", "type": "LATENT", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "KSamplerAdvanced"},
        "widgets_values": ["disable", 0, "fixed", 15, 7.0, "dpmpp_2m", "karras", 25, 30, "disable"],
        "title": "(14) [Sampler] Refiner"
    })
    node_id += 1
    y_pos += 334 + V_SPACING
    
    # VAE Decode (Refined)
    vae_decode_refined_id = node_id
    nodes.append({
        "id": node_id,
        "type": "VAEDecode",
        "pos": [x_pos, y_pos],
        "size": [210, 46],
        "flags": {},
        "order": 14,
        "mode": 0,
        "inputs": [
            {"name": "samples", "type": "LATENT", "link": None},
            {"name": "vae", "type": "VAE", "link": None}
        ],
        "outputs": [
            {"name": "IMAGE", "type": "IMAGE", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "VAEDecode"},
        "title": "(15) [VAE] Decode Refined"
    })
    node_id += 1
    y_pos += 46 + V_SPACING
    
    # Preview (Refined)
    preview_refined_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PreviewImage",
        "pos": [x_pos, y_pos],
        "size": [210, 246],
        "flags": {},
        "order": 15,
        "mode": 0,
        "inputs": [
            {"name": "images", "type": "IMAGE", "link": None}
        ],
        "properties": {"Node name for S&R": "PreviewImage"},
        "title": "(16) [Preview] Refined Result"
    })
    node_id += 1
    
    # Stage 5: Upscaling (X: 1200-1500)
    x_pos = 1200 + GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # Image Upscale By (2x)
    upscale_2x_id = node_id
    nodes.append({
        "id": node_id,
        "type": "ImageUpscaleWithModel",
        "pos": [x_pos, y_pos],
        "size": [315, 78],
        "flags": {},
        "order": 16,
        "mode": 0,
        "inputs": [
            {"name": "upscale_model", "type": "UPSCALE_MODEL", "link": None},
            {"name": "image", "type": "IMAGE", "link": None}
        ],
        "outputs": [
            {"name": "IMAGE", "type": "IMAGE", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "ImageUpscaleWithModel"},
        "title": "(17) [Upscale] 2x Upscaler"
    })
    node_id += 1
    y_pos += 78 + V_SPACING
    
    # Upscale Model Loader
    upscale_model_id = node_id
    nodes.append({
        "id": node_id,
        "type": "UpscaleModelLoader",
        "pos": [x_pos, y_pos],
        "size": [315, 58],
        "flags": {},
        "order": 17,
        "mode": 0,
        "outputs": [
            {"name": "UPSCALE_MODEL", "type": "UPSCALE_MODEL", "links": [], "slot_index": 0}
        ],
        "properties": {"Node name for S&R": "UpscaleModelLoader"},
        "widgets_values": ["4x-UltraSharp.pth"],
        "title": "(18) [Model] Upscale Model"
    })
    node_id += 1
    y_pos += 58 + V_SPACING
    
    # Preview (2x Upscaled)
    preview_2x_id = node_id
    nodes.append({
        "id": node_id,
        "type": "PreviewImage",
        "pos": [x_pos, y_pos],
        "size": [210, 246],
        "flags": {},
        "order": 18,
        "mode": 0,
        "inputs": [
            {"name": "images", "type": "IMAGE", "link": None}
        ],
        "properties": {"Node name for S&R": "PreviewImage"},
        "title": "(19) [Preview] 2x Upscaled"
    })
    node_id += 1
    
    # Stage 6: Output (X: 1500-1800)
    x_pos = 1500 + GROUP_PADDING
    y_pos = HEADER_HEIGHT + GROUP_PADDING
    
    # Save Image
    save_image_id = node_id
    nodes.append({
        "id": node_id,
        "type": "SaveImage",
        "pos": [x_pos, y_pos],
        "size": [315, 270],
        "flags": {},
        "order": 19,
        "mode": 0,
        "inputs": [
            {"name": "images", "type": "IMAGE", "link": None}
        ],
        "properties": {"Node name for S&R": "SaveImage"},
        "widgets_values": ["ComfyUI"],
        "title": "(20) [Output] Save Final Image"
    })
    node_id += 1
    
    # Add all nodes to workflow
    workflow["nodes"] = nodes
    workflow["last_node_id"] = node_id
    
    # Create links
    links = []
    
    # Base Model connections
    links.append([link_id, base_checkpoint_id, 0, base_sampler_id, 0, "MODEL"])
    link_id += 1
    links.append([link_id, base_checkpoint_id, 1, positive_base_id, 0, "CLIP"])
    link_id += 1
    links.append([link_id, base_checkpoint_id, 1, negative_base_id, 0, "CLIP"])
    link_id += 1
    links.append([link_id, base_checkpoint_id, 2, vae_decode_base_id, 1, "VAE"])
    link_id += 1
    links.append([link_id, base_checkpoint_id, 2, vae_decode_refined_id, 1, "VAE"])
    link_id += 1
    
    # Refiner Model connections
    links.append([link_id, refiner_checkpoint_id, 0, refiner_sampler_id, 0, "MODEL"])
    link_id += 1
    links.append([link_id, refiner_checkpoint_id, 1, positive_refiner_id, 0, "CLIP"])
    link_id += 1
    links.append([link_id, refiner_checkpoint_id, 1, negative_refiner_id, 0, "CLIP"])
    link_id += 1
    
    # Control connections
    links.append([link_id, seed_id, 0, base_sampler_id, 4, "INT"])
    link_id += 1
    links.append([link_id, seed_id, 0, refiner_sampler_id, 4, "INT"])
    link_id += 1
    links.append([link_id, steps_id, 0, base_sampler_id, 3, "INT"])
    link_id += 1
    links.append([link_id, cfg_id, 0, base_sampler_id, 5, "FLOAT"])
    link_id += 1
    links.append([link_id, cfg_id, 0, refiner_sampler_id, 5, "FLOAT"])
    link_id += 1
    
    # Conditioning connections
    links.append([link_id, positive_base_id, 0, base_sampler_id, 1, "CONDITIONING"])
    link_id += 1
    links.append([link_id, negative_base_id, 0, base_sampler_id, 2, "CONDITIONING"])
    link_id += 1
    links.append([link_id, positive_refiner_id, 0, refiner_sampler_id, 1, "CONDITIONING"])
    link_id += 1
    links.append([link_id, negative_refiner_id, 0, refiner_sampler_id, 2, "CONDITIONING"])
    link_id += 1
    
    # Generation flow
    links.append([link_id, empty_latent_id, 0, base_sampler_id, 3, "LATENT"])
    link_id += 1
    links.append([link_id, base_sampler_id, 0, refiner_sampler_id, 3, "LATENT"])
    link_id += 1
    links.append([link_id, base_sampler_id, 0, vae_decode_base_id, 0, "LATENT"])
    link_id += 1
    links.append([link_id, refiner_sampler_id, 0, vae_decode_refined_id, 0, "LATENT"])
    link_id += 1
    
    # Preview connections
    links.append([link_id, vae_decode_base_id, 0, preview_base_id, 0, "IMAGE"])
    link_id += 1
    links.append([link_id, vae_decode_refined_id, 0, preview_refined_id, 0, "IMAGE"])
    link_id += 1
    links.append([link_id, vae_decode_refined_id, 0, upscale_2x_id, 1, "IMAGE"])
    link_id += 1
    
    # Upscaling connections
    links.append([link_id, upscale_model_id, 0, upscale_2x_id, 0, "UPSCALE_MODEL"])
    link_id += 1
    links.append([link_id, upscale_2x_id, 0, preview_2x_id, 0, "IMAGE"])
    link_id += 1
    links.append([link_id, upscale_2x_id, 0, save_image_id, 0, "IMAGE"])
    link_id += 1
    
    workflow["links"] = links
    workflow["last_link_id"] = link_id
    
    # Create groups with V13 style
    groups = [
        {
            "title": "Step 1: Model Loading & Controls",
            "bounding": [0, 0, 280, 600],
            "color": GROUP_COLORS['loaders'],
            "font_size": 14,
            "flags": {}
        },
        {
            "title": "Step 2: Text Conditioning",
            "bounding": [300, 0, 420, 680],
            "color": GROUP_COLORS['conditioning'],
            "font_size": 14,
            "flags": {}
        },
        {
            "title": "Step 3: Base Generation",
            "bounding": [600, 0, 335, 850],
            "color": GROUP_COLORS['generation'],
            "font_size": 14,
            "flags": {}
        },
        {
            "title": "Step 4: Refiner Stage",
            "bounding": [900, 0, 335, 650],
            "color": GROUP_COLORS['upscaling'],
            "font_size": 14,
            "flags": {}
        },
        {
            "title": "Step 5: Upscaling",
            "bounding": [1200, 0, 335, 500],
            "color": GROUP_COLORS['detailing'],
            "font_size": 14,
            "flags": {}
        },
        {
            "title": "Step 6: Output",
            "bounding": [1500, 0, 335, 300],
            "color": GROUP_COLORS['output'],
            "font_size": 14,
            "flags": {}
        }
    ]
    
    workflow["groups"] = groups
    
    return workflow

if __name__ == "__main__":
    # Create the workflow
    workflow = create_sdxl_v13_workflow()
    
    # Save to file
    output_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\SDXL_T2I_V13_Professional.json"
    
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"SDXL Text-to-Image workflow created with V13 style:")
    print(f"- 6 color-coded groups")
    print(f"- 20 nodes total")
    print(f"- Compact spacing: 300px horizontal, 5px vertical")
    print(f"- Multiple preview points")
    print(f"- Upscaling pipeline included")
    print(f"Saved to: {output_path}")