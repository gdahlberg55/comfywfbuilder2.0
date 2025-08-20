"""
Data Bus Router Module for ComfyUI Workflow Layout
Version 2.0 - Implements orthogonal routing with horizontal data bus lanes
"""

import json
import math
from typing import Dict, List, Tuple, Any, Optional, Union

NodeT = Dict[str, Any]
LinkT = List[Any]  # [id, from_node, from_slot, to_node, to_slot, type]
SCS = Dict[str, Any]


class DataBusRouter:
    """Manages data bus routing and reroute node placement with orthogonal routing"""
    
    # Standard data bus types and their lane Y-coordinates
    DATA_BUS_TYPES = {
        "MODEL": {"y": -130, "color": "#FF6B6B", "priority": 1},
        "CLIP": {"y": -150, "color": "#4ECDC4", "priority": 2},
        "VAE": {"y": -170, "color": "#45B7D1", "priority": 3},
        "IMAGE": {"y": -190, "color": "#96CEB4", "priority": 4},
        "CONTEXT_PIPE": {"y": -210, "color": "#FFEAA7", "priority": 5},
        "CONDITIONING": {"y": -230, "color": "#DDA0DD", "priority": 6},
        "LATENT": {"y": -250, "color": "#98D8C8", "priority": 7}
    }
    
    def __init__(self, grid_size: int = 50):
        self.grid_size = grid_size
        self.reroute_counter = 0
        self.created_reroutes: List[NodeT] = []
        self.updated_links: List[LinkT] = []
        self.bus_utilization: Dict[str, Dict[str, Any]] = {}
    
    def _snap_to_grid(self, value: float) -> float:
        """Snap position to grid"""
        return round(value / self.grid_size) * self.grid_size
    
    def _get_node_output_pos(self, node: NodeT) -> Tuple[float, float]:
        """Get the output connection point of a node"""
        pos = node.get("pos", [0, 0])
        size = node.get("size", [200, 100])
        # Output is on the right side, middle height
        return pos[0] + size[0], pos[1] + size[1] // 2
    
    def _get_node_input_pos(self, node: NodeT) -> Tuple[float, float]:
        """Get the input connection point of a node"""
        pos = node.get("pos", [0, 0])
        size = node.get("size", [200, 100])
        # Input is on the left side, middle height
        return pos[0], pos[1] + size[1] // 2
    
    def _identify_link_type(self, link: LinkT, nodes_dict: Dict[str, NodeT]) -> str:
        """Identify the data type of a connection link"""
        # Extract link components
        if len(link) >= 6:
            link_type = link[5]
            # Map ComfyUI types to our data bus types
            type_mapping = {
                "MODEL": "MODEL",
                "CLIP": "CLIP",
                "VAE": "VAE",
                "IMAGE": "IMAGE",
                "LATENT": "LATENT",
                "CONDITIONING": "CONDITIONING",
                "CONTEXT": "CONTEXT_PIPE"
            }
            for key, bus_type in type_mapping.items():
                if key in str(link_type).upper():
                    return bus_type
        return "UNKNOWN"
    
    def analyze_connections(self, nodes: Union[List[NodeT], Dict[str, NodeT]], 
                          links: List[LinkT]) -> Dict[str, Any]:
        """
        Analyze all connections to identify data types and routing needs
        
        Args:
            nodes: List or dict of workflow nodes
            links: List of connection links
        
        Returns:
            Analysis of connections requiring data bus routing
        """
        # Normalize nodes to dict
        if isinstance(nodes, list):
            nodes_dict = {str(node.get('id', i)): node for i, node in enumerate(nodes)}
        else:
            nodes_dict = nodes
            
        routing_analysis = []
        type_counts = {}
        
        for i, link in enumerate(links):
            if len(link) < 6:
                continue
                
            link_id = link[0] if link[0] is not None else i
            from_node_id = str(link[1])
            from_slot = link[2]
            to_node_id = str(link[3])
            to_slot = link[4]
            
            if from_node_id not in nodes_dict or to_node_id not in nodes_dict:
                continue
            
            # Identify the data type
            data_type = self._identify_link_type(link, nodes_dict)
            
            # Count connections by type
            type_counts[data_type] = type_counts.get(data_type, 0) + 1
            
            # Check if this connection should use data bus
            if data_type in self.DATA_BUS_TYPES:
                from_node = nodes_dict[from_node_id]
                to_node = nodes_dict[to_node_id]
                
                from_x, from_y = self._get_node_output_pos(from_node)
                to_x, to_y = self._get_node_input_pos(to_node)
                
                # Determine if bus routing is beneficial
                distance = abs(to_x - from_x) + abs(to_y - from_y)  # Manhattan distance
                vertical_distance = abs(to_y - from_y)
                
                # Route through bus if: long distance, large vertical gap, or crosses multiple nodes
                needs_bus = (
                    distance > 400 or
                    vertical_distance > 200 or
                    (to_y < 0 and from_y > 100)  # From positive to negative Y
                )
                
                if needs_bus:
                    routing_analysis.append({
                        'link_id': link_id,
                        'from_node': from_node_id,
                        'to_node': to_node_id,
                        'from_slot': from_slot,
                        'to_slot': to_slot,
                        'data_type': data_type,
                        'bus_y': self.DATA_BUS_TYPES[data_type]['y'],
                        'distance': distance,
                        'from_pos': [from_x, from_y],
                        'to_pos': [to_x, to_y]
                    })
        
        # Update bus utilization
        for bus_type, info in self.DATA_BUS_TYPES.items():
            self.bus_utilization[bus_type] = {
                'y_position': info['y'],
                'utilized': bus_type in [r['data_type'] for r in routing_analysis],
                'connection_count': type_counts.get(bus_type, 0),
                'color': info['color']
            }
        
        return {
            'total_connections': len(links),
            'bus_routed_connections': len(routing_analysis),
            'routing_analysis': routing_analysis,
            'type_distribution': type_counts,
            'bus_utilization': self.bus_utilization
        }
    
    def _create_reroute_node(self, x: float, y: float, data_type: str = "UNKNOWN") -> NodeT:
        """Create a reroute node at specified position"""
        self.reroute_counter += 1
        node_id = f"reroute_{self.reroute_counter}"
        
        reroute = {
            "id": node_id,
            "type": "Reroute",
            "pos": [self._snap_to_grid(x), self._snap_to_grid(y)],
            "size": [75, 26],  # Standard reroute size
            "flags": {},
            "order": 0,
            "mode": 0,
            "outputs": [{"name": "", "type": "*", "links": [], "slot_index": 0}],
            "inputs": [{"name": "", "type": "*", "link": None}],
            "properties": {
                "showOutputText": False,
                "horizontal": False
            },
            "widgets_values": [data_type]  # Store data type for visualization
        }
        
        self.created_reroutes.append(reroute)
        return reroute
    
    def _create_orthogonal_path(self, routing_info: Dict[str, Any]) -> List[NodeT]:
        """
        Create orthogonal routing path using data bus lanes
        
        Returns list of reroute nodes for the path
        """
        from_x, from_y = routing_info['from_pos']
        to_x, to_y = routing_info['to_pos']
        bus_y = routing_info['bus_y']
        data_type = routing_info['data_type']
        
        reroutes = []
        
        # Determine routing strategy based on positions
        if from_y > bus_y and to_y > bus_y:
            # Both nodes above bus - route down to bus, along bus, then up
            # 1. Down from source to bus
            r1 = self._create_reroute_node(from_x, bus_y, data_type)
            reroutes.append(r1)
            
            # 2. Along bus if needed
            if abs(to_x - from_x) > 100:
                r2 = self._create_reroute_node(to_x, bus_y, data_type)
                reroutes.append(r2)
            
            # 3. Up from bus to target
            if abs(to_y - bus_y) > 50:
                r3 = self._create_reroute_node(to_x, to_y, data_type)
                reroutes.append(r3)
                
        elif from_y < bus_y < to_y:
            # Source below bus, target above - route up through bus
            # 1. Up to bus
            r1 = self._create_reroute_node(from_x, bus_y, data_type)
            reroutes.append(r1)
            
            # 2. Along bus
            if abs(to_x - from_x) > 100:
                r2 = self._create_reroute_node(to_x, bus_y, data_type)
                reroutes.append(r2)
            
            # 3. Continue up to target
            r3 = self._create_reroute_node(to_x, to_y, data_type)
            reroutes.append(r3)
            
        else:
            # Simple L-shaped routing
            if abs(to_x - from_x) > abs(to_y - from_y):
                # Horizontal first
                r1 = self._create_reroute_node(to_x, from_y, data_type)
                reroutes.append(r1)
            else:
                # Vertical first
                r1 = self._create_reroute_node(from_x, to_y, data_type)
                reroutes.append(r1)
        
        return reroutes
    
    def route_connections(self, scs_data: SCS) -> SCS:
        """
        Main routing function that adds reroute nodes to the workflow
        
        Args:
            scs_data: Shared Context System data
            
        Returns:
            Updated SCS data with reroute nodes added
        """
        # Extract workflow data
        graph = scs_data.get("workflow_state", {}).get("current_graph", {})
        nodes_raw = graph.get("nodes", [])
        links = graph.get("links", [])
        
        # Normalize nodes to list and dict formats
        if isinstance(nodes_raw, dict):
            nodes_list = list(nodes_raw.values())
            nodes_dict = nodes_raw
        else:
            nodes_list = nodes_raw
            nodes_dict = {str(node.get('id', i)): node for i, node in enumerate(nodes_list)}
        
        # Analyze connections
        analysis = self.analyze_connections(nodes_dict, links)
        
        # Generate reroute nodes for each connection needing routing
        link_id_mapping = {}  # Maps old link IDs to new link configurations
        next_link_id = max([link[0] for link in links if link[0] is not None], default=0) + 1
        
        for routing_info in analysis['routing_analysis']:
            # Create orthogonal path with reroute nodes
            reroute_nodes = self._create_orthogonal_path(routing_info)
            
            if not reroute_nodes:
                continue
            
            # Build new link chain
            old_link_id = routing_info['link_id']
            from_node_id = routing_info['from_node']
            to_node_id = routing_info['to_node']
            from_slot = routing_info['from_slot']
            to_slot = routing_info['to_slot']
            data_type = routing_info['data_type']
            
            # Create link segments
            new_links = []
            
            # First segment: from source to first reroute
            if reroute_nodes:
                new_links.append([
                    next_link_id,
                    int(from_node_id) if from_node_id.isdigit() else from_node_id,
                    from_slot,
                    reroute_nodes[0]['id'],
                    0,  # Reroute input slot
                    data_type
                ])
                next_link_id += 1
                
                # Intermediate segments between reroutes
                for i in range(len(reroute_nodes) - 1):
                    new_links.append([
                        next_link_id,
                        reroute_nodes[i]['id'],
                        0,  # Reroute output slot
                        reroute_nodes[i + 1]['id'],
                        0,  # Next reroute input slot
                        data_type
                    ])
                    next_link_id += 1
                
                # Final segment: from last reroute to target
                new_links.append([
                    next_link_id,
                    reroute_nodes[-1]['id'],
                    0,  # Reroute output slot
                    int(to_node_id) if to_node_id.isdigit() else to_node_id,
                    to_slot,
                    data_type
                ])
                next_link_id += 1
                
                link_id_mapping[old_link_id] = new_links
        
        # Update the workflow with new nodes and links
        if self.created_reroutes:
            # Add reroute nodes to the workflow
            if isinstance(nodes_raw, dict):
                for reroute in self.created_reroutes:
                    nodes_dict[reroute['id']] = reroute
                graph['nodes'] = nodes_dict
            else:
                graph['nodes'] = nodes_list + self.created_reroutes
            
            # Replace old links with new routed links
            new_links_list = []
            for link in links:
                if link[0] in link_id_mapping:
                    # Replace with new routed links
                    new_links_list.extend(link_id_mapping[link[0]])
                else:
                    # Keep original link
                    new_links_list.append(link)
            
            graph['links'] = new_links_list
        
        # Update layout parameters with bus utilization
        layout_params = scs_data.setdefault("layout_parameters", {})
        layout_params["data_bus_lanes"] = self.bus_utilization
        layout_params["orthogonal_routing_metrics"] = {
            "total_reroutes_added": len(self.created_reroutes),
            "bus_routed_connections": analysis['bus_routed_connections'],
            "total_connections": analysis['total_connections']
        }
        
        return scs_data


