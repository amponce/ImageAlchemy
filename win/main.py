import os
import torch

# Force CUDA-only operation
assert torch.cuda.is_available(), "CUDA GPU is required!"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'

# Set CUDA optimizations
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
torch.backends.cudnn.benchmark = True

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from diffusers import StableDiffusionXLImg2ImgPipeline, AutoencoderKL
from PIL import Image
import uuid
import json

app = FastAPI()

# Print GPU information
print(f"CUDA Device Count: {torch.cuda.device_count()}")
print(f"Using GPU: {torch.cuda.get_device_name(0)}")
print(f"Available GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
config_path = os.path.join(parent_dir, "config.json")
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    print(f"Loaded configuration from {config_path}")
except Exception as e:
    print(f"Error loading configuration: {e}")
    config = {}

# Extract face settings from config or use defaults
face_settings = config.get("face_settings", {})
FACE_PRESERVATION = face_settings.get("face_preservation", "preserve exact face structure, same facial features, same eye color, same nose, photorealistic face")
HAIR_PRESERVATION = face_settings.get("hair_preservation", "elegant flowing hair, beautiful wavy hair, silky smooth hair, well-styled hair, natural hair texture, glamorous hairstyle, luxurious hair volume, feminine hairstyle, elegant pixie cut")
EXPRESSION_MODIFIER = face_settings.get("expression_modifier", "pensive expression, slightly bigger anime-like eyes, dreamy gaze, thoughtful look, slightly larger eyes with love expression, anime influenced eye style, Roblox character style, 3D Roblox face")
BODY_PRESERVATION = face_settings.get("body_preservation", "preserve exact pose, same body position")
BASE_QUALITY = face_settings.get("base_quality", "high quality, detailed, professional photography")

# Extract negative prompts from config or use defaults
negative_prompts = config.get("negative_prompts", {})
FACE_NEGATIVE = negative_prompts.get("face_negative", "distorted face, deformed face, bad face, multiple faces, unrealistic face, face artifacts")
HAIR_NEGATIVE = negative_prompts.get("hair_negative", "buzz cut, messy hair, unkempt hair, hat, cap, headpiece, crown, tiara, hair accessories, bandana, headband, anything on head, bad hairstyle, tangled hair, frizzy hair")
BODY_NEGATIVE = negative_prompts.get("body_negative", "distorted body, bad anatomy, extra limbs, missing limbs, unrealistic proportions")
BASE_NEGATIVE = negative_prompts.get("base_negative", "nude, naked, nsfw, badly drawn face, wrong face, deformed face, extra fingers, poorly drawn fingers, blurry, bad art, poor quality, worst quality")

# Check for CUDA availability and force CUDA usage
if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is required for this application. Please ensure you have a CUDA-compatible GPU and the correct drivers installed.")

device = "cuda"
dtype = torch.float16

# Enable optimal settings for CUDA
torch.backends.cuda.matmul.allow_tf32 = True  # Better performance on Ampere GPUs
torch.backends.cudnn.allow_tf32 = True

print(f"Using device: {device} with dtype: {dtype}")

# Print GPU information
cuda_device_count = torch.cuda.device_count()
print(f"Found {cuda_device_count} CUDA device(s)")
for i in range(cuda_device_count):
    print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
print(f"  Current device: {torch.cuda.current_device()}")
print(f"  Available memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

# Initialize pipeline with custom SDXL model
model_name = "juggernautXL_juggXIByRundiffusion.safetensors"
custom_model_path = os.path.abspath(os.path.join(script_dir, "..", "models", model_name))
vae_path = os.path.abspath(os.path.join(script_dir, "..", "models", "sdxl-vae-fp16-fix"))

print(f"Loading model from: {custom_model_path}")
print(f"Loading VAE from: {vae_path}")

# First load the VAE
try:
    vae = AutoencoderKL.from_pretrained(
        vae_path,
        torch_dtype=torch.float16
    ).to("cuda")
    print("Loaded local optimized VAE")
except Exception as e:
    print(f"Couldn't load local VAE, downloading default: {e}")
    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=torch.float16
    ).to("cuda")

# Initialize pipeline with the model
pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(
    custom_model_path,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
    vae=vae
).to("cuda")

# Enable memory optimizations
pipe.enable_attention_slicing()
try:
    pipe.enable_xformers_memory_efficient_attention()
    print("Using xformers for memory efficient attention")
except:
    print("xformers not available, using default attention")
torch.backends.cudnn.benchmark = True

@app.post("/generate/")
async def generate_images(
    prompt: str = Form(...),
    negative_prompt: str = Form(default=BASE_NEGATIVE),
    strength: float = Form(0.75),
    guidance_scale: float = Form(10.0),
    steps: int = Form(50),
    batch_size: int = Form(1),
    file: UploadFile = File(...)
):
    try:
        # Create output directory
        output_dir = f"output_{uuid.uuid4()}"
        os.makedirs(output_dir, exist_ok=True)

        # Performance message
        if device == "cuda":
            print(f"Using CUDA with {batch_size} batch size")
            # Limit batch size based on GPU memory
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            if vram_gb < 8 and batch_size > 1:
                print(f"Limited VRAM detected ({vram_gb:.1f}GB). Reducing batch size to 1 for stability.")
                batch_size = 1
        else:
            print("Using CPU. For better performance, please use a CUDA-compatible GPU.")
            batch_size = 1  # Force batch size of 1 on CPU

        # Process initial image
        init_image = Image.open(file.file).convert("RGB")
        width, height = init_image.size
        
        # SDXL prefers resolutions that are multiples of 1024x1024 or 768x768
        max_size = 1024  # Optimal for SDXL
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int((height / width) * max_size)
        else:
            new_height = max_size
            new_width = int((width / height) * max_size)
        
        # Ensure dimensions are multiples of 8 for the model
        new_width = (new_width // 8) * 8
        new_height = (new_height // 8) * 8
        
        # Use Lanczos resampling for high-quality resizing
        init_image = init_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Save input for reference
        input_path = f"{output_dir}/input_resized.png"
        init_image.save(input_path)

        # Extract color information from the prompt if available
        color_terms = ["red", "blue", "green", "yellow", "purple", "pink", "black", "white", 
                      "teal", "orange", "navy", "burgundy", "emerald", "gold", "silver"]
        
        # Check if any color term is in the prompt
        color_in_prompt = next((color for color in color_terms if color in prompt.lower()), None)
        
        # Extract expression information from the prompt
        expression_terms = ["smile", "happy", "serious", "fierce", "surprised", "seductive", "pensive", "thoughtful"]
        
        # Check if any expression term is in the prompt
        expression_in_prompt = next((expr for expr in expression_terms if expr in prompt.lower()), None)
        
        # Color change instructions
        if color_in_prompt:
            color_change = f"{color_in_prompt} dress, {color_in_prompt} fabric"
        else:
            color_change = "colored dress"
        
        # SDXL optimized prompt
        enhanced_prompt = f"{prompt}, {FACE_PRESERVATION}, {HAIR_PRESERVATION}, {EXPRESSION_MODIFIER}, {BODY_PRESERVATION}, {color_change}, {BASE_QUALITY}"

        # Add expression-specific negative prompts based on what's in the prompt
        expression_negative = ""
        if expression_in_prompt:
            # Create opposite negative expressions based on what's desired
            if "smile" in expression_in_prompt or "happy" in expression_in_prompt:
                expression_negative = "sad face, frowning, serious expression"
            elif "serious" in expression_in_prompt:
                expression_negative = "smiling face, grinning, laughing"
            elif "fierce" in expression_in_prompt:
                expression_negative = "timid face, meek expression"
            elif "surprised" in expression_in_prompt:
                expression_negative = "bored expression, uninterested face"
            elif "seductive" in expression_in_prompt:
                expression_negative = "childish expression, innocent face"
                
        # Simplified negative prompt for SDXL
        full_negative_prompt = f"{negative_prompt}, {FACE_NEGATIVE}, {HAIR_NEGATIVE}, {BODY_NEGATIVE}, {expression_negative}"

        # Try using compel for better prompt weighting if available
        try:
            from compel import Compel, ReturnedEmbeddingsType

            # Set up compel for SDXL (helps with prompt understanding)
            compel = Compel(
                tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
                text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
                returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
                requires_pooled=[False, True]
            )
            
            # Compel gives better prompt understanding and higher quality results
            conditioning, pooled = compel(enhanced_prompt)
            neg_conditioning, neg_pooled = compel(full_negative_prompt)
            
            # Use compel-generated embeddings for higher quality
            images = pipe(
                prompt_embeds=conditioning,
                pooled_prompt_embeds=pooled,
                negative_prompt_embeds=neg_conditioning,
                negative_pooled_prompt_embeds=neg_pooled,
                image=init_image,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=steps,
            ).images
            
            print("Used Compel for optimized prompt understanding")
            
        except ImportError:
            # Fallback to standard generation if compel isn't available
            print("Compel not available, using standard prompt processing")
            
            # Generate the image with SDXL
            images = pipe(
                prompt=[enhanced_prompt] * batch_size,
                image=[init_image] * batch_size,
                negative_prompt=[full_negative_prompt] * batch_size,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=steps,
            ).images

        # Save and return the result
        image_paths = []
        for idx, img in enumerate(images):
            path = f"{output_dir}/image_{idx}.png"
            img.save(path)
            image_paths.append(path)

        # Save metadata for reference
        with open(f"{output_dir}/generation_params.txt", "w") as f:
            f.write(f"Prompt: {enhanced_prompt}\n")
            f.write(f"Negative prompt: {full_negative_prompt}\n")
            f.write(f"Strength: {strength}\n")
            f.write(f"Guidance scale: {guidance_scale}\n")
            f.write(f"Steps: {steps}\n")
            f.write(f"Using device: {device}, dtype: {dtype}\n")

        return FileResponse(image_paths[0])

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))