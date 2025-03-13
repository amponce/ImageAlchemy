#!/bin/bash

# Set up the models directory
mkdir -p models

# Check if SDXL model exists
if [ ! -d "models/sdxl-base-1.0" ] && [ ! -f "models/sdxl-base-1.0.safetensors" ]; then
    echo "SDXL model not found. Downloading..."
    # Use Python to download the model
    python -c "
from diffusers import StableDiffusionXLImg2ImgPipeline
import torch

# Determine the device
device = 'mps' if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available() else 'cpu'
dtype = torch.float32

# Download SDXL base model
print('Downloading SDXL model...')
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    'stabilityai/stable-diffusion-xl-base-1.0',
    torch_dtype=dtype,
    use_safetensors=True,
    variant='fp16' if torch.cuda.is_available() else None,
).to(device)

# Save the model
pipe.save_pretrained('models/sdxl-base-1.0')
print('SDXL model downloaded and saved to models/sdxl-base-1.0')
"
    echo "SDXL model downloaded successfully."
else
    echo "SDXL model already exists in models directory."
fi

# Try to download the optimized VAE
if [ ! -d "models/sdxl-vae-fp16-fix" ]; then
    echo "Optimized VAE not found. Downloading..."
    python -c "
from diffusers import AutoencoderKL
import torch

# Download optimized VAE
print('Downloading optimized VAE...')
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

echo "Model setup complete!"