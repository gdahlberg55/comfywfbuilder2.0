import json
import math
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict

class ZigzagWorkflowReorganizer:
    def __init__(self, workflow_data: dict):
        self.workflow = workflow_data
        self.nodes = {node['id']: node for node in workflow_data['nodes']}
        self.links = workflow_data['links']
        self.horizontal_spacing = 450   # Horizontal spacing between columns (slightly more for readability)
        self.vertical_spacing = 50      # 50px vertical spacing as requested
        self.grid_snap = 20             # 20px grid snap
        self.column_width = 400         # Width allocated for each column
        self.start_x = 100             # Starting X position (more centered)
        self.start_y = 100             # Starting Y position (top)
        self.max_column_height = 2000   # Maximum height before moving to next column
        
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
    
    def topological_sort(self, connections: Dict[int, Dict[str, Set[int]]]) -> List[int]:
        """Perform topological sort to get proper execution order"""
        # Calculate in-degree for each node
        in_degree = {node_id: len(conn['inputs']) for node_id, conn in connections.items()}
        
        # Queue for nodes with in-degree 0
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        sorted_nodes = []
        
        while queue:
            # Sort queue to ensure consistent ordering
            queue.sort()
            node_id = queue.pop(0)
            sorted_nodes.append(node_id)
            
            # Reduce in-degree for connected nodes
            for output_node in connections[node_id]['outputs']:
                in_degree[output_node] -= 1
                if in_degree[output_node] == 0:
                    queue.append(output_node)
        
        return sorted_nodes
    
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
            'RIFE VFI': 198,
            'CFGGuider': 98,
            'SamplerCustomAdvanced': 106,
            'BasicScheduler': 110,
            'RandomNoise': 82,
            'VAEDecode': 46,
            'KSamplerSelect': 60,
            'ColorMatchImage': 126
        }
        
        for type_name, height in type_heights.items():
            if type_name in node_type:
                return height
        
        # Default estimation
        widgets = node.get('widgets_values', [])
        widget_height = len(widgets) * 30
        
        return max(base_height + widget_height, 100)
    
    def categorize_nodes(self) -> Dict[str, List[int]]:
        """Categorize nodes by their function for better grouping"""
        categories = defaultdict(list)
        
        for node_id, node in self.nodes.items():
            node_type = node.get('type', '')
            
            # Skip note nodes from categorization (handle separately)
            if 'Note' in node_type:
                continue
                
            # Categorize based on node type
            if any(x in node_type for x in ['Loader', 'LoadImage', 'CLIPLoader', 'VAELoader', 'UnetLoader']):
                categories['loaders'].append(node_id)
            elif 'CLIPTextEncode' in node_type:
                categories['conditioning'].append(node_id)
            elif any(x in node_type for x in ['Sampler', 'CFGGuider', 'BasicScheduler', 'RandomNoise', 'SplitSigmas']):
                categories['sampling'].append(node_id)
            elif any(x in node_type for x in ['VAEDecode', 'VAEEncode']):
                categories['vae'].append(node_id)
            elif any(x in node_type for x in ['Preview', 'Save']):
                categories['output'].append(node_id)
            elif 'VideoCombine' in node_type:
                categories['video'].append(node_id)
            elif any(x in node_type for x in ['RIFE', 'Interpolat']):
                categories['interpolation'].append(node_id)
            elif any(x in node_type for x in ['Slider', 'Seed', 'mxSlider', 'Fast Groups Bypasser']):
                categories['controls'].append(node_id)
            elif any(x in node_type for x in ['ImageToVideo', 'VideoEnhance', 'VideoTeaCache', 'PatchModel', 'PathchSageAttention']):
                categories['video_processing'].append(node_id)
            elif any(x in node_type for x in ['ColorMatch', 'ImageResize', 'ImageCrop', 'ImageFromBatch', 'GetImageRange']):
                categories['image_processing'].append(node_id)
            else:
                categories['processing'].append(node_id)
        
        return dict(categories)
    
    def identify_stages(self, sorted_nodes: List[int], connections: Dict, categories: Dict) -> Dict[str, List[int]]:
        """Identify logical stages in the workflow"""
        stages = {
            'input': [],
            'preprocessing': [],
            'generation': [],
            'postprocessing': [],
            'output': []
        }
        
        for node_id in sorted_nodes:
            # Determine stage based on category and connections
            for cat, nodes in categories.items():
                if node_id in nodes:
                    if cat in ['loaders', 'controls']:
                        stages['input'].append(node_id)
                    elif cat in ['conditioning', 'video_processing']:
                        stages['preprocessing'].append(node_id)
                    elif cat in ['sampling', 'vae']:
                        stages['generation'].append(node_id)
                    elif cat in ['interpolation', 'image_processing']:
                        stages['postprocessing'].append(node_id)
                    elif cat in ['output', 'video']:
                        stages['output'].append(node_id)
                    else:
                        stages['generation'].append(node_id)
                    break
        
        return stages
    
    def reorganize(self) -> dict:
        """Main reorganization function with zigzag layout"""
        connections = self.get_node_connections()
        sorted_nodes = self.topological_sort(connections)
        categories = self.categorize_nodes()
        
        # Group nodes by processing stage
        stages = self.identify_stages(sorted_nodes, connections, categories)
        
        # Track positioned nodes and current position
        positioned_nodes = set()
        columns = []  # List of columns, each containing nodes
        current_column = []
        current_column_height = 0
        column_index = 0
        
        # Position nodes in zigzag pattern
        for node_id in sorted_nodes:
            if node_id not in self.nodes:
                continue
                
            node = self.nodes[node_id]
            node_height = self.estimate_node_height(node)
            
            # Skip notes for now (position them last)
            if 'Note' in node.get('type', ''):
                continue
            
            # Check if we need to move to next column
            if current_column_height + node_height > self.max_column_height and current_column:
                columns.append(current_column)
                current_column = []
                current_column_height = 0
                column_index += 1
            
            # Add node to current column
            current_column.append((node_id, node_height))
            current_column_height += node_height + self.vertical_spacing
            positioned_nodes.add(node_id)
        
        # Add the last column
        if current_column:
            columns.append(current_column)
        
        # Now position nodes in zigzag pattern
        for col_idx, column_nodes in enumerate(columns):
            x_pos = self.start_x + (col_idx * self.horizontal_spacing)
            
            # Determine if this column goes down (even) or up (odd)
            if col_idx % 2 == 0:
                # Even columns: top to bottom
                y_current = self.start_y
                for node_id, node_height in column_nodes:
                    node = self.nodes[node_id]
                    node['pos'] = [self.snap_to_grid(x_pos), self.snap_to_grid(y_current)]
                    y_current += node_height + self.vertical_spacing
            else:
                # Odd columns: bottom to top
                # First calculate total height to know where to start
                total_height = sum(h + self.vertical_spacing for _, h in column_nodes) - self.vertical_spacing
                y_current = self.start_y + total_height
                
                for node_id, node_height in column_nodes:
                    node = self.nodes[node_id]
                    y_current -= node_height
                    node['pos'] = [self.snap_to_grid(x_pos), self.snap_to_grid(y_current)]
                    y_current -= self.vertical_spacing
        
        # Position note nodes at the top of relevant columns
        note_nodes = [(nid, node) for nid, node in self.nodes.items() if 'Note' in node.get('type', '')]
        note_y_offset = -200  # Position notes above the main content
        
        for idx, (note_id, note) in enumerate(note_nodes):
            # Distribute notes across columns
            col_idx = min(idx, len(columns) - 1)
            x_pos = self.start_x + (col_idx * self.horizontal_spacing)
            y_pos = self.start_y + note_y_offset
            note['pos'] = [self.snap_to_grid(x_pos), self.snap_to_grid(y_pos)]
            positioned_nodes.add(note_id)
        
        # Handle any remaining unpositioned nodes
        unpositioned_x = self.start_x + (len(columns) * self.horizontal_spacing)
        unpositioned_y = self.start_y
        
        for node_id, node in self.nodes.items():
            if node_id not in positioned_nodes:
                node['pos'] = [self.snap_to_grid(unpositioned_x), self.snap_to_grid(unpositioned_y)]
                unpositioned_y += 100
        
        # Update groups if they exist
        if 'groups' in self.workflow:
            for group in self.workflow['groups']:
                self.update_group_bounds(group)
        
        # Update the workflow with new positions
        self.workflow['nodes'] = list(self.nodes.values())
        
        return self.workflow
    
    def update_group_bounds(self, group: dict):
        """Update group bounding box based on contained nodes"""
        # Find all nodes that belong to this group
        group_nodes = []
        for node_id, node in self.nodes.items():
            # Check if node position is within original group bounds
            if 'bounding' in group and len(group['bounding']) >= 4:
                orig_x, orig_y, orig_w, orig_h = group['bounding'][:4]
                node_x, node_y = node.get('pos', [0, 0])
                
                # Note: This is a simplified check, you might need more sophisticated group membership detection
                # For now, we'll just shift the group bounds
                pass
        
        # For now, just shift groups to a reasonable position
        if 'bounding' in group and len(group['bounding']) >= 4:
            # Shift group to new area
            group['bounding'][0] = self.start_x - 200  # Offset to the left
            group['bounding'][1] = self.start_y - 100  # Offset above
            # Keep width and height the same
    

def reorganize_workflow_zigzag(input_path: str, output_path: str):
    """Load, reorganize with zigzag pattern, and save workflow"""
    with open(input_path, 'r', encoding='utf-8') as f:
        workflow_data = json.load(f)
    
    reorganizer = ZigzagWorkflowReorganizer(workflow_data)
    reorganized = reorganizer.reorganize()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reorganized, f, indent=2)
    
    return reorganized


# If run directly, process the workflow
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        reorganize_workflow_zigzag(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python zigzag_workflow_reorganizer.py <input.json> <output.json>")