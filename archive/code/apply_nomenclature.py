"""
Apply descriptive nomenclature to outfit variation workflow
"""
import json
import os
from datetime import datetime

# Load the workflow
workflow_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v5_20250815_142937_collision_refined\workflow_collision_refined.json"
semantic_groups_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\semantic_groups\outfit_variation_semantic_groups_detailed.json"

with open(workflow_path, 'r') as f:
    workflow = json.load(f)

with open(semantic_groups_path, 'r') as f:
    semantic_data = json.load(f)

# Node type to descriptive name mapping
node_nomenclature = {
    # Loaders
    "UnetLoaderGGUFDisTorchMultiGPU": "(0) Model Loader - GGUF Multi-GPU",
    "CLIPLoaderMultiGPU": "(0) CLIP Loader - Multi-GPU", 
    "VAELoader": "(0) VAE Loader - Standard",
    "CLIPVisionLoader": "(0) Vision Model - CLIP",
    
    # LoRA Loaders
    "LoraLoaderModelOnly": {
        95: "(1) LoRA Stack - Bounce Motion V01",
        236: "(1) LoRA Stack - Bouncy Walk V01"
    },
    
    # Model Operations
    "ModelSamplingSD3": "(1) Model Config - SD3 Sampling",
    "PathchSageAttentionKJ": "(1) Model Patch - Sage Attention",
    "PatchModelPatcherOrder": "(1) Model Patch - Patcher Order",
    "WanVideoEnhanceAVideoKJ": "(1) Video Enhancement - A*Video",
    
    # Text Encoding
    "CLIPTextEncode": {
        14: "(2) Text Encode - Negative Prompt",
        126: "(2) Text Encode - Positive Main",
        130: "(2) Text Encode - Positive Style"
    },
    "CLIPVisionEncode": "(2) Vision Encode - Style Reference",
    "ConditioningSetTimestepRange": "(2) Conditioning - Timestep Range",
    "ConditioningCombine": "(2) Conditioning - Combine",
    
    # Image Processing  
    "LoadImage": "(3) Image Input - Source",
    "LoadImgFromUrl": "(3) Image Input - URL Source",
    "ImageMaskToMask": "(3) Mask Convert - Image to Mask",
    "ImageToMask": "(3) Mask Extract - Channel",
    "MaskToImage": "(3) Mask Convert - To Image",
    "WanImageUpscale": "(3) Image Process - Upscale",
    "ImageResize+": "(3) Image Process - Resize Plus",
    "ImageCrop": "(3) Image Process - Crop Region",
    
    # Control Parameters
    "PrimitiveNode": {
        129: "(4) Control - Steps Count",
        249: "(4) Control - Start Frame",
        250: "(4) Control - End Frame",
        192: "(4) Control - Width",
        193: "(4) Control - Height",
        269: "(4) Control - Seed Value"
    },
    "MathExpression|pysssss": "(4) Math - Expression Calculator",
    
    # Sampling
    "KSamplerSelect": "(5) Sampler - Gradient Estimation",
    "SamplerCustomAdvanced": "(5) Sampler - Advanced Custom",
    "BasicScheduler": "(5) Scheduler - Basic",
    "SplitSigmasDenoise": "(5) Sigma Split - Denoise",
    "FlipSigmas": "(5) Sigma Process - Flip",
    
    # Latent Operations
    "VAEEncode": "(5) VAE Encode - To Latent",
    "VAEDecode": {
        320: "(5) VAE Decode - First Pass",
        322: "(5) VAE Decode - Second Pass"
    },
    "EmptyLatentImage": "(5) Latent - Empty Image",
    
    # Video Processing
    "WanRepeatFrameToCount": "(6) Video - Repeat Frames",
    "WanSkipEndFrameImages_F2": "(6) Video - Skip End Frames",
    "VHS_VideoCombine": "(6) Video Output - Combine & Save",
    "ColorMatchImage": "(6) Color Process - Match Reference",
    
    # Output & Preview
    "PreviewImage": {
        110: "(7) Preview - Input Image",
        327: "(7) Preview - First Pass",
        324: "(7) Preview - Final Output"
    },
    
    # Reroute Nodes (Data Buses)
    "Reroute": {
        # These will be named based on their connection type
        "MODEL": "(Bus) MODEL Route",
        "CLIP": "(Bus) CLIP Route", 
        "VAE": "(Bus) VAE Route",
        "IMAGE": "(Bus) IMAGE Route",
        "LATENT": "(Bus) LATENT Route",
        "CONDITIONING": "(Bus) CONDITIONING Route"
    },
    
    # Notes
    "Note": "(8) Documentation - Note"
}

# Apply nomenclature to nodes
for node in workflow["nodes"]:
    node_type = node["type"]
    node_id = node["id"]
    
    # Check if we have a naming rule for this type
    if node_type in node_nomenclature:
        naming_rule = node_nomenclature[node_type]
        
        # Handle dictionary-based naming (for nodes with multiple instances)
        if isinstance(naming_rule, dict):
            if node_id in naming_rule:
                title = naming_rule[node_id]
            else:
                # Default naming if specific ID not found
                title = f"({node['order']}) {node_type}"
        else:
            title = naming_rule
            
        # Special handling for reroute nodes based on their connections
        if node_type == "Reroute" and "outputs" in node and len(node["outputs"]) > 0:
            output_type = node["outputs"][0].get("type", "UNKNOWN")
            if output_type in node_nomenclature["Reroute"]:
                title = node_nomenclature["Reroute"][output_type]
            else:
                title = f"(Bus) {output_type} Route"
    else:
        # Default naming for unknown nodes
        title = f"({node['order']}) {node_type}"
    
    # Apply the title
    node["title"] = title
    
    # Also add it to properties for compatibility
    if "properties" not in node:
        node["properties"] = {}
    node["properties"]["title"] = title

# Add groups from semantic groups
if "groups" not in workflow:
    workflow["groups"] = []

for group in semantic_data["semantic_groups"]:
    workflow_group = {
        "title": group["title"],
        "bounding": group["bounding"],
        "color": group["color"],
        "font_size": group.get("font_size", 24),
        "locked": group.get("locked", False),
        "metadata": group.get("metadata", {})
    }
    workflow["groups"].append(workflow_group)

# Create output directory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = rf"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v6_{timestamp}_nomenclature_applied"
os.makedirs(output_dir, exist_ok=True)

# Save the updated workflow
output_path = os.path.join(output_dir, "outfit_variation_named.json")
with open(output_path, 'w') as f:
    json.dump(workflow, f, indent=2)

# Create nomenclature report
report = {
    "timestamp": timestamp,
    "workflow_info": {
        "original_path": workflow_path,
        "output_path": output_path,
        "total_nodes": len(workflow["nodes"]),
        "total_groups": len(workflow["groups"])
    },
    "applied_names": {},
    "groups_added": []
}

# Document all applied names
for node in workflow["nodes"]:
    report["applied_names"][node["id"]] = {
        "type": node["type"],
        "title": node.get("title", "Untitled"),
        "order": node.get("order", -1)
    }

# Document groups
for group in workflow["groups"]:
    report["groups_added"].append({
        "title": group["title"],
        "bounding": group["bounding"],
        "color": group["color"]
    })

# Save the report
report_path = os.path.join(output_dir, "nomenclature_report.json")
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"Nomenclature applied successfully!")
print(f"Output saved to: {output_dir}")
print(f"- Workflow: outfit_variation_named.json")
print(f"- Report: nomenclature_report.json")
print(f"\nSummary:")
print(f"- {len(workflow['nodes'])} nodes renamed")
print(f"- {len(workflow['groups'])} groups added")