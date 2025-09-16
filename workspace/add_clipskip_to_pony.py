import json

# Load the extracted workflow
with open(r"C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\extracted_workflow.json", 'r') as f:
    workflow = json.load(f)

# Find the next available node ID
last_node_id = workflow.get("last_node_id", 28)
new_node_id = last_node_id + 1

# Find the next available link IDs (we need 2 new links)
last_link_id = workflow.get("last_link_id", 44)
new_link_id_1 = last_link_id + 1  # From second Lora Stack to CLIPSetLastLayer
new_link_id_2 = last_link_id + 2  # From CLIPSetLastLayer to negative prompt

# Create the CLIPSetLastLayer node
# Position it between the second Lora Stack (node 25) and the text encoders
# Good position would be around x=250, y=500 to be in clear space
clipskip_node = {
    "id": new_node_id,
    "type": "CLIPSetLastLayer",
    "pos": [250, 500],  # Positioned between Lora Stack and Conditioning
    "size": [315, 82],
    "flags": {},
    "order": 8,  # After second Lora Stack (7) but before text encoders (9, 10)
    "mode": 0,
    "inputs": [
        {
            "name": "clip",
            "type": "CLIP",
            "link": new_link_id_1  # Will connect from second Lora Stack
        }
    ],
    "outputs": [
        {
            "name": "CLIP",
            "type": "CLIP",
            "slot_index": 0,
            "links": [38, 42, new_link_id_2]  # Connects to both text encoders
        }
    ],
    "title": "[CLIP] Skip Last Layers",
    "properties": {
        "cnr_id": "comfy-core",
        "ver": "0.3.49",
        "Node name for S&R": "CLIPSetLastLayer",
        "ue_properties": {
            "version": "7.0.1",
            "widget_ue_connectable": {
                "stop_at_clip_layer": True
            }
        }
    },
    "widgets_values": [-2]  # Default clip skip value of -2
}

# Add the new node to the workflow
workflow["nodes"].append(clipskip_node)

# Update the links
new_links = []
for link in workflow["links"]:
    # Update links from second Lora Stack (node 25) CLIP output
    if link[0] == 38:  # Link from Lora Stack to negative text encoder
        # Change source to CLIPSetLastLayer
        link[1] = new_node_id
        link[2] = 0
    elif link[0] == 42:  # Link from Lora Stack to positive text encoder
        # Change source to CLIPSetLastLayer
        link[1] = new_node_id
        link[2] = 0
    new_links.append(link)

# Add new link from second Lora Stack to CLIPSetLastLayer
new_link = [
    new_link_id_1,  # Link ID
    25,  # Source node (second Lora Stack)
    1,   # Source slot (CLIP output)
    new_node_id,  # Target node (CLIPSetLastLayer)
    0,   # Target slot
    "CLIP"
]
new_links.append(new_link)

workflow["links"] = new_links

# Update the second Lora Stack outputs to only connect to CLIPSetLastLayer
for node in workflow["nodes"]:
    if node["id"] == 25:  # Second Lora Stack
        node["outputs"][1]["links"] = [new_link_id_1]  # CLIP output now only goes to CLIPSetLastLayer
        break

# Update last IDs
workflow["last_node_id"] = new_node_id
workflow["last_link_id"] = new_link_id_1

# Save the modified workflow
output_path = r"C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\pony_workflow_with_clipskip.json"
with open(output_path, 'w') as f:
    json.dump(workflow, f, indent=2)

print(f"Workflow with CLIPSetLastLayer node saved to: {output_path}")
print(f"Added CLIPSetLastLayer node with ID {new_node_id} at position [250, 500]")
print(f"Clip skip value set to -2 (can be adjusted from -1 to -12 in ComfyUI)")