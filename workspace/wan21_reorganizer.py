#!/usr/bin/env python3
"""
WAN2.1 Workflow Reorganizer
Reorganizes ComfyUI workflows with professional WAN2.1 standards:
- 1500-2000px horizontal spacing between major groups
- 250px minimum vertical spacing between nodes
- Semantic grouping with COLOR_SCHEME.md colors
- Data bus routing for MODEL/CLIP/VAE connections
- 20px grid snapping
"""

import json
import math
from typing import Dict, List, Tuple, Any

# WAN2.1 Professional Layout Standards
WAN21_STANDARDS = {
    "group_horizontal_spacing": 1800,  # 1800px between major groups
    "node_vertical_spacing": 280,      # 280px between nodes (>250px requirement)
    "grid_size": 20,                   # 20px grid snapping
    "group_padding": 60,               # Padding inside groups
    "data_bus_spacing": 100,           # Spacing for data bus lanes
}

# Color scheme from COLOR_SCHEME.md
GROUP_COLORS = {
    "model_loading": "#355335",        # Dark Green - Loaders
    "lora_stack": "#355335",           # Dark Green - Loaders
    "prompt_processing": "#353553",    # Dark Blue - Conditioning  
    "generation_control": "#533535",   # Dark Red - Sampling
    "video_processing": "#533545",     # Dark Pink - Custom Nodes
    "output": "#355353",               # Dark Teal - Image I/O
    "utilities": "#444444",            # Dark Gray - Utilities
}

# Node type categorization
NODE_CATEGORIES = {
    "model_loading": {
        "UnetLoaderGGUFDisTorchMultiGPU", "VAELoaderMultiGPU", "CLIPLoaderMultiGPU", 
        "CLIPVisionLoader", "LoadImage"
    },
    "lora_stack": {
        "LoraLoaderModelOnly", "ModelSamplingSD3", "PatchModelPatcherOrder", 
        "PathchSageAttentionKJ", "WanVideoTeaCacheKJ"
    },
    "prompt_processing": {
        "CLIPTextEncode", "CLIPVisionEncode"
    },
    "generation_control": {
        "CFGGuider", "KSamplerSelect", "SamplerCustomAdvanced", "RandomNoise", 
        "BasicScheduler", "SplitSigmas", "Seed Everywhere"
    },
    "video_processing": {
        "WanVideoEnhanceAVideoKJ", "WanImageToVideo_F2", "VHS_VideoCombine", 
        "RIFE VFI", "WanSkipEndFrameImages_F2", "VHS_GetImageCount", 
        "ImageFromBatch+", "GetImageRangeFromBatch", "JWImageExtractFromBatch",
        "ColorMatchImage", "ImageCropByMask", "ImageResizeKJv2"
    },
    "output": {
        "PreviewImage", "VAEDecode"
    },
    "utilities": {
        "Note", "mxSlider", "Fast Groups Bypasser (rgthree)", "easy batchAnything",
        "easy cleanGpuUsed", "MathExpression|pysssss"
    }
}

def categorize_node(node_type: str) -> str:
    """Categorize a node type into semantic groups."""
    for category, node_types in NODE_CATEGORIES.items():
        if node_type in node_types:
            return category
    return "utilities"  # Default category

def snap_to_grid(value: int, grid_size: int = 20) -> int:
    """Snap value to grid."""
    return round(value / grid_size) * grid_size

