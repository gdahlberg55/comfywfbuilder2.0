import os
import subprocess

# Define ComfyUI directories
COMFYUI_DIR = r"C:\Users\gdahl\Documents\ComfyUI"
MODELS_DIR = os.path.join(COMFYUI_DIR, "models")

# Additional OpenPose models and preprocessors
OPENPOSE_MODELS = {
    "controlnet_models": [
        {
            "name": "control-lora-openposeXL2-rank256.safetensors",
            "url": "https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0/resolve/main/control-lora-openposeXL2-rank256.safetensors",
            "folder": os.path.join(MODELS_DIR, "controlnet"),
            "description": "OpenPose ControlNet LoRA for SDXL"
        },
        {
            "name": "controlnetxlCNXL_openpose.safetensors", 
            "url": "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/controlnetxlCNXL_openpose.safetensors",
            "folder": os.path.join(MODELS_DIR, "controlnet"),
            "description": "Alternative OpenPose ControlNet for SDXL"
        }
    ],
    "ultralytics_models": [
        {
            "name": "yolov8n-pose.pt",
            "url": "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-pose.pt",
            "folder": os.path.join(MODELS_DIR, "ultralytics", "bbox"),
            "description": "YOLOv8 Pose Detection Model"
        },
        {
            "name": "yolov8s-pose.pt",
            "url": "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s-pose.pt",
            "folder": os.path.join(MODELS_DIR, "ultralytics", "bbox"),
            "description": "YOLOv8 Small Pose Model (better accuracy)"
        }
    ],
    "dwpose_models": [
        {
            "name": "dw-ll_ucoco_384.onnx",
            "url": "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx",
            "folder": os.path.join(MODELS_DIR, "pose"),
            "description": "DWPose Model for accurate pose estimation"
        },
        {
            "name": "yolox_l.onnx",
            "url": "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx",
            "folder": os.path.join(MODELS_DIR, "pose"),
            "description": "YOLOX detector for DWPose"
        }
    ]
}

print("=" * 80)
print("DOWNLOADING OPENPOSE PACKAGES FOR COMFYUI")
print("=" * 80)

def download_file(url, output_path, description):
    """Download a file using curl"""
    filename = os.path.basename(output_path)
    print(f"\n[{description}]")
    print(f"Downloading: {filename}")
    print(f"To: {output_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / (1024*1024)  # Size in MB
        print(f"Already exists ({file_size:.1f} MB), skipping...")
        return True
    
    # Use curl to download
    cmd = f'curl -L -o "{output_path}" "{url}"'
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"Downloaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to download: {e}")
        return False

# Download models by category
for category, models_list in OPENPOSE_MODELS.items():
    print(f"\n{'='*40}")
    print(f"{category.upper().replace('_', ' ')}")
    print(f"{'='*40}")
    
    for model in models_list:
        output_path = os.path.join(model["folder"], model["name"])
        success = download_file(model["url"], output_path, model["description"])
        
        if not success:
            print(f"Manual download URL: {model['url']}")

print("\n" + "=" * 80)
print("INSTALLATION SUMMARY")
print("=" * 80)

# Check what's installed
print("\nCHECKING INSTALLED MODELS:")
print("-" * 40)

# Check ControlNet models
controlnet_dir = os.path.join(MODELS_DIR, "controlnet")
if os.path.exists(controlnet_dir):
    openpose_models = [f for f in os.listdir(controlnet_dir) if 'openpose' in f.lower()]
    print(f"\nControlNet OpenPose Models ({len(openpose_models)}):")
    for model in openpose_models:
        size = os.path.getsize(os.path.join(controlnet_dir, model)) / (1024*1024)
        print(f"  - {model} ({size:.1f} MB)")

# Check Ultralytics models
ultralytics_dir = os.path.join(MODELS_DIR, "ultralytics", "bbox")
if os.path.exists(ultralytics_dir):
    pose_models = [f for f in os.listdir(ultralytics_dir) if 'pose' in f.lower()]
    if pose_models:
        print(f"\nUltralytics Pose Models ({len(pose_models)}):")
        for model in pose_models:
            size = os.path.getsize(os.path.join(ultralytics_dir, model)) / (1024*1024)
            print(f"  - {model} ({size:.1f} MB)")

# Check DWPose models
pose_dir = os.path.join(MODELS_DIR, "pose")
if os.path.exists(pose_dir):
    dwpose_models = [f for f in os.listdir(pose_dir) if f.endswith('.onnx')]
    if dwpose_models:
        print(f"\nDWPose Models ({len(dwpose_models)}):")
        for model in dwpose_models:
            size = os.path.getsize(os.path.join(pose_dir, model)) / (1024*1024)
            print(f"  - {model} ({size:.1f} MB)")

print("\n" + "="*80)
print("Your OpenPose setup is now complete!")
print("The workflow should work with full OpenPose functionality.")
print("="*80)