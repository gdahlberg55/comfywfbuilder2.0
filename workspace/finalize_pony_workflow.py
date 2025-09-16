import json
import os

# Read the original workflow
workflow_path = r"C:\Users\gdahl\Documents\End-to-end_Workflows\2-Pass_SDXL Pony Image Gen_ConrolNet_Face Fix_Hand fix.json"
with open(workflow_path, 'r') as f:
    workflow = json.load(f)

print("FINALIZING PONY WORKFLOW WITH DOWNLOADED MODELS")
print("=" * 80)

# Update model paths to use the actual downloaded models
for node in workflow["nodes"]:
    node_type = node.get("type", "")
    
    if node_type == "CheckpointLoaderSimple":
        # Use the Pony checkpoint that exists
        old_value = node["widgets_values"][0]
        node["widgets_values"][0] = "checkpoints/pony/Pony_CyberRealistic_v12.5.safetensors"
        print(f"Checkpoint: Updated to Pony_CyberRealistic_v12.5.safetensors")
    
    elif node_type == "LoraLoader":
        # Keep LoRAs bypassed since they don't exist
        old_value = node["widgets_values"][0]
        node["widgets_values"][1] = 0.0  # Set strength to 0
        node["mode"] = 2  # Bypass
        print(f"LoRA: {old_value} (bypassed - not available)")
    
    elif node_type == "SAMLoader":
        # SAM model exists
        old_value = node["widgets_values"][0]
        node["widgets_values"][0] = "sams/sam_vit_b_01ec64.pth"
        print(f"SAM: Using sam_vit_b_01ec64.pth")
    
    elif node_type == "ControlNetLoader":
        # Use the downloaded OpenPose ControlNet
        old_value = node["widgets_values"][0]
        node["widgets_values"][0] = "controlnet/t2i-adapter-openpose-sdxl-1.0.safetensors"
        node["mode"] = 0  # Enable (not bypassed)
        print(f"ControlNet: Using t2i-adapter-openpose-sdxl-1.0.safetensors")
    
    elif node_type == "ControlNetApplyAdvanced":
        # Re-enable ControlNet Apply nodes
        node["mode"] = 0  # Enable
        print(f"ControlNetApply: Enabled")
    
    elif node_type == "UltralyticsDetectorProvider":
        # Set to use the downloaded pose model
        if "widgets_values" in node and len(node["widgets_values"]) > 0:
            node["widgets_values"][0] = "ultralytics/bbox/yolov8s-pose.pt"
            print(f"Ultralytics: Using yolov8s-pose.pt for pose detection")

# Save the finalized workflow
output_path = r"C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\pony_workflow_ready.json"
with open(output_path, 'w') as f:
    json.dump(workflow, f, indent=2)

print("\n" + "=" * 80)
print("WORKFLOW READY!")
print("=" * 80)

print("\nMODELS CONFIGURED:")
print("-" * 40)
print("1. Checkpoint: pony/Pony_CyberRealistic_v12.5.safetensors")
print("2. SAM Model: sams/sam_vit_b_01ec64.pth")
print("3. ControlNet: controlnet/t2i-adapter-openpose-sdxl-1.0.safetensors")
print("4. Pose Detection: ultralytics/bbox/yolov8s-pose.pt")
print("5. LoRAs: Bypassed (not available)")

print("\nADDITIONAL MODELS AVAILABLE:")
print("-" * 40)
print("- control-lora-openposeXL2-rank256.safetensors")
print("- controlnetxlCNXL_openpose.safetensors")
print("- yolov8n-pose.pt (lighter alternative)")
print("- DWPose models (dw-ll_ucoco_384.onnx, yolox_l.onnx)")

print(f"\nWorkflow saved to: {output_path}")
print("\nThe workflow is now ready to use in ComfyUI!")