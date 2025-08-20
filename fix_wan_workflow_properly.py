import json
import math

def reorganize_workflow_properly(input_path, output_path):
    """Fix the workflow with ACTUAL good spacing like we did before"""
    
    # Load the workflow
    with open(input_path, 'r') as f:
        workflow = json.load(f)
    
    # COMPACT SPACING - What actually worked!
    H_SPACING = 250  # NOT 2400px nonsense
    V_SPACING = 100  # Reasonable vertical spacing
    GRID_SIZE = 20
    
    # Color scheme for groups (like we had before!)
    GROUP_COLORS = {
        'input': '#3f789e',      # Blue
        'conditioning': '#8A8',   # Green  
        'generation': '#A88',     # Red/Pink
        'processing': '#88A',     # Purple
        'output': '#AA8'          # Yellow/Orange
    }
    
    # Categorize nodes properly
    node_stages = {}
    
    for node in workflow['nodes']:
        node_type = node.get('type', '')
        node_id = node.get('id')
        
        # Stage 0: Loaders (leftmost)
        if 'Loader' in node_type or 'Load' in node_type:
            node_stages[node_id] = 0
        # Stage 1: CLIP/Conditioning
        elif 'CLIP' in node_type or 'Condition' in node_type or 'TextEncode' in node_type:
            node_stages[node_id] = 1
        # Stage 2: Core Generation
        elif 'Sampler' in node_type or 'Scheduler' in node_type or 'Noise' in node_type or 'Guider' in node_type:
            node_stages[node_id] = 2
        # Stage 3: VAE/Processing
        elif 'VAE' in node_type or 'RIFE' in node_type or 'Image' in node_type and 'Save' not in node_type and 'Preview' not in node_type:
            node_stages[node_id] = 3
        # Stage 4: Output
        elif 'Save' in node_type or 'Preview' in node_type or 'Combine' in node_type:
            node_stages[node_id] = 4
        else:
            # Default to processing
            node_stages[node_id] = 3
    
    # Position nodes by stage with compact spacing
    stage_x_positions = {
        0: 0,
        1: H_SPACING * 2,
        2: H_SPACING * 4, 
        3: H_SPACING * 6,
        4: H_SPACING * 8
    }
    
    stage_current_y = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    # Apply new positions
    for node in workflow['nodes']:
        node_id = node.get('id')
        stage = node_stages.get(node_id, 3)
        
        # Set position
        x = stage_x_positions[stage]
        y = stage_current_y[stage]
        
        node['pos'] = [x, y]
        
        # Increment Y for next node in this stage
        node_height = node.get('size', [200, 100])[1] if 'size' in node else 100
        stage_current_y[stage] += node_height + 50  # 50px gap between nodes
    
    # Create visual groups with colors
    workflow['groups'] = [
        {
            "title": "Input/Loaders",
            "bounding": [-50, -50, H_SPACING * 2 - 50, max(stage_current_y[0], 600)],
            "color": GROUP_COLORS['input'],
            "font_size": 24,
            "flags": {}
        },
        {
            "title": "Conditioning",
            "bounding": [H_SPACING * 2 - 25, -50, H_SPACING * 2 - 50, max(stage_current_y[1], 600)],
            "color": GROUP_COLORS['conditioning'],
            "font_size": 24,
            "flags": {}
        },
        {
            "title": "Generation",
            "bounding": [H_SPACING * 4 - 25, -50, H_SPACING * 2 - 50, max(stage_current_y[2], 600)],
            "color": GROUP_COLORS['generation'],
            "font_size": 24,
            "flags": {}
        },
        {
            "title": "Processing",
            "bounding": [H_SPACING * 6 - 25, -50, H_SPACING * 2 - 50, max(stage_current_y[3], 600)],
            "color": GROUP_COLORS['processing'],
            "font_size": 24,
            "flags": {}
        },
        {
            "title": "Output",
            "bounding": [H_SPACING * 8 - 25, -50, H_SPACING * 2 - 50, max(stage_current_y[4], 600)],
            "color": GROUP_COLORS['output'],
            "font_size": 24,
            "flags": {}
        }
    ]
    
    # Save the PROPERLY reorganized workflow
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Workflow PROPERLY reorganized with COMPACT spacing")
    print(f"- Horizontal spacing: {H_SPACING}px (not 2400px!)")
    print(f"- Vertical gaps: 50px")
    print(f"- {len(workflow['groups'])} colorful groups added")
    print(f"- Total width: ~{H_SPACING * 10}px (2500px, not 36000px!)")

if __name__ == "__main__":
    input_path = r"C:\Users\gdahl\Downloads\wan21SeamlessLoop_v12\Wan 2.1 - seamless loop workflow v1.2.json"
    output_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\Wan_2.1_ACTUALLY_reorganized.json"
    
    reorganize_workflow_properly(input_path, output_path)