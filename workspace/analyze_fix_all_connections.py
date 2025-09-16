#!/usr/bin/env python3
"""
Comprehensively analyze and fix ALL missing connections in Flux workflow
"""

import json

# Load the workflow
with open('flux_txt2img_workflow.json', 'r') as f:
    workflow = json.load(f)

print("COMPREHENSIVE CONNECTION ANALYSIS")
print("=" * 60)

# Map all nodes by ID for easy lookup
nodes_by_id = {node['id']: node for node in workflow['nodes']}

# Analyze each node's requirements and connections
print("\n1. CHECKING EACH NODE'S CONNECTIONS:")
print("-" * 40)

connection_issues = []

for node in workflow['nodes']:
    node_id = node['id']
    node_type = node['type']
    print(f"\nNode {node_id}: {node_type}")
    
    # Check inputs
    if 'inputs' in node:
        for inp in node['inputs']:
            inp_name = inp['name']
            inp_type = inp['type']
            link = inp.get('link')
            
            if link:
                # Find the source of this link
                source_found = False
                for l in workflow['links']:
                    if l[0] == link:
                        source_node_id = l[1]
                        source_node = nodes_by_id.get(source_node_id)
                        if source_node:
                            print(f"  ✓ {inp_name} ({inp_type}) <- {source_node['type']} ({source_node_id})")
                            source_found = True
                        break
                if not source_found:
                    print(f"  ✗ {inp_name} ({inp_type}) <- BROKEN LINK {link}")
                    connection_issues.append((node_id, node_type, inp_name, inp_type, 'broken_link'))
            else:
                # Check if this is a required input
                if 'widget' not in inp:  # Not a widget input, needs connection
                    print(f"  ✗ {inp_name} ({inp_type}) <- NOT CONNECTED")
                    connection_issues.append((node_id, node_type, inp_name, inp_type, 'missing'))

print("\n2. REQUIRED CONNECTION CHAIN FOR FLUX:")
print("-" * 40)

# Define the proper flow for Flux text-to-image
required_flow = {
    'UNETLoader': {'outputs': ['MODEL']},
    'DualCLIPLoader': {'outputs': ['CLIP']},
    'VAELoader': {'outputs': ['VAE']},
    'ModelSamplingFlux': {
        'inputs': {'model': 'MODEL'}, 
        'outputs': ['MODEL']
    },
    'CLIPSetLastLayer': {
        'inputs': {'clip': 'CLIP'},
        'outputs': ['CLIP']
    },
    'Power Lora Loader (rgthree)': {
        'inputs': {'model': 'MODEL', 'clip': 'CLIP'},
        'outputs': ['MODEL', 'CLIP']
    },
    'CLIPTextEncodeFlux': {
        'inputs': {'clip': 'CLIP'},
        'outputs': ['CONDITIONING']
    },
    'EmptyLatentImage': {
        'outputs': ['LATENT']
    },
    'KSampler': {
        'inputs': {
            'model': 'MODEL',
            'positive': 'CONDITIONING',
            'negative': 'CONDITIONING',
            'latent_image': 'LATENT'
        },
        'outputs': ['LATENT']
    },
    'VAEDecode': {
        'inputs': {'samples': 'LATENT', 'vae': 'VAE'},
        'outputs': ['IMAGE']
    }
}

print("\n3. FIXING MISSING CONNECTIONS:")
print("-" * 40)

# Track what outputs what
outputs_available = {}
for node in workflow['nodes']:
    if 'outputs' in node:
        for output in node['outputs']:
            if output['type'] not in outputs_available:
                outputs_available[output['type']] = []
            outputs_available[output['type']].append({
                'node_id': node['id'],
                'node_type': node['type'],
                'slot': output.get('slot_index', 0)
            })

print("\nAvailable outputs by type:")
for out_type, sources in outputs_available.items():
    print(f"  {out_type}: {[s['node_type'] for s in sources]}")

# Find specific node IDs
unet_loader = next((n['id'] for n in workflow['nodes'] if n['type'] == 'UNETLoader'), None)
dual_clip = next((n['id'] for n in workflow['nodes'] if n['type'] == 'DualCLIPLoader'), None)
vae_loader = next((n['id'] for n in workflow['nodes'] if n['type'] == 'VAELoader'), None)
model_sampling = next((n['id'] for n in workflow['nodes'] if n['type'] == 'ModelSamplingFlux'), None)
clip_set = next((n['id'] for n in workflow['nodes'] if n['type'] == 'CLIPSetLastLayer'), None)
lora_loader = next((n['id'] for n in workflow['nodes'] if 'Power Lora' in n['type']), None)
empty_latent = next((n['id'] for n in workflow['nodes'] if n['type'] == 'EmptyLatentImage'), None)
ksampler = next((n['id'] for n in workflow['nodes'] if n['type'] == 'KSampler'), None)
vae_decode = next((n['id'] for n in workflow['nodes'] if n['type'] == 'VAEDecode'), None)

