"""
Invoke Layout Refiner Agent for collision detection and layout refinement
"""
import json
import sys
import os
from datetime import datetime

# Add code_modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code_modules'))

# Import collision detection module
from collision_detection import AABBCollisionDetector

def load_workflow(filepath):
    """Load workflow JSON from file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def prepare_scs_data(workflow):
    """Prepare workflow data in SCS format for collision detection"""
    return {
        "session_metadata": {
            "session_id": f"layout_refiner_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "current_stage": "LayoutRefiner",
            "status": "active"
        },
        "workflow_state": {
            "current_graph": workflow
        },
        "layout_parameters": {
            "min_spacing": 80,
            "grid_size": 50,
            "layout_metrics": {}
        },
        "logging_metrics": {
            "errors_encountered": [],
            "performance_by_agent": {}
        }
    }

def main():
    # Load the workflow with data buses
    workflow_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v4_20250815_data_bus_routing\workflow_with_data_buses.json"
    workflow = load_workflow(workflow_path)
    
    # Prepare SCS data
    scs_data = prepare_scs_data(workflow)
    
    print("=== Layout Refiner Agent ===")
    print(f"Processing workflow: {workflow_path}")
    print(f"Total nodes: {len(workflow.get('nodes', []))}")
    print(f"Total groups: {len(workflow.get('groups', []))}")
    print()
    
    # Initialize collision detector
    detector = AABBCollisionDetector(min_padding=80, grid_size=50, max_iterations=100)
    
    # Run collision detection and resolution
    print("Running collision detection...")
    result = detector.resolve_collisions(scs_data)
    
    # Report results
    print(f"\nCollision Resolution Results:")
    print(f"- Iterations: {result['iterations']}")
    print(f"- Nodes adjusted: {len(result['refinements_applied'])}")
    print(f"\nLayout Metrics:")
    for metric, value in result['layout_metrics'].items():
        print(f"- {metric}: {value}")
    
    # Show refinements
    if result['refinements_applied']:
        print(f"\nRefinements Applied ({len(result['refinements_applied'])}):")
        for i, ref in enumerate(result['refinements_applied'][:5]):  # Show first 5
            print(f"{i+1}. Node {ref['node_id']}:")
            print(f"   From: {ref['original_position']}")
            print(f"   To: {ref['refined_position']}")
            print(f"   Reason: {ref['adjustment_reason']}")
        if len(result['refinements_applied']) > 5:
            print(f"   ... and {len(result['refinements_applied']) - 5} more adjustments")
    
    # Save refined workflow
    output_dir = os.path.join(os.path.dirname(workflow_path), "..", f"v5_{datetime.now().strftime('%Y%m%d_%H%M%S')}_collision_refined")
    os.makedirs(output_dir, exist_ok=True)
    
    refined_workflow_path = os.path.join(output_dir, "workflow_collision_refined.json")
    with open(refined_workflow_path, 'w') as f:
        json.dump(scs_data['workflow_state']['current_graph'], f, indent=2)
    
    # Save refinement report
    report_path = os.path.join(output_dir, "collision_refinement_report.json")
    report = {
        "timestamp": datetime.now().isoformat(),
        "source_workflow": workflow_path,
        "refined_workflow": refined_workflow_path,
        "collision_detection_results": result,
        "scs_metadata": scs_data['session_metadata']
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n[SUCCESS] Refined workflow saved to: {refined_workflow_path}")
    print(f"[SUCCESS] Refinement report saved to: {report_path}")
    
    # Generate summary markdown
    summary_path = os.path.join(output_dir, "layout_refinement_summary.md")
    with open(summary_path, 'w') as f:
        f.write("# Layout Refinement Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Collision Detection Results\n\n")
        f.write(f"- **Iterations Required**: {result['iterations']}\n")
        f.write(f"- **Nodes Adjusted**: {len(result['refinements_applied'])}\n")
        f.write(f"- **Total Canvas Width**: {result['layout_metrics']['total_width']}px\n")
        f.write(f"- **Total Canvas Height**: {result['layout_metrics']['total_height']}px\n")
        f.write(f"- **Node Density**: {result['layout_metrics']['node_density']}\n")
        f.write(f"- **Grid Alignment Score**: {result['layout_metrics']['alignment_score']}\n\n")
        
        if result['refinements_applied']:
            f.write("## Sample Refinements\n\n")
            for i, ref in enumerate(result['refinements_applied'][:10]):
                f.write(f"### {i+1}. Node {ref['node_id']}\n")
                f.write(f"- Original: `{ref['original_position']}`\n")
                f.write(f"- Refined: `{ref['refined_position']}`\n")
                f.write(f"- Reason: {ref['adjustment_reason']}\n\n")
    
    print(f"[SUCCESS] Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()