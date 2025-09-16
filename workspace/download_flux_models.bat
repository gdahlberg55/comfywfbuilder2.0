@echo off
echo ========================================
echo Flux Model Downloader for ComfyUI
echo ========================================
echo.
echo This script will download Flux models using wget or curl
echo Make sure you have wget or curl installed
echo.

set MODELS_DIR=C:\Users\gdahl\Documents\ComfyUI\models

echo Creating directories...
mkdir "%MODELS_DIR%\unet" 2>nul
mkdir "%MODELS_DIR%\clip" 2>nul
mkdir "%MODELS_DIR%\vae" 2>nul
mkdir "%MODELS_DIR%\loras" 2>nul

echo.
echo ========================================
echo DOWNLOADING FLUX MODELS
echo ========================================
echo.

REM Check for wget or curl
where wget >nul 2>nul
if %errorlevel%==0 (
    set DOWNLOAD_CMD=wget -c -O
) else (
    where curl >nul 2>nul
    if %errorlevel%==0 (
        set DOWNLOAD_CMD=curl -L -o
    ) else (
        echo ERROR: Neither wget nor curl found!
        echo Please install wget or curl first.
        pause
        exit /b 1
    )
)

echo Using download command: %DOWNLOAD_CMD%
echo.

REM ========================================
REM ESSENTIAL MODELS (Required)
REM ========================================

echo [1/6] Downloading Flux UNET Model (11.9GB)...
echo This is the main Flux model - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\unet\flux1-dev-fp8.safetensors" ^
    "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors"

echo.
echo [2/6] Downloading T5-XXL Text Encoder FP8 (4.7GB)...
echo Lower VRAM version - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\clip\t5xxl_fp8_e4m3fn.safetensors" ^
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors"

echo.
echo [3/6] Downloading CLIP-L Text Encoder (246MB)...
echo Secondary text encoder - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\clip\clip_l.safetensors" ^
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"

echo.
echo [4/6] Downloading Flux VAE (335MB)...
echo Image encoder/decoder - REQUIRED
%DOWNLOAD_CMD% "%MODELS_DIR%\vae\ae.safetensors" ^
    "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors"

echo.
echo ========================================
echo OPTIONAL MODELS
echo ========================================
echo.

echo [5/6] Downloading Realism LoRA (optional)...
echo Skip with Ctrl+C if not needed
%DOWNLOAD_CMD% "%MODELS_DIR%\loras\flux-RealismLora.safetensors" ^
    "https://civitai.com/api/download/models/680306"

echo.
echo [6/6] Downloading Detail Enhancer LoRA (optional)...
echo Skip with Ctrl+C if not needed
%DOWNLOAD_CMD% "%MODELS_DIR%\loras\flux-DetailEnhancer.safetensors" ^
    "https://civitai.com/api/download/models/721451"

echo.
echo ========================================
echo DOWNLOAD COMPLETE!
echo ========================================
echo.
echo Models installed in: %MODELS_DIR%
echo.
echo Required models for basic Flux workflow:
echo - unetlux1-dev-fp8.safetensors
echo - clip	5xxl_fp8_e4m3fn.safetensors
echo - clip\clip_l.safetensors
echo - vaee.safetensors
echo.
pause
