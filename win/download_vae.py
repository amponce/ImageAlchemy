from diffusers import AutoencoderKL
import torch

print("Downloading VAE model...")
vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix",
    torch_dtype=torch.float16
)
vae.save_pretrained("../models/sdxl-vae-fp16-fix")
print("VAE model downloaded and saved to ../models/sdxl-vae-fp16-fix") 