import json
import sys
import os
sys.path.append('code_modules')

from data_bus_router import DataBusRouter

# Load the SCS data
with open('output/workflows/v4_20250815_data_bus_routing/scs_data_for_routing.json', 'r') as f:
    scs_data = json.load(f)

# Initialize router with custom data bus lanes from layout strategy
router = DataBusRouter(grid_size=50)

# Update router's data bus types with the layout strategy lanes
router.DATA_BUS_TYPES = {
    "MODEL": {"y": -2000, "color": "#FFB6C1", "priority": 1},
    "CLIP": {"y": -1600, "color": "#98D8C8", "priority": 2},
    "VAE": {"y": -1200, "color": "#F7DC6F", "priority": 3},
    "IMAGE": {"y": -800, "color": "#BB8FCE", "priority": 4},
    "LATENT": {"y": -400, "color": "#85C1E2", "priority": 5},
    "CONDITIONING": {"y": 0, "color": "#F8C471", "priority": 6},
    "CONTROL": {"y": 400, "color": "#ABEBC6", "priority": 7}
}

# Analyze connections first
nodes = scs_data["workflow_state"]["current_graph"]["nodes"]
links = scs_data["workflow_state"]["current_graph"]["links"]
analysis = router.analyze_connections(nodes, links)

print("Connection Analysis:")
print(f"Total connections: {analysis['total_connections']}")
print(f"Connections needing bus routing: {analysis['bus_routed_connections']}")
print(f"\nType distribution:")
for data_type, count in analysis['type_distribution'].items():
    print(f"  {data_type}: {count}")

print(f"\nBus utilization:")
for bus_type, info in analysis['bus_utilization'].items():
    if info['utilized']:
        print(f"  {bus_type}: Y={info['y_position']}, {info['connection_count']} connections")

# Perform routing
updated_scs = router.route_connections(scs_data)

# Extract the updated workflow
updated_workflow = {
    "id": "outfit-variation-data-bus-routed",
    "revision": 0,
    "last_node_id": 361,
    "last_link_id": 571,
    "nodes": list(updated_scs["workflow_state"]["current_graph"]["nodes"].values()),
    "links": updated_scs["workflow_state"]["current_graph"]["links"],
    "groups": [],
    "config": {},
    "extra": {
        "ds": {"scale": 1, "offset": [0, 0]}
    },
    "version": 0.4
}

# Save the routed workflow
output_path = 'output/workflows/v4_20250815_data_bus_routing/workflow_with_data_buses.json'
with open(output_path, 'w') as f:
    json.dump(updated_workflow, f, indent=2)

# Save routing report
routing_metrics = updated_scs["layout_parameters"]["orthogonal_routing_metrics"]
report = {
    "routing_summary": {
        "total_connections": routing_metrics["total_connections"],
        "bus_routed_connections": routing_metrics["bus_routed_connections"],
        "total_reroutes_added": routing_metrics["total_reroutes_added"]
    },
    "bus_utilization": analysis['bus_utilization'],
    "reroute_nodes": [
        {
            "id": r["id"],
            "position": r["pos"],
            "data_type": r.get("widgets_values", ["UNKNOWN"])[0]
        }
        for r in router.created_reroutes
    ]
}

with open('output/workflows/v4_20250815_data_bus_routing/routing_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print(f"\n[SUCCESS] Data bus routing completed!")
print(f"[SUCCESS] Added {routing_metrics['total_reroutes_added']} reroute nodes")
print(f"[SUCCESS] Routed workflow saved to: {output_path}")