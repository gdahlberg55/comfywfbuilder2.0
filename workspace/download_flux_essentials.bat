@echo off
echo ============================================================
echo FLUX ESSENTIAL MODELS DOWNLOADER
echo ============================================================
echo.
echo This will download the minimum required Flux models
echo Total download size: ~17GB
echo.
echo Models will be saved to:
echo C:\Users\gdahl\Documents\ComfyUI\models\
echo.
pause

set MODELS_DIR=C:\Users\gdahl\Documents\ComfyUI\models

echo.
echo Creating directories...
mkdir "%MODELS_DIR%\unet" 2>nul
mkdir "%MODELS_DIR%\clip" 2>nul
mkdir "%MODELS_DIR%\vae" 2>nul

echo.
echo ============================================================
echo DOWNLOAD COMMANDS
echo ============================================================
echo.
echo Please download these files manually or use wget/curl:
echo.

echo 1. FLUX UNET MODEL (11.9GB) - REQUIRED
echo    Download: https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors
echo    Save to: %MODELS_DIR%\unet\flux1-dev-fp8.safetensors
echo.

echo 2. CLIP-L MODEL (246MB) - REQUIRED  
echo    Download: https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors
echo    Save to: %MODELS_DIR%\clip\clip_l.safetensors
echo.

echo 3. FLUX VAE (335MB) - REQUIRED
echo    Download: https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors
echo    Save to: %MODELS_DIR%\vae\ae.safetensors
echo.

echo NOTE: You already have t5xxl_fp8_e4m3fn.safetensors installed!
echo.

echo ============================================================
echo WGET COMMANDS (if you have wget installed):
echo ============================================================
echo.
echo wget -P "%MODELS_DIR%\unet" "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors"
echo wget -P "%MODELS_DIR%\clip" "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"
echo wget -P "%MODELS_DIR%\vae" "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"
echo.

pause