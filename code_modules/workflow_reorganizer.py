import json
import math
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

class WorkflowReorganizer:
    def __init__(self, workflow_data: dict):
        self.workflow = workflow_data
        self.nodes = {node['id']: node for node in workflow_data['nodes']}
        self.links = workflow_data['links']
        self.horizontal_spacing = 1700  # 1700px between stages
        self.vertical_spacing = 120     # 120px vertical spacing
        self.grid_snap = 20             # 20px grid snap
        self.y_min = -1970              # Minimum Y coordinate
        self.y_max = -940               # Maximum Y coordinate (less negative)
        
    def snap_to_grid(self, value: float) -> int:
        """Snap a value to the nearest grid point"""
        return int(round(value / self.grid_snap) * self.grid_snap)
    
    def get_node_connections(self) -> Dict[int, Dict[str, Set[int]]]:
        """Build a map of node connections"""
        connections = {}
        for node_id in self.nodes:
            connections[node_id] = {'inputs': set(), 'outputs': set()}
        
        for link in self.links:
            if len(link) >= 4:
                source_node = link[1]
                target_node = link[3]
                if source_node in connections and target_node in connections:
                    connections[source_node]['outputs'].add(target_node)
                    connections[target_node]['inputs'].add(source_node)
        
        return connections
    
    def topological_sort(self, connections: Dict[int, Dict[str, Set[int]]]) -> List[List[int]]:
        """Perform topological sort to get proper execution order in stages"""
        # Calculate in-degree for each node
        in_degree = {node_id: len(conn['inputs']) for node_id, conn in connections.items()}
        
        # Queue for nodes with in-degree 0
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        stages = []
        
        while queue:
            # Process all nodes at current depth level
            current_stage = []
            next_queue = []
            
            for node_id in queue:
                current_stage.append(node_id)
                
                # Reduce in-degree for connected nodes
                for output_node in connections[node_id]['outputs']:
                    in_degree[output_node] -= 1
                    if in_degree[output_node] == 0:
                        next_queue.append(output_node)
            
            stages.append(current_stage)
            queue = next_queue
        
        return stages
    
    def categorize_nodes(self) -> Dict[str, List[int]]:
        """Categorize nodes by their function"""
        categories = defaultdict(list)
        
        for node_id, node in self.nodes.items():
            node_type = node.get('type', '')
            
            # Categorize based on node type
            if 'Loader' in node_type or 'LoadImage' in node_type:
                categories['loaders'].append(node_id)
            elif 'CLIPTextEncode' in node_type:
                categories['conditioning'].append(node_id)
            elif 'Sampler' in node_type or 'CFGGuider' in node_type:
                categories['sampling'].append(node_id)
            elif 'VAEDecode' in node_type or 'VAEEncode' in node_type:
                categories['vae'].append(node_id)
            elif 'Preview' in node_type or 'Save' in node_type:
                categories['output'].append(node_id)
            elif 'VideoCombine' in node_type:
                categories['video'].append(node_id)
            elif 'Note' in node_type:
                categories['notes'].append(node_id)
            elif 'RIFE' in node_type or 'Interpolat' in node_type:
                categories['interpolation'].append(node_id)
            elif 'Slider' in node_type or 'Seed' in node_type:
                categories['controls'].append(node_id)
            else:
                categories['processing'].append(node_id)
        
        return dict(categories)
    
    def reorganize(self) -> dict:
        """Main reorganization function with engineering-style layout"""
        connections = self.get_node_connections()
        stages = self.topological_sort(connections)
        categories = self.categorize_nodes()
        
        # Define stage positions
        stage_positions = {}
        x_current = -1800  # Starting X position
        
        # Create position map for each stage
        for stage_idx, stage_nodes in enumerate(stages):
            stage_positions[stage_idx] = {
                'x': self.snap_to_grid(x_current),
                'nodes': stage_nodes
            }
            x_current += self.horizontal_spacing
        
        # Position nodes within each stage
        positioned_nodes = set()
        
        for stage_idx, stage_info in stage_positions.items():
            x_pos = stage_info['x']
            stage_nodes = stage_info['nodes']
            
            # Group nodes by category within the stage
            stage_by_category = defaultdict(list)
            for node_id in stage_nodes:
                for category, nodes in categories.items():
                    if node_id in nodes:
                        stage_by_category[category].append(node_id)
                        break
                else:
                    stage_by_category['other'].append(node_id)
            
            # Define category order (top to bottom)
            category_order = ['notes', 'loaders', 'controls', 'conditioning', 
                            'sampling', 'processing', 'interpolation', 
                            'vae', 'output', 'video', 'other']
            
            # Position nodes by category
            y_current = self.y_min
            
            for category in category_order:
                if category in stage_by_category:
                    nodes_in_category = stage_by_category[category]
                    
                    # Position nodes in this category
                    for node_id in nodes_in_category:
                        if node_id in positioned_nodes:
                            continue
                            
                        node = self.nodes[node_id]
                        
                        # Special handling for certain node types
                        if node.get('type') == 'Note':
                            # Keep notes at their relative positions but align X
                            old_y = node['pos'][1] if 'pos' in node else y_current
                            node['pos'] = [x_pos, self.snap_to_grid(old_y)]
                        else:
                            # Normal positioning
                            node['pos'] = [x_pos, self.snap_to_grid(y_current)]
                            node_height = self.estimate_node_height(node)
                            y_current += node_height + self.vertical_spacing
                        
                        positioned_nodes.add(node_id)
                    
                    # Add extra spacing between categories
                    if nodes_in_category and category != category_order[-1]:
                        y_current += self.vertical_spacing
            
            # Ensure we don't exceed Y bounds
            if y_current > self.y_max:
                # Compress spacing if needed
                self.compress_stage_vertically(stage_nodes, x_pos)
        
        # Handle any unpositioned nodes (shouldn't happen with proper topological sort)
        for node_id, node in self.nodes.items():
            if node_id not in positioned_nodes:
                # Place at the end
                node['pos'] = [self.snap_to_grid(x_current), self.snap_to_grid(self.y_min)]
        
        # Update the workflow with new positions
        self.workflow['nodes'] = list(self.nodes.values())
        
        return self.workflow
    
    def compress_stage_vertically(self, node_ids: List[int], x_pos: int):
        """Compress nodes vertically if they exceed bounds"""
        nodes_in_stage = [(nid, self.nodes[nid]) for nid in node_ids if nid in self.nodes]
        if not nodes_in_stage:
            return
        
        # Sort by current Y position
        nodes_in_stage.sort(key=lambda x: x[1]['pos'][1])
        
        # Calculate total height needed
        total_height = 0
        for _, node in nodes_in_stage:
            total_height += self.estimate_node_height(node)
        
        total_height += self.vertical_spacing * (len(nodes_in_stage) - 1)
        
        # Calculate available space
        available_height = abs(self.y_max - self.y_min)
        
        if total_height > available_height:
            # Need to compress
            spacing = max(20, (available_height - sum(self.estimate_node_height(n[1]) for n in nodes_in_stage)) / max(1, len(nodes_in_stage) - 1))
        else:
            spacing = self.vertical_spacing
        
        # Reposition with compressed spacing
        y_current = self.y_min
        for _, node in nodes_in_stage:
            node['pos'] = [x_pos, self.snap_to_grid(y_current)]
            y_current += self.estimate_node_height(node) + spacing
    
    def estimate_node_height(self, node: dict) -> int:
        """Estimate node height based on type and widgets"""
        base_height = 50
        
        # Check for collapsed state
        if node.get('flags', {}).get('collapsed', False):
            return base_height
        
        # Get actual size if available
        if 'size' in node and isinstance(node['size'], list) and len(node['size']) >= 2:
            return int(node['size'][1])
        
        # Estimate based on node type
        node_type = node.get('type', '')
        
        # Known node type heights
        type_heights = {
            'PreviewImage': 300,
            'VHS_VideoCombine': 800,
            'CLIPTextEncode': 200,
            'Note': 150,
            'LoadImage': 360,
            'ImageResizeKJ': 266,
            'WanImageToVideo_F2': 206,
            'RIFE VFI': 198
        }
        
        for type_name, height in type_heights.items():
            if type_name in node_type:
                return height
        
        # Default estimation
        widgets = node.get('widgets_values', [])
        widget_height = len(widgets) * 30
        
        return max(base_height + widget_height, 100)


def reorganize_workflow(input_path: str, output_path: str):
    """Load, reorganize, and save workflow"""
    with open(input_path, 'r', encoding='utf-8') as f:
        workflow_data = json.load(f)
    
    reorganizer = WorkflowReorganizer(workflow_data)
    reorganized = reorganizer.reorganize()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reorganized, f, indent=2)
    
    return reorganized