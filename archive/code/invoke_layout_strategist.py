#!/usr/bin/env python3
"""
Layout Strategist Agent Invocation Script
This script simulates the layout-strategist agent execution for the AE workflow
"""

import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 80)
    print("LAYOUT STRATEGIST AGENT - EXECUTING")
    print("=" * 80)
    
    # Task parameters
    task_params = {
        "spacing": {
            "within_groups": 80,
            "between_groups": 300,
            "between_categories": 600,
            "data_bus_vertical_offset": 150
        },
        "data_bus_lanes": {
            "AE_BG": 0,      # Top lane for AE Background
            "AE_FG": 150,    # Second lane for AE Foreground  
            "MODEL": 300,    # Third lane for model connections
            "CLIP": 450,     # Fourth lane for CLIP connections
            "IMAGE": 600     # Bottom lane for image data
        }
    }
    
    print("\n1. RETRIEVING WORKFLOW FROM MEMORY...")
    # In a real implementation, this would use mcp__memory__retrieve
    # For now, we'll simulate by looking for existing workflow files
    
    workflow_files = []
    output_dir = "output/workflows"
    if os.path.exists(output_dir):
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.json') and 'ae' in file.lower():
                    workflow_files.append(os.path.join(root, file))
    
    if workflow_files:
        print(f"Found {len(workflow_files)} workflow files")
        latest_file = max(workflow_files, key=os.path.getmtime)
        print(f"Using latest: {latest_file}")
        
        with open(latest_file, 'r') as f:
            workflow = json.load(f)
    else:
        print("ERROR: No workflow found in memory or filesystem")
        return
    
    print("\n2. ANALYZING WORKFLOW STRUCTURE...")
    # Handle both dict and list node formats
    nodes_data = workflow.get('nodes', {})
    if isinstance(nodes_data, dict):
        nodes = list(nodes_data.values())
    else:
        nodes = nodes_data
    
    # Get connections/links
    connections = workflow.get('connections', workflow.get('links', []))
    groups = workflow.get('groups', [])
    
    print(f"- Nodes: {len(nodes)}")
    print(f"- Connections: {len(connections) if isinstance(connections, list) else connections}")
    print(f"- Groups: {len(groups)}")
    
    # Identify AE nodes
    ae_nodes = []
    for node in nodes:
        if isinstance(node, dict):
            node_type = node.get('type', '')
            if 'AE' in node_type or 'AnimateDiff' in node_type:
                ae_nodes.append(node)
    print(f"- AE/AnimateDiff Nodes: {len(ae_nodes)}")
    
    print("\n3. CALCULATING LAYOUT...")
    
    # Stage-based layout calculation
    stages = {
        'input': [],
        'processing': [],
        'ae_integration': [],
        'output': []
    }
    
    # Categorize nodes
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_type = node.get('type', '')
        if 'LoadImage' in node_type or 'Checkpoint' in node_type:
            stages['input'].append(node)
        elif 'Save' in node_type or 'Preview' in node_type:
            stages['output'].append(node)
        elif 'AE' in node_type or 'AnimateDiff' in node_type:
            stages['ae_integration'].append(node)
        else:
            stages['processing'].append(node)
    
    print("\n4. APPLYING LAYOUT POSITIONS...")
    
    # X-axis positions for stages
    x_positions = {
        'input': 0,
        'processing': 800,
        'ae_integration': 1600,
        'output': 2400
    }
    
    # Apply positions
    for stage_name, stage_nodes in stages.items():
        x_base = x_positions[stage_name]
        y_current = 0
        
        for i, node in enumerate(stage_nodes):
            # Check if node is in a data bus lane
            if node in ae_nodes:
                # Position in appropriate data bus lane
                if 'BG' in str(node.get('title', '')):
                    y_pos = task_params['data_bus_lanes']['AE_BG']
                elif 'FG' in str(node.get('title', '')):
                    y_pos = task_params['data_bus_lanes']['AE_FG']
                else:
                    y_pos = y_current
            else:
                y_pos = y_current
            
            # Update node position
            node['pos'] = [x_base, y_pos]
            
            # Update y position for next node
            if node not in ae_nodes:
                y_current += task_params['spacing']['within_groups']
        
        # Add stage spacing
        y_current += task_params['spacing']['between_categories']
    
    print("\n5. STORING UPDATED WORKFLOW...")
    
    # Update the original workflow structure with new positions
    if isinstance(workflow.get('nodes'), dict):
        # Update dict-based nodes
        for node in nodes:
            node_id = str(node.get('id', ''))
            if node_id in workflow['nodes']:
                workflow['nodes'][node_id]['pos'] = node['pos']
    else:
        # Update list-based nodes
        workflow['nodes'] = nodes
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_dir = f"output/workflows/v2_{timestamp}_layout_strategist"
    os.makedirs(version_dir, exist_ok=True)
    
    # Save workflow
    output_file = os.path.join(version_dir, "ae_workflow_layout_v2.json")
    with open(output_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"\nWorkflow saved to: {output_file}")
    
    # Create summary report
    report = {
        "agent": "layout-strategist",
        "timestamp": datetime.now().isoformat(),
        "workflow_stats": {
            "total_nodes": len(nodes),
            "ae_nodes": len(ae_nodes),
            "stages": {k: len(v) for k, v in stages.items()}
        },
        "layout_applied": {
            "spacing": task_params['spacing'],
            "data_bus_lanes": task_params['data_bus_lanes'],
            "stage_positions": x_positions
        },
        "output_file": output_file,
        "memory_key": "ae_workflow_layout_v2_20250814"
    }
    
    report_file = os.path.join(version_dir, "layout_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {report_file}")
    
    print("\n" + "=" * 80)
    print("LAYOUT STRATEGIST AGENT - COMPLETE")
    print("=" * 80)
    
    # In real implementation, would update SCS via mcp__memory__store
    print("\nSCS Update (simulated):")
    print(f"- Memory key: ae_workflow_layout_v2_20250814")
    print(f"- Status: layout_complete")
    print(f"- Next agent: layout-refiner")

if __name__ == "__main__":
    main()