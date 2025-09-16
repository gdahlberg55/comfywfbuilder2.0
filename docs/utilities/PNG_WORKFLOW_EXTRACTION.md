# PNG Workflow Extraction Utility

## Overview
ComfyUI embeds workflow JSON data in PNG metadata, allowing workflows to be recovered from generated images. This utility extracts and validates these embedded workflows.

## Technical Implementation

### PNG Structure
PNG files consist of chunks, each with:
- Length (4 bytes)
- Type (4 bytes)
- Data (variable)
- CRC (4 bytes)

ComfyUI stores workflows in **tEXt chunks** with keyword "workflow".

### Extraction Process

```python
def extract_workflow_from_png(png_path):
    """Extract ComfyUI workflow JSON from PNG metadata"""
    with open(png_path, 'rb') as f:
        # Verify PNG signature
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            return None
        
        # Read chunks
        while True:
            # Read chunk length
            length_bytes = f.read(4)
            if not length_bytes:
                break
            
            length = struct.unpack('>I', length_bytes)[0]
            
            # Read chunk type
            chunk_type = f.read(4).decode('ascii', errors='ignore')
            
            # Read chunk data
            data = f.read(length)
            
            # Skip CRC
            f.read(4)
            
            # Process tEXt chunks
            if chunk_type == 'tEXt':
                try:
                    # Find null separator
                    null_index = data.index(b'\x00')
                    keyword = data[:null_index].decode('latin-1')
                    text = data[null_index + 1:].decode('latin-1')
                    
                    if keyword == 'workflow':
                        # Parse and return workflow JSON
                        return json.loads(text)
                except Exception:
                    continue
            
            # Stop at IEND chunk
            if chunk_type == 'IEND':
                break
    
    return None
```

## Usage Examples

### Basic Extraction
```python
workflow = extract_workflow_from_png("image.png")
if workflow:
    print(f"Found workflow with {len(workflow['nodes'])} nodes")
```

### Batch Processing
```python
from pathlib import Path

def find_workflows_in_directory(directory):
    """Find all PNG files with embedded workflows"""
    workflows = []
    for png_file in Path(directory).glob("*.png"):
        workflow = extract_workflow_from_png(png_file)
        if workflow:
            workflows.append({
                "file": png_file.name,
                "workflow": workflow,
                "node_count": len(workflow.get("nodes", []))
            })
    return workflows
```

### Workflow Validation
```python
def validate_workflow(workflow):
    """Validate extracted workflow structure"""
    required_keys = ["nodes", "links", "groups", "config"]
    
    # Check structure
    if not all(key in workflow for key in required_keys):
        return False, "Missing required keys"
    
    # Check nodes have positions
    for node in workflow.get("nodes", []):
        if "pos" not in node or "size" not in node:
            return False, f"Node {node.get('id')} missing layout data"
    
    # Check Frontend/UI format
    if not any("widgets_values" in node for node in workflow.get("nodes", [])):
        return False, "Appears to be API format, not Frontend/UI"
    
    return True, "Valid workflow"
```

## Integration with Workflow Modification

### Adding Nodes to Extracted Workflows
```python
def add_clipskip_to_workflow(workflow):
    """Add CLIPSetLastLayer node to extracted workflow"""
    # Find next IDs
    last_node_id = workflow.get("last_node_id", 0)
    last_link_id = workflow.get("last_link_id", 0)
    
    # Create CLIPSetLastLayer node
    clipskip_node = {
        "id": last_node_id + 1,
        "type": "CLIPSetLastLayer",
        "pos": [250, 500],  # Position in clear space
        "size": [315, 82],
        "flags": {},
        "order": 10,
        "mode": 0,
        "inputs": [
            {"name": "clip", "type": "CLIP", "link": None}
        ],
        "outputs": [
            {"name": "CLIP", "type": "CLIP", "slot_index": 0, "links": []}
        ],
        "title": "[CLIP] Skip Last Layers",
        "properties": {
            "Node name for S&R": "CLIPSetLastLayer"
        },
        "widgets_values": [-2]  # Default clip skip
    }
    
    # Add to workflow
    workflow["nodes"].append(clipskip_node)
    workflow["last_node_id"] = last_node_id + 1
    
    # Update connections (simplified example)
    # ... connection logic here ...
    
    return workflow
```

## Complete Example Script

```python
#!/usr/bin/env python3
"""
PNG Workflow Extractor and Modifier
Extracts ComfyUI workflows from PNG files and adds clip skip functionality
"""

import json
import struct
from pathlib import Path
import argparse

def extract_workflow_from_png(png_path):
    """Extract workflow from PNG metadata"""
    # Implementation as shown above
    pass

def add_clipskip(workflow):
    """Add CLIPSetLastLayer to workflow"""
    # Implementation as shown above
    pass

def main():
    parser = argparse.ArgumentParser(description='Extract and modify ComfyUI workflows')
    parser.add_argument('input', help='Input PNG file')
    parser.add_argument('--add-clipskip', action='store_true', 
                       help='Add CLIPSetLastLayer node')
    parser.add_argument('--output', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Extract workflow
    workflow = extract_workflow_from_png(args.input)
    if not workflow:
        print(f"No workflow found in {args.input}")
        return
    
    print(f"Extracted workflow with {len(workflow['nodes'])} nodes")
    
    # Modify if requested
    if args.add_clipskip:
        workflow = add_clipskip(workflow)
        print("Added CLIPSetLastLayer node")
    
    # Save
    output_path = args.output or "extracted_workflow.json"
    with open(output_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
```

## Common Use Cases

### 1. Workflow Recovery
Extract workflow from a generated image when the original JSON is lost:
```bash
python extract_workflow.py generated_image.png --output recovered_workflow.json
```

### 2. Workflow Analysis
Analyze workflows from a collection of images:
```bash
python extract_workflow.py *.png --analyze
```

### 3. Batch Modification
Add features to multiple workflows:
```bash
python extract_workflow.py images/*.png --add-clipskip --output-dir modified/
```

### 4. Version Control
Extract workflows for git tracking:
```bash
python extract_workflow.py output.png --output workflows/$(date +%Y%m%d)_workflow.json
git add workflows/
git commit -m "Add workflow from generated image"
```

## Troubleshooting

### No Workflow Found
- Ensure the PNG was saved from ComfyUI with workflow metadata enabled
- Check ComfyUI settings: "Embed workflow in generated images" should be ON
- Some image processors may strip metadata

### Encoding Issues
- Use `errors='ignore'` when decoding chunk types
- Handle both latin-1 and utf-8 encodings for text data
- Some workflows may use different text encoding

### Large Workflows
- For workflows > 100 nodes, consider chunked reading
- Implement memory-efficient parsing for batch processing

## Notes

- ComfyUI embeds the FULL Frontend/UI format workflow
- All visual layout information is preserved
- Widget values and node properties are included
- Group information and colors are maintained
- This allows perfect reconstruction of the workflow

---

*Last Updated: 2025-01-31*
*Tested with ComfyUI versions: 0.3.x*