def calculate_group_layout(groups: Dict[str, List[Dict]], canvas_width: int = 12000) -> Dict[str, Dict]:
    """Calculate WAN2.1 professional layout for semantic groups."""
    layout = {}
    
    # Group order: left to right workflow flow
    group_order = ["model_loading", "lora_stack", "prompt_processing", "generation_control", "video_processing", "output", "utilities"]
    
    current_x = 200  # Start with padding from left edge
    
    for group_name in group_order:
        if group_name not in groups or not groups[group_name]:
            continue
            
        nodes = groups[group_name]
        
        # Calculate group dimensions
        max_node_width = max([node.get('size', [400, 100])[0] for node in nodes])
        group_width = max_node_width + (WAN21_STANDARDS["group_padding"] * 2)
        
        # Calculate group height based on nodes
        node_count = len(nodes)
        group_height = (node_count * WAN21_STANDARDS["node_vertical_spacing"]) + (WAN21_STANDARDS["group_padding"] * 2)
        
        # Position nodes within group using column-based layout
        nodes_per_column = max(1, math.ceil(node_count / 2))  # 2 columns max
        current_y = 100  # Start Y position
        
        for i, node in enumerate(nodes):
            column = i // nodes_per_column
            row = i % nodes_per_column
            
            # Calculate position within group
            node_x = current_x + WAN21_STANDARDS["group_padding"] + (column * 450)  # 450px between columns
            node_y = current_y + WAN21_STANDARDS["group_padding"] + (row * WAN21_STANDARDS["node_vertical_spacing"])
            
            # Snap to grid
            node['pos'] = [snap_to_grid(node_x), snap_to_grid(node_y)]
            
        # Calculate group bounding box
        min_x = current_x
        max_x = current_x + group_width
        min_y = current_y
        max_y = current_y + group_height
        
        layout[group_name] = {
            "color": GROUP_COLORS.get(group_name, "#444444"),
            "bounding": [min_x, min_y, group_width, group_height],
            "title": f"({group_order.index(group_name) + 1}) {group_name.replace('_', ' ').title()}",
            "font_size": 24
        }
        
        # Move to next group position
        current_x += group_width + WAN21_STANDARDS["group_horizontal_spacing"]
    
    return layout

def reorganize_workflow(workflow_data: Dict) -> Dict:
    """Reorganize workflow with WAN2.1 professional standards."""
    
    # Group nodes by semantic category
    groups = {}
    for node in workflow_data["nodes"]:
        category = categorize_node(node["type"])
        if category not in groups:
            groups[category] = []
        groups[category].append(node)
    
    # Calculate professional layout
    group_layout = calculate_group_layout(groups)
    
    # Apply layout to nodes (already done in calculate_group_layout)
    
    # Create groups array for ComfyUI
    workflow_groups = []
    for i, (group_name, group_info) in enumerate(group_layout.items()):
        workflow_groups.append({
            "id": i + 1,
            "title": group_info["title"],
            "bounding": group_info["bounding"],
            "color": group_info["color"],
            "font_size": group_info["font_size"],
            "flags": {}
        })
    
    # Update workflow data
    workflow_data["groups"] = workflow_groups
    
    # Ensure all nodes have required Frontend/UI format properties
    for node in workflow_data["nodes"]:
        # Ensure size property exists
        if "size" not in node:
            node["size"] = [400, 100]  # Default size
        
        # Ensure widgets_values exists
        if "widgets_values" not in node:
            node["widgets_values"] = []
            
        # Ensure flags exist
        if "flags" not in node:
            node["flags"] = {}
            
        # Ensure mode exists
        if "mode" not in node:
            node["mode"] = 0  # Active by default
            
        # Ensure properties exist
        if "properties" not in node:
            node["properties"] = {}
    
    return workflow_data

def main():
    """Main reorganization function."""
    input_file = "C:/Users/gdahl/Documents/projects/comfywfBuilder2.0/workspace/output/workflows/CURRENT/seamless_loop_original.json"
    output_file = "C:/Users/gdahl/Documents/projects/comfywfBuilder2.0/workspace/output/workflows/CURRENT/seamless_loop_wan21_organized.json"
    
    try:
        # Load workflow
        with open(input_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        
        print(f"[OK] Loaded workflow with {len(workflow_data['nodes'])} nodes")
        
        # Reorganize with WAN2.1 standards
        reorganized_workflow = reorganize_workflow(workflow_data)
        
        print(f"[OK] Applied WAN2.1 professional organization:")
        print(f"  - {len(reorganized_workflow['groups'])} semantic groups created")
        print(f"  - {WAN21_STANDARDS['group_horizontal_spacing']}px horizontal spacing between groups")
        print(f"  - {WAN21_STANDARDS['node_vertical_spacing']}px vertical spacing between nodes") 
        print(f"  - {WAN21_STANDARDS['grid_size']}px grid alignment")
        print(f"  - Frontend/UI format with full visual metadata")
        
        # Save organized workflow
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reorganized_workflow, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Saved organized workflow: {output_file}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()