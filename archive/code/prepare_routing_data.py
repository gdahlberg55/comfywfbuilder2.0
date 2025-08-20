import json

# Load the workflow
with open('wan_with_notes.json', 'r') as f:
    workflow = json.load(f)

# Extract nodes and links
nodes = workflow['nodes']
links = workflow['links']

# Create SCS data structure
scs_data = {
    "workflow_state": {
        "current_graph": {
            "nodes": {str(node['id']): node for node in nodes},
            "links": links
        }
    },
    "layout_parameters": {
        "spacing_recommendation": "extreme_plus",
        "calculated_spacing": {
            "horizontal": 2000,
            "vertical": 400,
            "group_padding": 120,
            "data_bus_lane_height": 150
        },
        "layout_type": "data_bus_with_stages",
        "grid_size": 50,
        "data_bus_lanes": {
            "MODEL": {"y": -2000, "color": "#FFB6C1"},
            "CLIP": {"y": -1600, "color": "#98D8C8"},
            "VAE": {"y": -1200, "color": "#F7DC6F"},
            "IMAGE": {"y": -800, "color": "#BB8FCE"},
            "LATENT": {"y": -400, "color": "#85C1E2"},
            "CONDITIONING": {"y": 0, "color": "#F8C471"},
            "CONTROL": {"y": 400, "color": "#ABEBC6"}
        }
    }
}

# Save prepared data
with open('output/workflows/v4_20250815_data_bus_routing/scs_data_for_routing.json', 'w') as f:
    json.dump(scs_data, f, indent=2)

print(f"Prepared SCS data with {len(nodes)} nodes and {len(links)} links")
print(f"Node types found: {set(node['type'] for node in nodes)}")