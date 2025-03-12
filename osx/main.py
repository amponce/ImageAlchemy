from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
import uuid
import os

app = FastAPI()

# Check for MPS (Metal Performance Shaders) availability on Mac
if torch.backends.mps.is_available():
    device = "mps"
    print("Using MPS (Metal Performance Shaders) for acceleration on Apple Silicon")
    dtype = torch.float16
else:
    device = "cpu"
    print("MPS not available, using CPU (this will be slow)")
    dtype = torch.float32

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
).to(device)

@app.post("/generate/")
async def generate_images(
    prompt: str = Form(...),
    strength: float = Form(0.6),
    guidance_scale: float = Form(7.5),
    steps: int = Form(30),  # Default to 30 for better Mac performance
    batch_size: int = Form(1),  # Default to 1 for Mac
    file: UploadFile = File(...)
):
    # Force batch_size to 1 for MPS
    if device == "mps" and batch_size > 1:
        print(f"Reducing batch size from {batch_size} to 1 for optimal MPS performance")
        batch_size = 1

    output_dir = f"output_{uuid.uuid4()}"
    os.makedirs(output_dir, exist_ok=True)

    # Use a moderate size that works well on Macs
    init_image = Image.open(file.file).convert("RGB").resize((768, 768), Image.LANCZOS)
    
    # Cap steps for Mac performance
    if device == "mps" and steps > 30:
        print(f"Reducing steps from {steps} to 30 for optimal MPS performance")
        steps = 30
    
    images = pipe(
        prompt=[prompt] * batch_size,
        image=[init_image] * batch_size,
        strength=strength,
        guidance_scale=guidance_scale,
        num_inference_steps=steps,
        output_type="pil"
    ).images
    
    image_paths = []
    for idx, img in enumerate(images):
        path = f"{output_dir}/image_{idx}.png"
        img.save(path)
        image_paths.append(path)

    # Return the first image
    return FileResponse(image_paths[0]) 