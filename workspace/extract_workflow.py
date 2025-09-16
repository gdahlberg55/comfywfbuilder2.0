import json
import struct
import sys

def extract_workflow_from_png(png_path):
    """Extract ComfyUI workflow from PNG metadata"""
    try:
        with open(png_path, 'rb') as f:
            # Check PNG signature
            signature = f.read(8)
            if signature != b'\x89PNG\r\n\x1a\n':
                print(f"Not a valid PNG file: {png_path}")
                return None
            
            # Read chunks
            while True:
                # Read chunk length
                length_bytes = f.read(4)
                if not length_bytes:
                    break
                    
                length = struct.unpack('>I', length_bytes)[0]
                
                # Read chunk type
                chunk_type = f.read(4)
                if not chunk_type:
                    break
                
                # Read chunk data
                chunk_data = f.read(length)
                
                # Skip CRC
                f.read(4)
                
                # Check for tEXt chunk with workflow
                if chunk_type == b'tEXt':
                    # Split keyword and text
                    null_index = chunk_data.find(b'\x00')
                    if null_index != -1:
                        keyword = chunk_data[:null_index].decode('latin-1')
                        text = chunk_data[null_index+1:].decode('latin-1')
                        
                        if keyword == 'workflow':
                            print(f"Found workflow in {png_path}")
                            return json.loads(text)
                        elif keyword == 'prompt':
                            print(f"Found prompt data (API format) in {png_path}")
    
    except Exception as e:
        print(f"Error reading {png_path}: {e}")
    
    return None

# Check multiple files
import os
import glob

files_to_check = [
    r'C:\Users\gdahl\Downloads\workflow.png',
    r'C:\Users\gdahl\Downloads\Screenshot 2025-09-01 131124.png',
    r'C:\Users\gdahl\Downloads\PonyXL_output_11106_.png',
    r'C:\Users\gdahl\Downloads\ComfyUI_temp_opsdu_00189_.png'
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"\nChecking: {os.path.basename(file_path)}")
        workflow = extract_workflow_from_png(file_path)
        if workflow:
            output_name = os.path.basename(file_path).replace('.png', '_workflow.json')
            output_path = os.path.join(r'C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace', output_name)
            with open(output_path, 'w') as f:
                json.dump(workflow, f, indent=2)
            print(f"  Workflow saved to: {output_path}")
            print(f"  Has {len(workflow.get('nodes', []))} nodes")
