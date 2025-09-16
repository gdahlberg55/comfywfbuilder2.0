import os
import subprocess
import json

# Define ComfyUI models directory
COMFYUI_DIR = r"C:\Users\gdahl\Documents\ComfyUI\models"

# Models needed for the workflow
REQUIRED_MODELS = {
    "controlnet": {
        "t2i-adapter-openpose-sdxl-1.0.safetensors": {
            "url": "https://huggingface.co/TencentARC/t2i-adapter-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors",
            "folder": os.path.join(COMFYUI_DIR, "controlnet"),
            "filename": "t2i-adapter-openpose-sdxl-1.0.safetensors"
        }
    }
}

print("=" * 80)
print("DOWNLOADING MISSING MODELS FOR PONY WORKFLOW")
print("=" * 80)

def download_file(url, output_path):
    """Download a file using curl (available on Windows)"""
    print(f"\nDownloading: {os.path.basename(output_path)}")
    print(f"From: {url}")
    print(f"To: {output_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Use curl to download (available on Windows 10+)
    cmd = f'curl -L -o "{output_path}" "{url}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ Downloaded successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to download {os.path.basename(output_path)}")
        return False

# Download each required model
for category, models in REQUIRED_MODELS.items():
    print(f"\n{category.upper()} MODELS:")
    print("-" * 40)
    
    for model_name, model_info in models.items():
        output_path = os.path.join(model_info["folder"], model_info["filename"])
        
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"✓ {model_name} already exists, skipping...")
            continue
        
        # Download the model
        success = download_file(model_info["url"], output_path)
        
        if not success:
            print(f"\n⚠ Alternative: You can manually download from:")
            print(f"  {model_info['url']}")
            print(f"  And save to: {output_path}")

print("\n" + "=" * 80)
print("DOWNLOAD SUMMARY")
print("=" * 80)

# Check what's now available
print("\n✓ MODELS NOW AVAILABLE:")
print(f"1. Checkpoint: pony/Pony_CyberRealistic_v12.5.safetensors (already had)")
print(f"2. SAM: sams/sam_vit_b_01ec64.pth (already had)")

# Check if ControlNet was downloaded
controlnet_path = os.path.join(COMFYUI_DIR, "controlnet", "t2i-adapter-openpose-sdxl-1.0.safetensors")
if os.path.exists(controlnet_path):
    print(f"3. ControlNet: controlnet/t2i-adapter-openpose-sdxl-1.0.safetensors ✓")
else:
    print(f"3. ControlNet: NEEDS MANUAL DOWNLOAD")

print("\n📝 NOTE: LoRAs were skipped as requested")
print("\nYour workflow should now work with the available models!")