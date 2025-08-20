import json
import math
from collections import defaultdict

# Load the workflow
with open(r'C:\Users\gdahl\Downloads\wan21SeamlessLoop_v12\Wan 2.1 - seamless loop workflow v1.2.json', 'r') as f:
    workflow = json.load(f)

nodes = workflow['nodes']
links = workflow['links']

# Create node lookup
node_lookup = {node['id']: node for node in nodes}

# Analyze flow patterns
node_connections = defaultdict(lambda: {'inputs': [], 'outputs': []})

for link in links:
    # link format: [link_id, source_node, source_slot, target_node, target_slot, type]
    source_node = link[1]
    target_node = link[3]
    link_type = link[5] if len(link) > 5 else 'UNKNOWN'
    
    node_connections[source_node]['outputs'].append({
        'target': target_node,
        'type': link_type,
        'slot': link[2]
    })
    
    node_connections[target_node]['inputs'].append({
        'source': source_node,
        'type': link_type,
        'slot': link[4]
    })

# Identify processing stages based on X positions
stages = defaultdict(list)
for node in nodes:
    x_pos = node['pos'][0]
    # Round to nearest 500px for stage grouping
    stage = round(x_pos / 500) * 500
    stages[stage].append(node)

# Sort stages by X position
sorted_stages = sorted(stages.items())

print("Processing Stages (by X position):")
for stage_x, stage_nodes in sorted_stages:
    print(f"\nStage at X={stage_x}:")
    for node in sorted(stage_nodes, key=lambda n: n['pos'][1]):
        print(f"  - {node['type']} (ID: {node['id']}) at Y={node['pos'][1]}")

# Identify main data buses
print("\n\nMain Data Buses:")
data_buses = {
    'MODEL': [],
    'CLIP': [],
    'VAE': [],
    'CONDITIONING': [],
    'LATENT': [],
    'IMAGE': []
}

for link in links:
    link_type = link[5] if len(link) > 5 else 'UNKNOWN'
    if link_type in data_buses:
        source_node = node_lookup[link[1]]
        target_node = node_lookup[link[3]]
        data_buses[link_type].append({
            'from': f"{source_node['type']} ({link[1]})",
            'to': f"{target_node['type']} ({link[3]})",
            'from_pos': source_node['pos'],
            'to_pos': target_node['pos']
        })

for bus_type, connections in data_buses.items():
    if connections:
        print(f"\n{bus_type} Bus ({len(connections)} connections):")
        # Calculate average Y positions for routing
        y_positions = []
        for conn in connections[:3]:  # Show first 3 connections
            print(f"  {conn['from']} -> {conn['to']}")
            y_positions.extend([conn['from_pos'][1], conn['to_pos'][1]])
        if y_positions:
            avg_y = sum(y_positions) / len(y_positions)
            print(f"  Suggested routing channel Y: {avg_y:.0f}")