def main(scs_data: SCS) -> Dict[str, Any]:
    """
    Entry point for MCP code execution.
    Returns the status wrapper shape that the calling agent expects.
    """
    try:
        # Initialize router
        router = DataBusRouter(grid_size=50)
        
        # Perform routing and update SCS data
        updated_scs = router.route_connections(scs_data)
        
        # Extract metrics from updated SCS
        layout_params = updated_scs.get("layout_parameters", {})
        routing_metrics = layout_params.get("orthogonal_routing_metrics", {})
        bus_lanes = layout_params.get("data_bus_lanes", {})
        
        # Prepare detailed routing results
        routing_details = []
        for reroute in router.created_reroutes:
            routing_details.append({
                "node_id": reroute["id"],
                "position": reroute["pos"],
                "data_type": reroute.get("widgets_values", ["UNKNOWN"])[0],
                "purpose": "Data bus routing node"
            })
        
        return {
            "success": True,
            "reroutes_added": routing_details,
            "routing_metrics": routing_metrics,
            "data_bus_lanes": bus_lanes,
            "total_reroutes": len(router.created_reroutes),
            # Provide updated scs back for convenience if caller wants to overwrite
            "scs_data": updated_scs
        }
        
    except Exception as e:
        # On failure, still return a consistent shape
        return {
            "success": False,
            "error": str(e),
            "reroutes_added": [],
            "routing_metrics": {
                "total_reroutes_added": 0,
                "bus_routed_connections": 0,
                "total_connections": 0
            },
            "data_bus_lanes": {},
            "total_reroutes": 0,
            "scs_data": scs_data
        }