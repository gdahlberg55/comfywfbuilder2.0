import json

# Read the workflow
with open('wan_with_notes.json', 'r') as f:
    workflow = json.load(f)

# Filter out Note nodes
workflow['nodes'] = [node for node in workflow['nodes'] if node['type'] != 'Note']

# Save without notes version
with open('wan_without_notes.json', 'w') as f:
    json.dump(workflow, f, separators=(',', ':'))

print('Created wan_without_notes.json')