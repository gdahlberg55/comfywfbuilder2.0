"""
Lightweight Workflow Serializer - processes workflow efficiently
"""

import json
import os
from datetime import datetime

def validate_workflow_structure(workflow):
    """
    Lightweight validation without full json_validator overhead
    """
    errors = []
    warnings = []
    fixes_applied = []
    
    # Check required top-level keys
    required_keys = ['nodes', 'links']
    for key in required_keys:
        if key not in workflow:
            workflow[key] = []
            fixes_applied.append(f"Added missing '{key}' array")
    
    # Add version if missing
    if 'version' not in workflow:
        workflow['version'] = 0.4
        fixes_applied.append("Added missing 'version' field (0.4)")
    
    # Update last_node_id and last_link_id
    if workflow['nodes']:
        # Convert all node IDs to integers for comparison
        node_ids = []
        for node in workflow['nodes']:
            node_id = node.get('id', 0)
            if isinstance(node_id, str):
                try:
                    node_ids.append(int(node_id))
                except ValueError:
                    node_ids.append(0)
            else:
                node_ids.append(int(node_id))
        max_node_id = max(node_ids) if node_ids else 0
        workflow['last_node_id'] = max_node_id
        fixes_applied.append(f"Updated last_node_id to {max_node_id}")
    
    if workflow['links']:
        link_ids = []
        for link in workflow['links']:
            if isinstance(link, list) and len(link) > 0:
                link_id = link[0]
                if isinstance(link_id, str):
                    try:
                        link_ids.append(int(link_id))
                    except ValueError:
                        link_ids.append(0)
                else:
                    link_ids.append(int(link_id))
        max_link_id = max(link_ids) if link_ids else 0
        workflow['last_link_id'] = max_link_id
        fixes_applied.append(f"Updated last_link_id to {max_link_id}")
    
    # Validate nodes have required properties
    for i, node in enumerate(workflow.get('nodes', [])):
        node_id = node.get('id', f'unknown_{i}')
        
        # Check required properties
        if 'flags' not in node:
            node['flags'] = {}
            fixes_applied.append(f"Node {node_id}: Added missing 'flags'")
            
        if 'order' not in node:
            node['order'] = i
            fixes_applied.append(f"Node {node_id}: Added missing 'order' (set to {i})")
            
        if 'mode' not in node:
            node['mode'] = 0
            fixes_applied.append(f"Node {node_id}: Added missing 'mode' (set to 0)")
            
        if 'properties' not in node:
            node['properties'] = {}
            if 'type' in node:
                node['properties']['Node name for S&R'] = node['type']
            fixes_applied.append(f"Node {node_id}: Added missing 'properties'")
        
        # Fix outputs slot_index
        if 'outputs' in node:
            for j, output in enumerate(node.get('outputs', [])):
                if 'slot_index' not in output:
                    output['slot_index'] = j
                    fixes_applied.append(f"Node {node_id} output {j}: Added missing 'slot_index'")
    
    # Validate groups
    for i, group in enumerate(workflow.get('groups', [])):
        # Fix bounding_box -> bounding
        if 'bounding_box' in group and 'bounding' not in group:
            group['bounding'] = group['bounding_box']
            del group['bounding_box']
            fixes_applied.append(f"Group {i}: Changed 'bounding_box' to 'bounding'")
        elif 'bounding' not in group:
            group['bounding'] = [0, 0, 400, 300]
            fixes_applied.append(f"Group {i}: Added default 'bounding'")
    
    # Check link structure
    for i, link in enumerate(workflow.get('links', [])):
        if not isinstance(link, list) or len(link) != 6:
            errors.append(f"Link {i}: Invalid structure (expected 6 elements)")
    
    return {
        'errors': errors,
        'warnings': warnings,
        'fixes_applied': fixes_applied,
        'is_valid': len(errors) == 0
    }

def serialize_workflow(workflow_path):
    """
    Main serialization function
    """
    print(f"[Workflow Serializer Lite] Processing: {workflow_path}")
    
    # Load workflow
    try:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        print(f"[Workflow Serializer Lite] Loaded workflow with {len(workflow.get('nodes', []))} nodes")
    except Exception as e:
        print(f"[ERROR] Failed to load workflow: {e}")
        return None
    
    # Validate and fix
    print("[Workflow Serializer Lite] Validating and fixing workflow structure...")
    validation_result = validate_workflow_structure(workflow)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/workflows/v7_{timestamp}_serialized"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save serialized workflow
    output_path = os.path.join(output_dir, "workflow_serialized.json")
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"[Workflow Serializer Lite] Saved to: {output_path}")
    
    # Save report
    report = {
        'timestamp': timestamp,
        'source_workflow': workflow_path,
        'validation': validation_result,
        'summary': {
            'total_nodes': len(workflow.get('nodes', [])),
            'total_links': len(workflow.get('links', [])),
            'total_groups': len(workflow.get('groups', [])),
            'errors_count': len(validation_result['errors']),
            'fixes_applied': len(validation_result['fixes_applied']),
            'is_valid': validation_result['is_valid']
        }
    }
    
    report_path = os.path.join(output_dir, "serialization_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n[Workflow Serializer Lite] Summary:")
    print(f"  - Nodes: {report['summary']['total_nodes']}")
    print(f"  - Links: {report['summary']['total_links']}")
    print(f"  - Groups: {report['summary']['total_groups']}")
    print(f"  - Valid: {report['summary']['is_valid']}")
    print(f"  - Fixes Applied: {report['summary']['fixes_applied']}")
    
    if validation_result['fixes_applied']:
        print("\n  Fixes Applied:")
        for fix in validation_result['fixes_applied'][:10]:  # Show first 10
            print(f"    - {fix}")
        if len(validation_result['fixes_applied']) > 10:
            print(f"    ... and {len(validation_result['fixes_applied']) - 10} more")
    
    if validation_result['errors']:
        print("\n  Errors:")
        for error in validation_result['errors']:
            print(f"    - {error}")
    
    return output_path

if __name__ == "__main__":
    import sys
    
    # Default to the latest nomenclature-applied workflow
    workflow_path = "output/workflows/v6_20250815_145203_nomenclature_applied/outfit_variation_named.json"
    
    if len(sys.argv) > 1:
        workflow_path = sys.argv[1]
    
    result = serialize_workflow(workflow_path)
    if result:
        print(f"\n[SUCCESS] Workflow serialized to: {result}")
    else:
        print("\n[FAILED] Workflow serialization failed")