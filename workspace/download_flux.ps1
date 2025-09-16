# Flux Model Downloader PowerShell Script
# Run with: powershell -ExecutionPolicy Bypass -File download_flux.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FLUX MODEL DOWNLOADER FOR COMFYUI" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$modelsDir = "C:\Users\gdahl\Documents\ComfyUI\models"

# Create directories
$dirs = @("$modelsDir\unet", "$modelsDir\clip", "$modelsDir\vae")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "[OK] Created directory: $dir" -ForegroundColor Green
    }
}

# Define downloads
$downloads = @(
    @{
        Name = "FLUX UNET Model (11.9 GB)"
        Url = "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors"
        Path = "$modelsDir\unet\flux1-dev-fp8.safetensors"
    },
    @{
        Name = "CLIP-L Text Encoder (246 MB)"
        Url = "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"
        Path = "$modelsDir\clip\clip_l.safetensors"
    },
    @{
        Name = "Flux VAE (335 MB)"
        Url = "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"
        Path = "$modelsDir\vae\ae.safetensors"
    }
)

Write-Host ""
Write-Host "Models to download:" -ForegroundColor Yellow
foreach ($item in $downloads) {
    Write-Host "  - $($item.Name)" -ForegroundColor White
}

Write-Host ""
$response = Read-Host "Start download? (y/n)"
if ($response -ne 'y') {
    Write-Host "Download cancelled" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DOWNLOADING MODELS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$count = 0
foreach ($item in $downloads) {
    $count++
    Write-Host ""
    Write-Host "[$count/3] Downloading: $($item.Name)" -ForegroundColor Yellow
    
    if (Test-Path $item.Path) {
        Write-Host "[SKIP] File already exists" -ForegroundColor Green
        continue
    }
    
    try {
        Write-Host "Downloading to: $($item.Path)" -ForegroundColor Gray
        Write-Host "This may take a while..." -ForegroundColor Gray
        
        # Use Invoke-WebRequest with progress
        $ProgressPreference = 'Continue'
        Invoke-WebRequest -Uri $item.Url -OutFile $item.Path -UseBasicParsing
        
        Write-Host "[OK] Downloaded successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "[ERROR] Failed to download: $_" -ForegroundColor Red
        Write-Host "Try downloading manually from:" -ForegroundColor Yellow
        Write-Host $item.Url -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DOWNLOAD COMPLETE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use the Flux workflow in ComfyUI!" -ForegroundColor Green
Write-Host "Load: flux_inpaint_workflow_with_clipskip.json" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")