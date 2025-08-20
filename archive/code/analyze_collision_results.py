"""
Analyze collision detection results and provide insights
"""
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def visualize_workflow_layout(workflow, title="Workflow Layout", save_path=None):
    """Create a visual representation of the workflow layout"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    
    # Extract nodes
    nodes = workflow.get('nodes', [])
    
    # Color scheme for different node types
    colors = {
        'LoadImage': '#FFE6E6',
        'SaveImage': '#E6FFE6',
        'CLIPTextEncode': '#E6E6FF',
        'KSampler': '#FFFFE6',
        'VAEDecode': '#FFE6FF',
        'VAEEncode': '#E6FFFF',
        'CheckpointLoaderSimple': '#FFD700',
        'LoraLoader': '#FFA500',
        'ControlNet': '#FF69B4',
        'IPAdapter': '#9370DB',
        'Reroute': '#D3D3D3',
        'default': '#F0F0F0'
    }
    
    # Plot nodes
    for node in nodes:
        if isinstance(node, dict):
            node_id = node.get('id', 'unknown')
            node_type = node.get('type', 'unknown')
            pos = node.get('pos', [0, 0])
            size = node.get('size', [200, 100])
            
            # Get size properly
            if isinstance(size, dict):
                width = float(size.get('0', size.get(0, 200)))
                height = float(size.get('1', size.get(1, 100)))
            elif isinstance(size, list) and len(size) >= 2:
                width = float(size[0])
                height = float(size[1])
            else:
                width, height = 200, 100
            
            x, y = float(pos[0]), float(pos[1])
            
            # Determine color
            color = colors.get('default')
            for key in colors:
                if key in node_type:
                    color = colors[key]
                    break
            
            # Draw node
            rect = Rectangle((x, -y-height), width, height, 
                           facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            
            # Add label
            ax.text(x + width/2, -y - height/2, f"{node_id}\n{node_type[:20]}", 
                   ha='center', va='center', fontsize=6, wrap=True)
    
    # Set axis properties
    ax.set_aspect('equal')
    ax.autoscale_view()
    ax.set_title(title, fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Position (pixels)')
    ax.set_ylabel('Y Position (pixels)')
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def analyze_collision_report(report_path):
    """Analyze the collision refinement report"""
    report = load_json(report_path)
    results = report['collision_detection_results']
    
    print("=== Collision Detection Analysis ===\n")
    
    # Basic stats
    print(f"Total refinements: {len(results['refinements_applied'])}")
    print(f"Iterations used: {results['iterations']} (max: 100)")
    print(f"Layout metrics:")
    for metric, value in results['layout_metrics'].items():
        print(f"  - {metric}: {value}")
    
    # Analyze movement patterns
    movements = results['refinements_applied']
    if movements:
        x_moves = []
        y_moves = []
        distances = []
        
        for move in movements[:1000]:  # Analyze first 1000 to avoid too much data
            orig = move['original_position']
            new = move['refined_position']
            dx = new[0] - orig[0]
            dy = new[1] - orig[1]
            dist = (dx**2 + dy**2)**0.5
            
            x_moves.append(dx)
            y_moves.append(dy)
            distances.append(dist)
        
        print(f"\nMovement Analysis (first 1000 adjustments):")
        print(f"  - Average X movement: {np.mean(x_moves):.1f}px")
        print(f"  - Average Y movement: {np.mean(y_moves):.1f}px")
        print(f"  - Average distance: {np.mean(distances):.1f}px")
        print(f"  - Max distance: {max(distances):.1f}px")
        
        # Collision pairs
        collision_pairs = {}
        for move in movements:
            reason = move['adjustment_reason']
            if 'Resolved collision with' in reason:
                collider = reason.split('Resolved collision with ')[-1]
                collision_pairs[collider] = collision_pairs.get(collider, 0) + 1
        
        print(f"\nMost frequent collision sources (top 10):")
        sorted_pairs = sorted(collision_pairs.items(), key=lambda x: x[1], reverse=True)
        for collider, count in sorted_pairs[:10]:
            print(f"  - {collider}: {count} collisions")

def main():
    # Paths
    base_dir = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows"
    
    # Find the latest collision refined directory
    refined_dirs = [d for d in os.listdir(base_dir) if d.startswith('v5_') and 'collision_refined' in d]
    if not refined_dirs:
        print("No collision refined workflows found!")
        return
    
    latest_dir = sorted(refined_dirs)[-1]
    refined_dir = os.path.join(base_dir, latest_dir)
    
    # Load files
    report_path = os.path.join(refined_dir, "collision_refinement_report.json")
    workflow_path = os.path.join(refined_dir, "workflow_collision_refined.json")
    
    # Analyze report
    analyze_collision_report(report_path)
    
    # Load workflows for comparison
    original_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v4_20250815_data_bus_routing\workflow_with_data_buses.json"
    original_workflow = load_json(original_path)
    refined_workflow = load_json(workflow_path)
    
    # Create visualizations
    print("\nGenerating layout visualizations...")
    
    viz_dir = os.path.join(refined_dir, "visualizations")
    os.makedirs(viz_dir, exist_ok=True)
    
    # Original layout
    visualize_workflow_layout(
        original_workflow, 
        "Original Layout (Before Collision Detection)",
        os.path.join(viz_dir, "layout_original.png")
    )
    
    # Refined layout
    visualize_workflow_layout(
        refined_workflow,
        "Refined Layout (After Collision Detection)",
        os.path.join(viz_dir, "layout_refined.png")
    )
    
    print(f"\nVisualizations saved to: {viz_dir}")

if __name__ == "__main__":
    main()