#!/usr/bin/env python3
"""
Add image generation capability to Flux inpainting workflow
Creates a dual-purpose workflow: generate OR inpaint
"""

import json

# Load the current workflow
with open('flux_inpaint_workflow_with_clipskip.json', 'r') as f:
    workflow = json.load(f)

print("Adding image generation capability to Flux workflow...")
print("=" * 60)

# Find next available ID
max_id = workflow['last_node_id']
next_id = max_id + 1

# Add EmptyLatentImage node for generation
empty_latent = {
    "id": next_id,
    "type": "EmptyLatentImage",
    "pos": [600, 700],  # Below the inpaint input group
    "size": [315, 106],
    "flags": {},
    "order": 3,
    "mode": 0,
    "outputs": [
        {
            "name": "LATENT",
            "type": "LATENT",
            "slot_index": 0,
            "links": []  # Will be connected via switch
        }
    ],
    "title": "[Generation] Empty Latent",
    "properties": {
        "Node name for S&R": "EmptyLatentImage"
    },
    "widgets_values": [
        1024,  # width
        1024,  # height
        1     # batch_size
    ]
}
workflow['nodes'].append(empty_latent)
empty_latent_id = next_id
next_id += 1

# Add a switch node to choose between generation and inpainting
switch_node = {
    "id": next_id,
    "type": "LatentSwitch",
    "pos": [750, 450],
    "size": [200, 100],
    "flags": {},
    "order": 8,
    "mode": 0,
    "inputs": [
        {
            "name": "input1",
            "type": "LATENT",
            "link": None  # Will connect to VAEEncodeForInpaint
        },
        {
            "name": "input2", 
            "type": "LATENT",
            "link": None  # Will connect to EmptyLatentImage
        }
    ],
    "outputs": [
        {
            "name": "LATENT",
            "type": "LATENT",
            "slot_index": 0,
            "links": []  # Will connect to KSampler
        }
    ],
    "title": "[Switch] Gen/Inpaint Mode",
    "properties": {
        "Node name for S&R": "LatentSwitch"
    },
    "widgets_values": [
        1  # 1 = inpaint (default), 2 = generation
    ]
}

# Check if LatentSwitch exists, if not use a simpler approach
# Since LatentSwitch might not be available, let's use reroute nodes instead

# Add reroute nodes for switching
reroute1 = {
    "id": next_id,
    "type": "Reroute",
    "pos": [800, 400],
    "size": [75, 26],
    "flags": {},
    "order": 7,
    "mode": 0,
    "inputs": [
        {
            "name": "",
            "type": "*",
            "link": None
        }
    ],
    "outputs": [
        {
            "name": "",
            "type": "LATENT",
            "slot_index": 0,
            "links": []
        }
    ],
    "title": "Latent Route",
    "properties": {
        "showOutputText": False,
        "horizontal": False
    }
}
workflow['nodes'].append(reroute1)
reroute_id = next_id
next_id += 1

# Add note explaining how to switch modes
note_node = {
    "id": next_id,
    "type": "Note",
    "pos": [570, 850],
    "size": [380, 140],
    "flags": {},
    "order": 0,
    "mode": 0,
    "title": "Mode Selection",
    "properties": {
        "text": ""
    },
    "widgets_values": [
        "WORKFLOW MODES:\n\n1. INPAINTING MODE (default):\n   - Latent Route connected to VAEEncodeForInpaint\n   - Load image and mask\n\n2. GENERATION MODE:\n   - Disconnect Latent Route from VAEEncodeForInpaint\n   - Connect Latent Route to Empty Latent\n   - Set dimensions in Empty Latent node"
    ],
    "color": "#432",
    "bgcolor": "#653"
}
workflow['nodes'].append(note_node)
note_id = next_id
next_id += 1

# Find VAEEncodeForInpaint node
vae_encode_id = None
for node in workflow['nodes']:
    if node['type'] == 'VAEEncodeForInpaint':
        vae_encode_id = node['id']
        break

# Find KSampler node
ksampler_id = None
ksampler_latent_link = None
for node in workflow['nodes']:
    if node['type'] == 'KSampler':
        ksampler_id = node['id']
        # Find current latent input link
        for inp in node['inputs']:
            if inp['name'] == 'latent_image':
                ksampler_latent_link = inp.get('link')
                break
        break

# Update connections
# 1. Connect VAEEncodeForInpaint to reroute
new_link_id = workflow['last_link_id'] + 1
workflow['links'].append([
    new_link_id,
    vae_encode_id,
    0,  # output slot
    reroute_id,
    0,  # input slot
    "LATENT"
])

# Update VAEEncodeForInpaint output links
for node in workflow['nodes']:
    if node['id'] == vae_encode_id:
        if 'outputs' in node and len(node['outputs']) > 0:
            node['outputs'][0]['links'] = [new_link_id]
        break

# 2. Connect reroute to KSampler
new_link_id += 1
workflow['links'].append([
    new_link_id,
    reroute_id,
    0,  # output slot
    ksampler_id,
    3,  # latent_image input slot
    "LATENT"
])

# Update reroute output links
for node in workflow['nodes']:
    if node['id'] == reroute_id:
        node['outputs'][0]['links'] = [new_link_id]
        break

# Update KSampler to use new link
for node in workflow['nodes']:
    if node['id'] == ksampler_id:
        for inp in node['inputs']:
            if inp['name'] == 'latent_image':
                inp['link'] = new_link_id
                break
        break

# Remove old direct link from VAEEncodeForInpaint to KSampler
if ksampler_latent_link:
    workflow['links'] = [link for link in workflow['links'] if link[0] != ksampler_latent_link]

# 3. Create link from EmptyLatentImage (ready to connect manually)
new_link_id += 1
empty_latent_link = new_link_id
# Don't add this link yet - user will connect manually to switch modes

# Add a new group for generation controls
generation_group = {
    "id": 8,
    "title": "Generation Mode",
    "bounding": [560, 660, 400, 330],
    "color": "#3f5159",
    "font_size": 24,
    "flags": {}
}
workflow['groups'].append(generation_group)

# Update IDs
workflow['last_node_id'] = next_id
workflow['last_link_id'] = new_link_id

# Save the dual-purpose workflow
output_file = 'flux_dual_generate_inpaint.json'
with open(output_file, 'w') as f:
    json.dump(workflow, f, indent=2)

print(f"Created dual-purpose workflow: {output_file}")
print("\nFeatures added:")
print("- EmptyLatentImage node for generation from scratch")
print("- Reroute node for switching between modes")
print("- Instructions note for mode switching")
print("- New 'Generation Mode' group")
print("\nHow to use:")
print("1. DEFAULT: Workflow is set to INPAINT mode")
print("2. TO GENERATE: Disconnect reroute from VAEEncodeForInpaint,")
print("   connect it to EmptyLatentImage instead")
print("3. Set your desired resolution in EmptyLatentImage")
print("4. Write your prompt and generate!")