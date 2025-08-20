import json
import sys

def reorganize_workflow(input_path, output_path):
    """Reorganize the Wan 2.1 workflow with professional spacing"""
    
    # Load the workflow
    with open(input_path, 'r') as f:
        workflow = json.load(f)
    
    # Professional spacing parameters (addressing ISSUE-003)
    H_SPACING = 2400  # Horizontal spacing between stages
    V_SPACING = 400   # Vertical spacing between parallel nodes
    GROUP_PADDING = 100  # Padding within groups
    GRID_SIZE = 20  # Grid alignment
    
    # Node categories for organization
    node_categories = {
        'loaders': [],
        'conditioning': [],
        'generation': [],
        'processing': [],
        'output': []
    }
    
    # Categorize nodes
    for node in workflow['nodes']:
        node_type = node.get('type', '')
        
        if 'Loader' in node_type or 'Load' in node_type:
            node_categories['loaders'].append(node)
        elif 'CLIP' in node_type or 'Condition' in node_type or 'Encode' in node_type:
            node_categories['conditioning'].append(node)
        elif 'Sampler' in node_type or 'Guider' in node_type or 'Noise' in node_type or 'Scheduler' in node_type:
            node_categories['generation'].append(node)
        elif 'VAE' in node_type or 'Image' in node_type or 'Video' in node_type or 'RIFE' in node_type:
            node_categories['processing'].append(node)
        elif 'Preview' in node_type or 'Save' in node_type or 'Combine' in node_type:
            node_categories['output'].append(node)
        else:
            # Default to processing for uncategorized nodes
            node_categories['processing'].append(node)
    
    # Position nodes with professional spacing
    current_x = 0
    
    # Stage 1: Loaders (leftmost)
    y_pos = 0
    for node in node_categories['loaders']:
        node['pos'] = [current_x, y_pos]
        y_pos += V_SPACING
    
    # Stage 2: Conditioning
    current_x += H_SPACING
    y_pos = 0
    for node in node_categories['conditioning']:
        node['pos'] = [current_x, y_pos]
        y_pos += V_SPACING
    
    # Stage 3: Generation
    current_x += H_SPACING
    y_pos = 0
    for node in node_categories['generation']:
        node['pos'] = [current_x, y_pos]
        y_pos += V_SPACING
    
    # Stage 4: Processing
    current_x += H_SPACING
    y_pos = 0
    for node in node_categories['processing']:
        node['pos'] = [current_x, y_pos]
        y_pos += V_SPACING
    
    # Stage 5: Output (rightmost)
    current_x += H_SPACING
    y_pos = 0
    for node in node_categories['output']:
        node['pos'] = [current_x, y_pos]
        y_pos += V_SPACING
    
    # Align all positions to grid
    for node in workflow['nodes']:
        if 'pos' in node:
            node['pos'][0] = round(node['pos'][0] / GRID_SIZE) * GRID_SIZE
            node['pos'][1] = round(node['pos'][1] / GRID_SIZE) * GRID_SIZE
    
    # Update groups with proper spacing
    if 'groups' in workflow:
        for group in workflow['groups']:
            if 'bounding' in group:
                # Expand group boundaries for professional spacing
                group['bounding'][2] = max(group['bounding'][2], 1000)  # Min width
                group['bounding'][3] = max(group['bounding'][3], 500)   # Min height
    
    # Save the reorganized workflow
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Workflow reorganized and saved to {output_path}")
    print(f"- Total nodes: {len(workflow['nodes'])}")
    print(f"- Horizontal spacing: {H_SPACING}px")
    print(f"- Vertical spacing: {V_SPACING}px")
    print(f"- Grid alignment: {GRID_SIZE}px")

if __name__ == "__main__":
    input_path = r"C:\Users\gdahl\Downloads\wan21SeamlessLoop_v12\Wan 2.1 - seamless loop workflow v1.2.json"
    output_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\Wan_2.1_reorganized.json"
    
    reorganize_workflow(input_path, output_path)