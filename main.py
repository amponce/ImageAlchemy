from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
import uuid
import os

app = FastAPI()

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
).to("cuda")

@app.post("/generate/")
async def generate_images(
    prompt: str = Form(...),
    strength: float = Form(0.6),
    guidance_scale: float = Form(7.5),
    steps: int = Form(50),
    batch_size: int = Form(1),  # Reduced batch size to save memory
    file: UploadFile = File(...)
):
    output_dir = f"output_{uuid.uuid4()}"
    os.makedirs(output_dir, exist_ok=True)

    # Use a more moderate size that requires less VRAM
    init_image = Image.open(file.file).convert("RGB").resize((768, 768))
    
    images = pipe(
        prompt=[prompt] * batch_size,
        image=[init_image] * batch_size,
        strength=strength,
        guidance_scale=guidance_scale,
        num_inference_steps=steps,
        # Removed denoising_end parameter which is specific to refiner
        output_type="pil"
    ).images
    
    image_paths = []
    for idx, img in enumerate(images):
        path = f"{output_dir}/image_{idx}.png"
        img.save(path)
        image_paths.append(path)

    # For simplicity, return the first image
    return FileResponse(image_paths[0])

