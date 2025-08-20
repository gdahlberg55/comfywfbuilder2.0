#!/usr/bin/env python3
"""
Wan 2.1 Seamless Loop Workflow Compact Reorganizer
Creates EXTREMELY COMPACT layout matching user's screenshot requirements
"""

import json
import os

def load_workflow():
    """Load the source Wan workflow"""
    source_path = r"C:\Users\gdahl\Downloads\wan21SeamlessLoop_v12\Wan_2.1_V13_style_NAMED.json"
    with open(source_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_compact_layout(workflow_data):
    """Create EXTREMELY compact layout with 400-600px major section spacing"""
    
    # CRITICAL COMPACT LAYOUT PARAMETERS
    SECTION_SPACING = 500  # 500px between major sections (NOT 1800px!)
    GROUP_PADDING = 25     # Tight group padding
    NODE_V_SPACING = 60    # Vertical spacing between nodes
    NODE_H_SPACING = 80    # Horizontal spacing within sections
    
    # Define compact column layout (6 main columns)
    COLUMNS = {
        'model_loading': 0,      # X: 0
        'input_processing': 500,  # X: 500
        'generation': 1000,      # X: 1000  
        'frame_processing': 1500, # X: 1500
        'interpolation': 2000,   # X: 2000
        'final_output': 2500     # X: 2500
    }
    
    # Node categorization for compact vertical stacking
    node_categories = {
        # Far Left Column: Model Loading (Purple Group)
        'model_loading': [97, 98, 99, 95, 236, 48, 28, 84, 50, 54, 230],  # Models, LoRAs, configs
        
        # Left-Center: Input Processing (Teal Group) 
        'input_processing': [339, 112, 109, 96, 110, 17, 16],  # Image load, crop, resize, vision
        
        # Center: Generation Pipeline (Purple Group)
        'generation': [118, 14, 315, 310, 318, 319, 317, 314, 313, 312, 316],  # Prompts, sampling
        
        # Right-Center: Frame Processing (Teal Group)
        'frame_processing': [322, 323, 320, 306, 276, 249, 246],  # Decode, skip frames, color match
        
        # Right: Interpolation (Purple Group) 
        'interpolation': [277, 278, 301, 279, 290, 294, 291, 293, 282, 284, 304, 305, 281, 358],  # Controls and RIFE
        
        # Far Right: Final Output (Purple Group)
        'final_output': [321, 38, 299, 349, 356, 221, 359, 222, 247]  # Video combines and final output
    }
    
    # COMPACT POSITIONING - Extremely tight vertical stacking
    nodes = workflow_data["nodes"]
    
    for node in nodes:
        node_id = node["id"]
        
        # Find which category this node belongs to
        category = None
        for cat, node_list in node_categories.items():
            if node_id in node_list:
                category = cat
                break
        
        if category:
            # Get column X position
            base_x = COLUMNS[category]
            
            # Calculate tight vertical position within category
            node_index = node_categories[category].index(node_id)
            y_pos = -2000 + (node_index * NODE_V_SPACING)  # Start at -2000, stack tightly
            
            # Apply position
            node["pos"] = [base_x, y_pos]
            
            # Ensure compact node sizes
            if "size" not in node or not node["size"]:
                node["size"] = [400, 80]  # Default compact size
            else:
                # Keep width reasonable, limit height for compactness
                current_size = node["size"]
                if isinstance(current_size, list) and len(current_size) >= 2:
                    node["size"] = [min(current_size[0], 450), min(current_size[1], 200)]
        
        # Handle note nodes - make them ultra-thin and place in gaps
        if node.get("type") == "Note":
            # Find gaps between groups and place notes there
            note_positions = [
                [250, -1500],   # Between model and input
                [750, -1500],   # Between input and generation  
                [1250, -1500],  # Between generation and processing
                [1750, -1500],  # Between processing and interpolation
                [2250, -1500],  # Between interpolation and output
            ]
            
            # Assign note position based on node ID
            pos_index = (node_id % len(note_positions))
            node["pos"] = note_positions[pos_index]
            node["size"] = [200, 30]  # Ultra-thin profile for notes
    
    # Create COMPACT group definitions with Purple/Teal color scheme
    groups = [
        {
            "id": 1,
            "title": "(1) Model Loading",
            "bounding": [-50, -2050, 500, 800],  # Tight bounding
            "color": "#8A8AA8",  # Purple
            "font_size": 20,
            "flags": {}
        },
        {
            "id": 2, 
            "title": "(2) Input Processing",
            "bounding": [450, -2050, 500, 600],  # Compact
            "color": "#3f789e",  # Teal
            "font_size": 20,
            "flags": {}
        },
        {
            "id": 3,
            "title": "(3) Generation Pipeline", 
            "bounding": [950, -2050, 500, 800],  # Tight
            "color": "#A88AA8",  # Purple variant
            "font_size": 20,
            "flags": {}
        },
        {
            "id": 4,
            "title": "(4) Frame Processing",
            "bounding": [1450, -2050, 500, 600],  # Compact  
            "color": "#8AA88A",  # Teal variant
            "font_size": 20,
            "flags": {}
        },
        {
            "id": 5,
            "title": "(5) Interpolation",
            "bounding": [1950, -2050, 500, 700],  # Tight
            "color": "#8A8AA8",  # Purple
            "font_size": 20,
            "flags": {}
        },
        {
            "id": 6,
            "title": "(6) Final Output",
            "bounding": [2450, -2050, 500, 800],  # Compact
            "color": "#A88AA8",  # Purple variant  
            "font_size": 20,
            "flags": {}
        }
    ]
    
    workflow_data["groups"] = groups
    
    return workflow_data

def save_compact_workflow(workflow_data):
    """Save the reorganized compact workflow"""
    output_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v3_20250119_wan_compact\Wan_2.1_compact_layout.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow_data, f, indent=2, ensure_ascii=False)
    
    print(f"COMPACT workflow saved to: {output_path}")
    print(f"Total width: ~3000px (was >10800px)")
    print(f"Section spacing: 500px (was ~1800px)")
    print(f"Layout: 6 tight vertical columns")
    print(f"Groups: 6 compact themed groups")
    
    return output_path

def main():
    """Main reorganization process"""
    print("Starting WAN 2.1 COMPACT Layout Reorganization")
    print("Target: EXTREMELY COMPACT vertical layout")
    print("Max width: 3000px (4-5x smaller than original)")
    print()
    
    # Load source workflow
    print("Loading source workflow...")
    workflow = load_workflow()
    print(f"Loaded {len(workflow['nodes'])} nodes")
    
    # Create compact layout
    print("Creating COMPACT layout...")
    compact_workflow = create_compact_layout(workflow)
    
    # Save result
    print("Saving compact workflow...")
    output_path = save_compact_workflow(compact_workflow)
    
    print("\nCOMPACT REORGANIZATION COMPLETE!")
    print("Layout Summary:")
    print("   - 6 vertical columns with 500px spacing")
    print("   - Purple/Teal color scheme") 
    print("   - Ultra-tight node stacking")
    print("   - Total width: ~3000px (massive reduction)")
    print("   - Dense, professional layout")
    
    return output_path

if __name__ == "__main__":
    main()