#!/bin/bash

# Set up the models directory
mkdir -p models

# Check if the VAE exists and download if needed
if [ ! -d "models/sdxl-vae-fp16-fix" ]; then
    echo "Optimized VAE not found. Downloading..."
    python -c "
from diffusers import AutoencoderKL
import torch

# Download optimized VAE
print('Downloading optimized VAE for better image quality...')
vae = AutoencoderKL.from_pretrained(
    'madebyollin/sdxl-vae-fp16-fix',
    torch_dtype=torch.float32
)

# Save the VAE
vae.save_pretrained('models/sdxl-vae-fp16-fix')
print('Optimized VAE downloaded and saved to models/sdxl-vae-fp16-fix')
"
    echo "Optimized VAE downloaded successfully."
else
    echo "Optimized VAE already exists in models directory."
fi

# Install the compel library for better prompt understanding
pip install compel>=2.0.2

# Check if custom model exists
if [ -f "models/realcartoon3d_v18.safetensors" ]; then
    echo "Custom SDXL model (EpicJuggernautXL_vxvXI) found!"
else
    echo "WARNING: Custom SDXL model not found at models/realcartoon3d_v18.safetensors"
    echo "Please make sure your model file is in the correct location."
fi

echo "Setup complete! Your custom SDXL model is now optimized with:"
echo "- SDXL pipeline architecture"
echo "- Improved VAE for better image quality"
echo "- Compel for enhanced prompt understanding"