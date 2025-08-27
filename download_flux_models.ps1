# FLUX Model Auto-Downloader for ComfyUI
# This script downloads all required FLUX models to their correct locations

Write-Host "FLUX Model Downloader for ComfyUI" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Set ComfyUI base path - CHANGE THIS TO YOUR COMFYUI LOCATION
$COMFYUI_PATH = "C:\ComfyUI"  # Change this to your actual ComfyUI path

# Create directories
Write-Host "`nCreating model directories..." -ForegroundColor Yellow
$directories = @(
    "$COMFYUI_PATH\models\unet",
    "$COMFYUI_PATH\models\clip", 
    "$COMFYUI_PATH\models\vae",
    "$COMFYUI_PATH\models\upscale_models"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "Exists: $dir" -ForegroundColor Gray
    }
}

# Download function with progress
function Download-Model {
    param(
        [string]$url,
        [string]$output,
        [string]$name
    )
    
    Write-Host "`nDownloading $name..." -ForegroundColor Cyan
    Write-Host "From: $url" -ForegroundColor Gray
    Write-Host "To: $output" -ForegroundColor Gray
    
    if (Test-Path $output) {
        Write-Host "$name already exists, skipping..." -ForegroundColor Yellow
        return
    }
    
    try {
        # Use curl for better progress display (available in Windows 10+)
        curl.exe -L -o $output --progress-bar $url
        Write-Host "$name downloaded successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "Error downloading $name : $_" -ForegroundColor Red
    }
}

# Model URLs and destinations
$models = @{
    "FLUX Dev Model (23.8GB)" = @{
        url = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors"
        output = "$COMFYUI_PATH\models\unet\flux1-dev.safetensors"
    }
    "T5-XXL Text Encoder (4.9GB)" = @{
        url = "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors"
        output = "$COMFYUI_PATH\models\clip\t5xxl_fp8_e4m3fn.safetensors"
    }
    "CLIP-L Text Encoder (246MB)" = @{
        url = "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"
        output = "$COMFYUI_PATH\models\clip\clip_l.safetensors"
    }
    "VAE Model (335MB)" = @{
        url = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"
        output = "$COMFYUI_PATH\models\vae\ae.safetensors"
    }
    "4x-UltraSharp Upscaler (67MB)" = @{
        url = "https://huggingface.co/Kim2091/UltraSharp/resolve/main/4x-UltraSharp.pth"
        output = "$COMFYUI_PATH\models\upscale_models\4x-UltraSharp.pth"
    }
}

# Show download menu
Write-Host "`nModels to download:" -ForegroundColor Yellow
$i = 1
foreach ($modelName in $models.Keys) {
    Write-Host "$i. $modelName" -ForegroundColor White
    $i++
}
Write-Host "$i. Download ALL models" -ForegroundColor Green

# Ask user what to download
$choice = Read-Host "`nEnter your choice (1-$i)"

if ($choice -eq $i.ToString()) {
    # Download all models
    Write-Host "`nDownloading all models (Total: ~29.3GB)..." -ForegroundColor Green
    foreach ($modelName in $models.Keys) {
        $model = $models[$modelName]
        Download-Model -url $model.url -output $model.output -name $modelName
    }
} else {
    # Download specific model
    $selectedModel = ($models.Keys | Select-Object -Index ($choice - 1))
    if ($selectedModel) {
        $model = $models[$selectedModel]
        Download-Model -url $model.url -output $model.output -name $selectedModel
    } else {
        Write-Host "Invalid choice!" -ForegroundColor Red
    }
}

Write-Host "`n=================================" -ForegroundColor Cyan
Write-Host "Download process complete!" -ForegroundColor Green
Write-Host "Your FLUX workflow is ready to use in ComfyUI" -ForegroundColor Green
Write-Host "`nWorkflow location:" -ForegroundColor Yellow
Write-Host "flux_complete_workflow.json" -ForegroundColor White

Read-Host "`nPress Enter to exit"