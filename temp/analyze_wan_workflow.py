#!/usr/bin/env python3
"""
Graph Analyzer for Wan 2.1 Seamless Loop Workflow
Analyzes the workflow structure and prepares for reorganization
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, deque

def load_workflow(filepath):
    """Load workflow JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_workflow_structure(workflow):
    """Analyze workflow structure and identify components"""
    nodes = workflow.get('nodes', [])
    links = workflow.get('links', [])
    
    # Categorize nodes by type
    node_categories = {
        'loaders': [],
        'conditioning': [],
        'sampling': [],
        'latent_ops': [],
        'post_processing': [],
        'utility': [],
        'video_processing': [],
        'controls': []
    }
    
    # Define node type categories
    loader_types = ['CLIPLoaderMultiGPU', 'UNETLoader', 'VAELoader', 'LoraLoader', 'CheckpointLoaderSimple']
    conditioning_types = ['CLIPTextEncode', 'ConditioningCombine', 'ConditioningSetArea']
    sampling_types = ['KSampler', 'KSamplerAdvanced', 'SamplerCustom', 'SamplerCustomAdvanced']
    latent_types = ['VAEEncode', 'VAEDecode', 'LatentUpscale', 'EmptyLatentImage']
    post_processing_types = ['ImageUpscaleWithModel', 'ImageScale', 'ImageComposite', 'ColorMatch']
    video_types = ['WanVideoEnhanceAVideoKJ', 'VHS_VideoCombine', 'RIFE VFI']
    utility_types = ['PrimitiveNode', 'Note', 'Reroute', 'IntegerInput', 'FloatInput']
    
    for node in nodes:
        node_type = node.get('type', '')
        
        if any(t in node_type for t in loader_types):
            node_categories['loaders'].append(node)
        elif any(t in node_type for t in conditioning_types):
            node_categories['conditioning'].append(node)
        elif any(t in node_type for t in sampling_types):
            node_categories['sampling'].append(node)
        elif any(t in node_type for t in latent_types):
            node_categories['latent_ops'].append(node)
        elif any(t in node_type for t in post_processing_types):
            node_categories['post_processing'].append(node)
        elif any(t in node_type for t in video_types):
            node_categories['video_processing'].append(node)
        elif any(t in node_type for t in utility_types):
            node_categories['utility'].append(node)
        else:
            node_categories['controls'].append(node)
    
    # Analyze current layout bounds
    x_coords = [node['pos'][0] for node in nodes if 'pos' in node]
    y_coords = [node['pos'][1] for node in nodes if 'pos' in node]
    
    bounds = {
        'min_x': min(x_coords) if x_coords else 0,
        'max_x': max(x_coords) if x_coords else 0,
        'min_y': min(y_coords) if y_coords else 0,
        'max_y': max(y_coords) if y_coords else 0,
        'width': max(x_coords) - min(x_coords) if x_coords else 0,
        'height': max(y_coords) - min(y_coords) if y_coords else 0
    }
    
    # Analyze connections
    connection_analysis = analyze_connections(workflow)
    
    return {
        'node_categories': node_categories,
        'bounds': bounds,
        'total_nodes': len(nodes),
        'total_links': len(links),
        'connection_analysis': connection_analysis
    }

def analyze_connections(workflow):
    """Analyze node connections for routing optimization"""
    nodes = {node['id']: node for node in workflow.get('nodes', [])}
    links = workflow.get('links', [])
    
    # Build connection graph
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    
    for link in links:
        if len(link) >= 4:
            source_node = link[1]
            target_node = link[3]
            graph[source_node].append(target_node)
            reverse_graph[target_node].append(source_node)
    
    # Find major data flows
    major_flows = find_major_data_flows(graph, nodes)
    
    return {
        'graph': dict(graph),
        'reverse_graph': dict(reverse_graph),
        'major_flows': major_flows
    }

def find_major_data_flows(graph, nodes):
    """Identify major data flow patterns for bus routing"""
    flows = []
    
    # Look for common connection patterns
    node_types = {node_id: node.get('type', '') for node_id, node in nodes.items()}
    
    # Find MODEL flows
    model_sources = [nid for nid, ntype in node_types.items() if 'Loader' in ntype and 'MODEL' in str(nodes[nid].get('outputs', []))]
    
    # Find CLIP flows  
    clip_sources = [nid for nid, ntype in node_types.items() if 'CLIP' in ntype]
    
    return {
        'model_flows': model_sources,
        'clip_flows': clip_sources
    }

def generate_layout_strategy(analysis):
    """Generate layout strategy based on analysis"""
    categories = analysis['node_categories']
    
    # Define stages with 1500-2000px spacing
    stage_positions = {
        'loaders': 0,
        'conditioning': 1800,
        'sampling': 3600,
        'video_processing': 5400,
        'post_processing': 7200,
        'utility': 9000
    }
    
    # Vertical stacking within stages
    vertical_spacing = 200
    group_height = 600
    
    layout_plan = {}
    
    for category, nodes in categories.items():
        if not nodes:
            continue
            
        base_x = stage_positions.get(category, 9000)
        base_y = 0
        
        for i, node in enumerate(nodes):
            layout_plan[node['id']] = {
                'x': base_x,
                'y': base_y + (i * vertical_spacing),
                'category': category
            }
    
    return layout_plan

def main():
    # Load the workflow
    workflow_path = Path("C:/Users/gdahl/OneDrive/Documents/Projects/ComfyUI/comfywfBuilder2.0/output/workflows/v1_20250814_174438/Wan_2.1_seamless_loop_reorganized_v1_20250814_174438.json")
    
    try:
        workflow = load_workflow(workflow_path)
        analysis = analyze_workflow_structure(workflow)
        layout_plan = generate_layout_strategy(analysis)
        
        # Output analysis results
        results = {
            'analysis': analysis,
            'layout_plan': layout_plan,
            'recommendations': {
                'horizontal_spacing': '1800px between major stages',
                'vertical_spacing': '200px between nodes in same category',
                'total_width': '~9000px for full workflow',
                'group_colors': {
                    'loaders': '#355335',
                    'conditioning': '#353553', 
                    'sampling': '#533535',
                    'video_processing': '#453553',
                    'post_processing': '#534535',
                    'utility': '#444444'
                }
            }
        }
        
        # Save analysis results
        output_path = Path("C:/Users/gdahl/OneDrive/Documents/Projects/ComfyUI/comfywfBuilder2.0/temp/wan_analysis_results.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"Analysis complete. Results saved to: {output_path}")
        print(f"Total nodes: {analysis['total_nodes']}")
        print(f"Current bounds: {analysis['bounds']['width']}x{analysis['bounds']['height']}px")
        print(f"Recommended width: ~9000px with 1800px stage spacing")
        
        return results
        
    except Exception as e:
        print(f"Error analyzing workflow: {e}")
        return None

if __name__ == "__main__":
    main()