# Find text encode nodes
positive_encode = None
negative_encode = None
for node in workflow['nodes']:
    if node['type'] == 'CLIPTextEncodeFlux':
        if 'positive' in node.get('title', '').lower():
            positive_encode = node['id']
        elif 'negative' in node.get('title', '').lower():
            negative_encode = node['id']

print(f"\nNode IDs found:")
print(f"  UNETLoader: {unet_loader}")
print(f"  DualCLIPLoader: {dual_clip}")
print(f"  VAELoader: {vae_loader}")
print(f"  ModelSamplingFlux: {model_sampling}")
print(f"  CLIPSetLastLayer: {clip_set}")
print(f"  Power Lora Loader: {lora_loader}")
print(f"  Positive Encode: {positive_encode}")
print(f"  Negative Encode: {negative_encode}")
print(f"  EmptyLatentImage: {empty_latent}")
print(f"  KSampler: {ksampler}")
print(f"  VAEDecode: {vae_decode}")

# Create all required connections
new_link_id = max([l[0] for l in workflow['links']] if workflow['links'] else 0) + 1
required_connections = [
    # UNETLoader -> ModelSamplingFlux
    (unet_loader, 0, model_sampling, 0, 'MODEL'),
    # DualCLIPLoader -> CLIPSetLastLayer
    (dual_clip, 0, clip_set, 0, 'CLIP'),
    # ModelSamplingFlux -> Power Lora Loader
    (model_sampling, 0, lora_loader, 0, 'MODEL'),
    # CLIPSetLastLayer -> Power Lora Loader
    (clip_set, 0, lora_loader, 1, 'CLIP'),
    # Power Lora Loader -> Text Encoders
    (lora_loader, 1, positive_encode, 0, 'CLIP'),
    (lora_loader, 1, negative_encode, 0, 'CLIP'),
    # Power Lora Loader -> KSampler
    (lora_loader, 0, ksampler, 0, 'MODEL'),
    # Text Encoders -> KSampler
    (positive_encode, 0, ksampler, 1, 'CONDITIONING'),
    (negative_encode, 0, ksampler, 2, 'CONDITIONING'),
    # EmptyLatentImage -> KSampler
    (empty_latent, 0, ksampler, 3, 'LATENT'),
    # KSampler -> VAEDecode
    (ksampler, 0, vae_decode, 0, 'LATENT'),
    # VAELoader -> VAEDecode
    (vae_loader, 0, vae_decode, 1, 'VAE')
]

# Check and create missing connections
for source_id, source_slot, target_id, target_slot, link_type in required_connections:
    if source_id and target_id:
        # Check if connection exists
        exists = False
        for link in workflow['links']:
            if link[1] == source_id and link[3] == target_id and link[4] == target_slot:
                exists = True
                print(f"  ✓ Connection exists: {nodes_by_id[source_id]['type']} -> {nodes_by_id[target_id]['type']}")
                break
        
        if not exists:
            # Create new connection
            new_link = [new_link_id, source_id, source_slot, target_id, target_slot, link_type]
            workflow['links'].append(new_link)
            print(f"  + Created: {nodes_by_id[source_id]['type']} -> {nodes_by_id[target_id]['type']} ({link_type})")
            
            # Update node inputs
            target_node = nodes_by_id[target_id]
            if 'inputs' in target_node:
                for inp in target_node['inputs']:
                    if inp.get('type') == link_type:
                        # Match by slot index
                        input_names = ['model', 'positive', 'negative', 'latent_image', 'samples', 'vae', 'clip']
                        for i, name in enumerate(input_names):
                            if inp['name'] == name and i == target_slot:
                                inp['link'] = new_link_id
                                break
            
            # Update node outputs
            source_node = nodes_by_id[source_id]
            if 'outputs' in source_node:
                for output in source_node['outputs']:
                    if output.get('slot_index') == source_slot:
                        if 'links' not in output:
                            output['links'] = []
                        output['links'].append(new_link_id)
                        break
            
            new_link_id += 1

# Update last_link_id
workflow['last_link_id'] = new_link_id - 1

# Save the fully connected workflow
output_file = 'flux_txt2img_fully_connected.json'
with open(output_file, 'w') as f:
    json.dump(workflow, f, indent=2)

print(f"\n4. VALIDATION SUMMARY:")
print("-" * 40)
print(f"✓ Created fully connected workflow: {output_file}")
print(f"✓ Total nodes: {len(workflow['nodes'])}")
print(f"✓ Total connections: {len(workflow['links'])}")
print("\nComplete connection chain:")
print("  UNETLoader → ModelSamplingFlux → Power Lora Loader → KSampler")
print("  DualCLIPLoader → CLIPSetLastLayer → Power Lora Loader → Text Encoders")
print("  EmptyLatentImage → KSampler → VAEDecode")
print("  VAELoader → VAEDecode → SaveImage")