import struct
import json
import os

def find_json_in_binary(file_path, max_size=10*1024*1024):
    """Search for JSON workflow data in binary file"""
    with open(file_path, 'rb') as f:
        data = f.read(max_size)
    
    # Look for JSON markers
    markers = [
        b'workflow',
        b'ComfyUI', 
        b'"nodes"',
        b'"links"',
        b'"last_node_id"',
        b'"last_link_id"',
        b'"groups"',
        b'"config"',
        b'"extra"'
    ]
    
    found_markers = []
    for marker in markers:
        pos = 0
        while True:
            pos = data.find(marker, pos)
            if pos == -1:
                break
            found_markers.append((marker.decode('utf-8', errors='ignore'), pos))
            print(f'Found "{marker.decode("utf-8", errors="ignore")}" at byte position {pos}')
            pos += 1
    
    # Try to extract JSON starting from each marker position
    for marker, pos in found_markers:
        # Search backwards for '{'
        start = pos
        while start > 0 and data[start:start+1] != b'{':
            start -= 1
        
        if start > 0:
            # Try to extract JSON
            bracket_count = 0
            end = start
            max_search = min(start + 1000000, len(data))  # Search up to 1MB forward
            
            while end < max_search:
                char = data[end:end+1]
                
                if char == b'{':
                    bracket_count += 1
                elif char == b'}':
                    bracket_count -= 1
                    if bracket_count == 0:
                        # Found matching closing bracket
                        json_data = data[start:end+1]
                        try:
                            obj = json.loads(json_data)
                            # Check if this looks like a ComfyUI workflow
                            if isinstance(obj, dict) and ('nodes' in obj or 'workflow' in obj):
                                return obj
                        except:
                            pass
                        break
                
                end += 1
    
    return None

# Check both video files
video_files = [
    r'C:\Users\gdahl\Downloads\Video-720p-rife_00014 (1).rife',
    r'C:\Users\gdahl\Downloads\Video-720p-rife_00014.mp4'
]

for video_path in video_files:
    if os.path.exists(video_path):
        print(f'\nAnalyzing: {video_path}')
        print(f'File size: {os.path.getsize(video_path):,} bytes')
        print('-' * 50)
        
        workflow = find_json_in_binary(video_path)
        if workflow:
            filename = os.path.basename(video_path).replace('.rife', '').replace('.mp4', '')
            output_path = rf'C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\{filename}_workflow.json'
            with open(output_path, 'w') as f:
                json.dump(workflow, f, indent=2)
            print(f'\nWorkflow successfully extracted!')
            print(f'Saved to: {output_path}')
            if 'nodes' in workflow:
                print(f'Workflow has {len(workflow.get("nodes", []))} nodes')
            else:
                print(f'Found workflow data with keys: {list(workflow.keys())}')
        else:
            print('\nNo ComfyUI workflow found embedded in this video file')
    else:
        print(f'\nFile not found: {video_path}')

print('\n' + '='*60)
print('Note: ComfyUI typically embeds workflows in PNG image outputs,')
print('not in video files. Video files are usually the final rendered output.')
print('To find the original workflow, look for PNG files with similar names.')