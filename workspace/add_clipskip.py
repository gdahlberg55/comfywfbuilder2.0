import json

# Load the workflow
with open(r"C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\output\workflows\CURRENT\seamless_loop_wan21_organized.json", 'r') as f:
    workflow = json.load(f)

# Find the next available node ID
last_node_id = workflow.get("last_node_id", 363)
new_node_id = last_node_id + 1

# Find the next available link ID
last_link_id = workflow.get("last_link_id", 599)
new_link_id_1 = last_link_id + 1
new_link_id_2 = last_link_id + 2

# Create the CLIPSetLastLayer node
# Position it between the CLIP loader (at 260, 720) and the text encoders (at 4900, 160/440)
# Good position would be around x=1200, y=900 to be in clear space
clipskip_node = {
    "id": new_node_id,
    "type": "CLIPSetLastLayer",
    "pos": [1200, 900],
    "size": [315, 82],
    "flags": {},
    "order": 29,  # After CLIP loader (28) but before text encoders (33, 34)
    "mode": 0,
    "inputs": [
        {
            "name": "clip",
            "type": "CLIP",
            "link": new_link_id_1  # Will connect from CLIP loader
        }
    ],
    "outputs": [
        {
            "name": "CLIP",
            "type": "CLIP",
            "slot_index": 0,
            "links": [272, 303]  # These will connect to the text encoders
        }
    ],
    "properties": {
        "cnr_id": "comfy-core",
        "ver": "0.3.27",
        "Node name for S&R": "CLIPSetLastLayer",
        "widget_ue_connectable": {}
    },
    "widgets_values": [-2]  # Default clip skip value of -2
}

# Add the new node to the workflow
workflow["nodes"].append(clipskip_node)

# Update the links
# Find and modify existing links
new_links = []
for link in workflow["links"]:
    if link[0] == 272:  # Link from CLIP loader to first text encoder
        # Change it to go from CLIPSetLastLayer to text encoder
        link[1] = new_node_id  # Source node is now CLIPSetLastLayer
        link[2] = 0  # Source slot
    elif link[0] == 303:  # Link from CLIP loader to second text encoder
        # Change it to go from CLIPSetLastLayer to text encoder
        link[1] = new_node_id  # Source node is now CLIPSetLastLayer
        link[2] = 0  # Source slot
    new_links.append(link)

# Add new link from CLIP loader to CLIPSetLastLayer
new_link = [
    new_link_id_1,  # Link ID
    98,  # Source node (CLIP loader)
    0,   # Source slot
    new_node_id,  # Target node (CLIPSetLastLayer)
    0,   # Target slot
    "CLIP"
]
new_links.append(new_link)

workflow["links"] = new_links

# Update the CLIP loader outputs to only connect to CLIPSetLastLayer
for node in workflow["nodes"]:
    if node["id"] == 98:  # CLIP loader
        node["outputs"][0]["links"] = [new_link_id_1]
        break

# Update last IDs
workflow["last_node_id"] = new_node_id
workflow["last_link_id"] = new_link_id_1

# Save the modified workflow
output_path = r"C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\output\workflows\CURRENT\seamless_loop_wan21_with_clipskip.json"
with open(output_path, 'w') as f:
    json.dump(workflow, f, indent=2)

print(f"Workflow with CLIPSetLastLayer node saved to: {output_path}")
print(f"Added CLIPSetLastLayer node with ID {new_node_id} at position [1200, 900]")
print(f"Clip skip value set to -2 (can be adjusted from -1 to -12)")