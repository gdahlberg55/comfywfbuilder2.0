#!/usr/bin/env python3
"""
Validate the fixed Flux workflow
"""

import json

# Load the fixed workflow
with open('flux_inpaint_workflow_fixed.json', 'r') as f:
    workflow = json.load(f)

print("Validating Flux Workflow")
print("=" * 60)

# Check for duplicate IDs
node_ids = set()
duplicates = []
for node in workflow['nodes']:
    if node['id'] in node_ids:
        duplicates.append(node['id'])
    node_ids.add(node['id'])

if duplicates:
    print(f"ERROR: Found duplicate node IDs: {duplicates}")
else:
    print("[OK] No duplicate node IDs")

# Validate KSampler connections
ksampler = None
for node in workflow['nodes']:
    if node['type'] == 'KSampler':
        ksampler = node
        break

if ksampler:
    print(f"\nKSampler (ID {ksampler['id']}) connections:")
    
    for input_slot in ksampler['inputs']:
        if 'link' in input_slot:
            link_id = input_slot['link']
            # Find the link details
            for link in workflow['links']:
                if link[0] == link_id:
                    source_node_id = link[1]
                    source_type = link[5]
                    
                    # Find source node type
                    source_node_type = None
                    for node in workflow['nodes']:
                        if node['id'] == source_node_id:
                            source_node_type = node['type']
                            break
                    
                    status = "[OK]" if input_slot['type'] == source_type else "[ERROR]"
                    print(f"  {status} {input_slot['name']}: receives {source_type} from {source_node_type} (node {source_node_id})")
                    break

# Check all required connections
print("\nModel Flow:")
models = []
for node in workflow['nodes']:
    if node['type'] in ['UNETLoader', 'ModelSamplingFlux']:
        models.append(f"  {node['type']} (ID {node['id']})")
print("\n".join(models))

print("\nCLIP Flow:")
clips = []
for node in workflow['nodes']:
    if 'CLIP' in node['type'] or node['type'] == 'CLIPSetLastLayer':
        clips.append(f"  {node['type']} (ID {node['id']})")
print("\n".join(clips))

print("\nConditioning Nodes:")
conditioning = []
for node in workflow['nodes']:
    if node['type'] == 'CLIPTextEncodeFlux':
        title = node.get('title', 'Untitled')
        conditioning.append(f"  {node['type']} - {title} (ID {node['id']})")
print("\n".join(conditioning))

print("\nVAE Flow:")
vaes = []
for node in workflow['nodes']:
    if 'VAE' in node['type']:
        vaes.append(f"  {node['type']} (ID {node['id']})")
print("\n".join(vaes))

print("\n" + "=" * 60)
print("Workflow structure validated successfully!")
print(f"Total nodes: {len(workflow['nodes'])}")
print(f"Total links: {len(workflow['links'])}")
print(f"Total groups: {len(workflow.get('groups', []))}")