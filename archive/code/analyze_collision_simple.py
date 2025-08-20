"""
Simple analysis of collision detection results without visualization
"""
import json
import os
from datetime import datetime

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def analyze_collision_report(report_path):
    """Analyze the collision refinement report"""
    report = load_json(report_path)
    results = report['collision_detection_results']
    
    print("=== Collision Detection Analysis ===\n")
    
    # Basic stats
    print(f"Total refinements: {len(results['refinements_applied'])}")
    print(f"Iterations used: {results['iterations']} (hit max limit: {results['iterations'] >= 100})")
    print(f"\nLayout metrics:")
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
        print(f"  - Average X movement: {sum(x_moves)/len(x_moves):.1f}px")
        print(f"  - Average Y movement: {sum(y_moves)/len(y_moves):.1f}px")
        print(f"  - Average distance: {sum(distances)/len(distances):.1f}px")
        print(f"  - Max distance: {max(distances):.1f}px")
        
        # Collision pairs
        collision_pairs = {}
        for move in movements:
            reason = move['adjustment_reason']
            if 'Resolved collision with' in reason:
                collider = reason.split('Resolved collision with ')[-1]
                collision_pairs[collider] = collision_pairs.get(collider, 0) + 1
        
        print(f"\nMost frequent collision sources (top 20):")
        sorted_pairs = sorted(collision_pairs.items(), key=lambda x: x[1], reverse=True)
        for i, (collider, count) in enumerate(sorted_pairs[:20]):
            print(f"  {i+1}. {collider}: {count} collisions")
        
        # Node collision frequency
        node_collisions = {}
        for move in movements:
            node_id = move['node_id']
            node_collisions[node_id] = node_collisions.get(node_id, 0) + 1
        
        print(f"\nMost moved nodes (top 20):")
        sorted_nodes = sorted(node_collisions.items(), key=lambda x: x[1], reverse=True)
        for i, (node_id, count) in enumerate(sorted_nodes[:20]):
            print(f"  {i+1}. Node {node_id}: moved {count} times")

def compare_layouts(original_path, refined_path):
    """Compare original and refined layouts"""
    original = load_json(original_path)
    refined = load_json(refined_path)
    
    print("\n=== Layout Comparison ===\n")
    
    # Build position maps
    orig_positions = {}
    refined_positions = {}
    
    for node in original.get('nodes', []):
        node_id = str(node.get('id'))
        orig_positions[node_id] = node.get('pos', [0, 0])
    
    for node in refined.get('nodes', []):
        node_id = str(node.get('id'))
        refined_positions[node_id] = node.get('pos', [0, 0])
    
    # Calculate bounds
    def get_bounds(positions):
        if not positions:
            return 0, 0, 0, 0
        xs = [p[0] for p in positions.values()]
        ys = [p[1] for p in positions.values()]
        return min(xs), min(ys), max(xs), max(ys)
    
    orig_bounds = get_bounds(orig_positions)
    refined_bounds = get_bounds(refined_positions)
    
    print(f"Original layout bounds:")
    print(f"  - X: {orig_bounds[0]} to {orig_bounds[2]} (width: {orig_bounds[2] - orig_bounds[0]})")
    print(f"  - Y: {orig_bounds[1]} to {orig_bounds[3]} (height: {orig_bounds[3] - orig_bounds[1]})")
    
    print(f"\nRefined layout bounds:")
    print(f"  - X: {refined_bounds[0]} to {refined_bounds[2]} (width: {refined_bounds[2] - refined_bounds[0]})")
    print(f"  - Y: {refined_bounds[1]} to {refined_bounds[3]} (height: {refined_bounds[3] - refined_bounds[1]})")
    
    # Find nodes with largest movements
    movements = []
    for node_id in orig_positions:
        if node_id in refined_positions:
            orig = orig_positions[node_id]
            new = refined_positions[node_id]
            dist = ((new[0] - orig[0])**2 + (new[1] - orig[1])**2)**0.5
            if dist > 0:
                movements.append((node_id, orig, new, dist))
    
    movements.sort(key=lambda x: x[3], reverse=True)
    
    print(f"\nLargest node movements (top 10):")
    for i, (node_id, orig, new, dist) in enumerate(movements[:10]):
        print(f"  {i+1}. Node {node_id}: {dist:.1f}px")
        print(f"     From: {orig} -> To: {new}")

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
    
    print(f"Analyzing: {latest_dir}\n")
    
    # Load files
    report_path = os.path.join(refined_dir, "collision_refinement_report.json")
    workflow_path = os.path.join(refined_dir, "workflow_collision_refined.json")
    original_path = r"C:\Users\gdahl\OneDrive\Documents\Projects\ComfyUI\comfywfBuilder2.0\output\workflows\v4_20250815_data_bus_routing\workflow_with_data_buses.json"
    
    # Analyze report
    analyze_collision_report(report_path)
    
    # Compare layouts
    compare_layouts(original_path, workflow_path)
    
    print(f"\nAnalysis complete. Results saved in: {refined_dir}")

if __name__ == "__main__":
    main()