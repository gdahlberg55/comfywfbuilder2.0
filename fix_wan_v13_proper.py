import json
import math

def reorganize_wan_properly_v13(input_path, output_path):
    """Fix the Wan workflow with V13-style compact spacing and proper headers"""
    
    # Load the workflow
    with open(input_path, 'r') as f:
        workflow = json.load(f)
    
    # V13 COMPACT SPACING - What actually worked!
    H_SPACING = 300  # Compact horizontal spacing between groups
    V_SPACING = 5    # 2-5px between nodes WITHIN groups
    HEADER_HEIGHT = 35  # Space for group header
    NOTE_HEIGHT = 30    # Height of note nodes
    GROUP_PADDING = 20  # Padding around nodes in groups
    GRID_SIZE = 5      # Small grid for precise alignment
    
    # Color scheme with darker headers (like tabs)
    GROUP_COLORS = {
        'loaders': '#3f789e',      # Blue
        'conditioning': '#4a7c59',  # Green  
        'generation': '#8b5a8c',    # Purple
        'processing': '#c97064',    # Red/Coral
        'output': '#d4a574'         # Yellow/Gold
    }
    
    # Stage descriptions for headers
    STAGE_DESCRIPTIONS = {
        0: "Load Models & Assets",
        1: "Text Conditioning", 
        2: "Generation Core",
        3: "Processing & Effects",
        4: "Output & Save"
    }
    
    # Categorize nodes by type
    nodes_by_stage = {0: [], 1: [], 2: [], 3: [], 4: []}
    note_nodes = []
    
    for node in workflow['nodes']:
        node_type = node.get('type', '')
        node_id = node.get('id')
        
        # Separate note nodes
        if node_type == 'Note':
            note_nodes.append(node)
            continue
            
        # Stage 0: Loaders
        if any(x in node_type for x in ['Loader', 'Load', 'MODEL', 'GGUF', 'Lora']):
            nodes_by_stage[0].append(node)
        # Stage 1: CLIP/Conditioning  
        elif any(x in node_type for x in ['CLIP', 'Text', 'Encode', 'Condition']):
            nodes_by_stage[1].append(node)
        # Stage 2: Generation
        elif any(x in node_type for x in ['Sampler', 'Schedule', 'Noise', 'Guider', 'Sigma']):
            nodes_by_stage[2].append(node)
        # Stage 3: Processing
        elif any(x in node_type for x in ['VAE', 'Image', 'RIFE', 'Video', 'Color', 'Wan']) and not any(x in node_type for x in ['Save', 'Preview', 'Combine']):
            nodes_by_stage[3].append(node)
        # Stage 4: Output
        elif any(x in node_type for x in ['Save', 'Preview', 'Combine']):
            nodes_by_stage[4].append(node)
        else:
            # Default to processing
            nodes_by_stage[3].append(node)
    
    # Calculate positions for each stage
    current_x = 0
    groups = []
    stage_bounds = {}
    
    for stage in range(5):
        if not nodes_by_stage[stage]:
            continue
            
        # Start Y position BELOW the header
        current_y = HEADER_HEIGHT + GROUP_PADDING
        max_width = 0
        
        # Position nodes in this stage
        for node in nodes_by_stage[stage]:
            # Get node dimensions
            if 'size' in node:
                node_width = node['size'][0]
                node_height = node['size'][1]
            else:
                node_width = 200
                node_height = 100
            
            # Set position (ensuring it's below header)
            node['pos'] = [current_x + GROUP_PADDING, current_y]
            
            # Update max width
            max_width = max(max_width, node_width)
            
            # Move to next Y position with tight spacing
            current_y += node_height + V_SPACING
        
        # Calculate group bounds
        group_width = max_width + GROUP_PADDING * 2
        group_height = current_y + GROUP_PADDING
        
        # Store stage bounds for note positioning
        stage_bounds[stage] = {
            'x': current_x,
            'width': group_width,
            'height': group_height
        }
        
        # Create group with proper header
        color_keys = ['loaders', 'conditioning', 'generation', 'processing', 'output']
        groups.append({
            "title": f"Step {stage + 1}: {STAGE_DESCRIPTIONS[stage]}",
            "bounding": [current_x, 0, group_width, group_height],
            "color": GROUP_COLORS[color_keys[stage]],
            "font_size": 14,
            "flags": {}
        })
        
        # Move to next stage position
        current_x += group_width + 50  # 50px gap between groups
    
    # Position note nodes
    for i, note in enumerate(note_nodes):
        note_text = note.get('widgets_values', [''])[0].lower() if 'widgets_values' in note else ''
        
        # Determine which stage this note relates to
        related_stage = None
        if 'model' in note_text or 'load' in note_text:
            related_stage = 0
        elif 'prompt' in note_text or 'condition' in note_text:
            related_stage = 1
        elif 'sampl' in note_text or 'gener' in note_text:
            related_stage = 2
        elif 'process' in note_text or 'vae' in note_text:
            related_stage = 3
        elif 'output' in note_text or 'save' in note_text:
            related_stage = 4
        
        if related_stage is not None and related_stage in stage_bounds:
            bounds = stage_bounds[related_stage]
            
            # Position between this stage and next, or at top for first/last
            if related_stage < 4 and (related_stage + 1) in stage_bounds:
                # Between two stages
                next_bounds = stage_bounds[related_stage + 1]
                x_pos = bounds['x'] + bounds['width'] + 10
                y_pos = min(bounds['height'], next_bounds['height']) // 2 - NOTE_HEIGHT // 2
            else:
                # At top of stage
                x_pos = bounds['x'] + GROUP_PADDING
                y_pos = -NOTE_HEIGHT - 10  # Above the group
            
            note['pos'] = [x_pos, y_pos]
            note['size'] = [bounds['width'] - GROUP_PADDING * 2, NOTE_HEIGHT]
    
    # Apply grid alignment to all positions
    for node in workflow['nodes']:
        if 'pos' in node:
            node['pos'][0] = round(node['pos'][0] / GRID_SIZE) * GRID_SIZE
            node['pos'][1] = round(node['pos'][1] / GRID_SIZE) * GRID_SIZE
    
    # Update workflow groups
    workflow['groups'] = groups
    
    # Save the properly reorganized workflow
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Workflow reorganized V13-style:")
    print(f"- Horizontal spacing: {H_SPACING}px between groups")
    print(f"- Vertical spacing: {V_SPACING}px between nodes")
    print(f"- Header clearance: {HEADER_HEIGHT}px")
    print(f"- {len(groups)} color-coded groups with headers")
    print(f"- {len(note_nodes)} note nodes positioned")
    print(f"- Total width: ~{current_x}px")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    input_path = r"C:\Users\gdahl\Downloads\wan21SeamlessLoop_v12\Wan 2.1 - seamless loop workflow v1.2.json"
    output_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\Wan_2.1_V13_style.json"
    
    reorganize_wan_properly_v13(input_path, output_path)