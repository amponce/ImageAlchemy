@echo off
echo Setting up custom SDXL model for ImageAlchemy with GPU optimization...

:: Create parent models directory if it doesn't exist
if not exist ..\models mkdir ..\models

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install compel for optimized prompt understanding
echo Installing compel for optimized prompt understanding...
pip install compel --upgrade

:: Install xformers for memory efficiency if using CUDA (critical for GPU performance)
echo Installing xformers for memory efficiency (critical for GPU performance)...
pip install xformers --upgrade

:: Install additional GPU optimizers
echo Installing additional GPU optimizations...
pip install accelerate --upgrade
pip install bitsandbytes --upgrade
pip install ninja --upgrade

:: Download the custom model if it doesn't exist
if not exist ..\models\epicjuggernautxl_vxvXI.safetensors (
    echo Downloading EpicJuggernautXL model...
    echo This will download the model from Hugging Face...
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='stablediffusionapi/epicjuggernautxl', filename='epicjuggernautxl_vxvXI.safetensors', local_dir='../models')"
)

:: Check if model download was successful
if not exist ..\models\epicjuggernautxl_vxvXI.safetensors (
    echo Could not download model automatically.
    echo Please download manually from: https://civitai.com/models/133005
    echo And place it in the models directory as: epicjuggernautxl_vxvXI.safetensors
) else (
    echo Custom model successfully installed!
)

:: Try to download VAE if it doesn't exist (essential for quality images)
if not exist ..\models\sdxl-vae-fp16-fix (
    echo Downloading optimized VAE...
    python -c "import os; from huggingface_hub import snapshot_download; snapshot_download(repo_id='madebyollin/sdxl-vae-fp16-fix', local_dir='../models/sdxl-vae-fp16-fix')"
)

:: Try to download LoRA weights for enhanced quality
if not exist ..\models\sd_xl_offset_example-lora_1.0.safetensors (
    echo Downloading LoRA weights for enhanced quality...
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='stabilityai/stable-diffusion-xl-base-1.0', filename='sd_xl_offset_example-lora_1.0.safetensors', local_dir='../models')"
)

echo Setup complete! Your system is now optimized for maximum GPU performance.
echo.
echo Run the application with run_windows.bat
echo.
echo Press any key to exit...
pause > nul