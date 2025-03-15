from diffusers import StableDiffusionXLImg2ImgPipeline, AutoencoderKL
import torch
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import uuid
import os
import json
from diffusers.utils import load_image
from safetensors.torch import load_file

app = FastAPI()

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")
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
HAIR_PRESERVATION = face_settings.get("hair_preservation", "natural hair only, same hair style, same hair color, no head accessories")
EXPRESSION_MODIFIER = face_settings.get("expression_modifier", "pensive expression, slightly bigger anime-like eyes, dreamy gaze, thoughtful look, slightly larger eyes with love expression, anime influenced eye style, Roblox character style, 3D Roblox face")
BODY_PRESERVATION = face_settings.get("body_preservation", "preserve exact pose, same body position")
BASE_QUALITY = face_settings.get("base_quality", "high quality, detailed, professional photography")

# Extract negative prompts from config or use defaults
negative_prompts = config.get("negative_prompts", {})
FACE_NEGATIVE = negative_prompts.get("face_negative", "distorted face, deformed face, bad face, multiple faces, unrealistic face, face artifacts")
HAIR_NEGATIVE = negative_prompts.get("hair_negative", "weird hair, hair accessories, headpiece, crown, tiara, hat, anything on head")
BODY_NEGATIVE = negative_prompts.get("body_negative", "distorted body, bad anatomy, extra limbs, missing limbs, unrealistic proportions")
BASE_NEGATIVE = negative_prompts.get("base_negative", "nude, naked, nsfw, badly drawn face, wrong face, deformed face, extra fingers, poorly drawn fingers, blurry, bad art, poor quality, worst quality")

# Check for MPS (Metal Performance Shaders) availability on Mac
if torch.backends.mps.is_available():
    device = "mps"
    print("Using MPS (Metal Performance Shaders) for acceleration on Apple Silicon")
    dtype = torch.float32
else:
    device = "cpu"
    print("MPS not available, using CPU (this will be slow)")
    dtype = torch.float32

# Initialize pipeline with your custom SDXL model: EpicJuggernautXL
custom_model_path = "models/epicjuggernautxl_vxvXI.safetensors" # EpicJuggernautXL_vxvXI model

# Check if custom model exists
if os.path.exists(custom_model_path):
    print(f"Using custom SDXL model: {custom_model_path}")
    
    # Optional: Load improved VAE for better image reconstruction
    try:
        vae = AutoencoderKL.from_pretrained(
            "madebyollin/sdxl-vae-fp16-fix", 
            torch_dtype=dtype
        )
        print("Loaded optimized VAE for better image quality")
    except Exception as e:
        print(f"Couldn't load optimized VAE, using default: {e}")
        vae = None
    
    # Initialize SDXL pipeline with your custom model
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(
        custom_model_path,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
        use_safetensors=True,
        vae=vae  # Use the optimized VAE if available
    ).to(device)
    
    # Try to load LoRA for better face quality if available
    try:
        if os.path.exists("models/sd_xl_offset_example-lora_1.0.safetensors"):
            pipe.load_lora_weights("models/sd_xl_offset_example-lora_1.0.safetensors")
            print("Loaded LoRA weights for enhanced quality")
    except Exception as e:
        print(f"Couldn't load LoRA weights: {e}")
    
else:
    # If model doesn't exist, raise an error
    raise FileNotFoundError(f"Custom model not found at {custom_model_path}. Please ensure the model file exists.")

# Enable memory optimizations
pipe.enable_attention_slicing()

@app.post("/generate/")
async def generate_images(
    prompt: str = Form(...),
    negative_prompt: str = Form(default=BASE_NEGATIVE),
    strength: float = Form(0.75),  # Increased for more dramatic dress transformations for Roblox outfits
    guidance_scale: float = Form(10.0),  # Increased to enforce stronger adherence to the dress style prompt
    steps: int = Form(50),  # Increased for better detail preservation in transformed areas
    batch_size: int = Form(1),
    file: UploadFile = File(...)
):
    try:
        # Force batch_size to 1 for MPS
        if device == "mps" and batch_size > 1:
            print(f"Reducing batch size from {batch_size} to 1 for optimal MPS performance")
            batch_size = 1

        # Create a unique identifier for the output directory
        output_dir = f"tmp_{uuid.uuid4()}"
        os.makedirs(output_dir, exist_ok=True)

        # Open and process the initial image
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
        
        # SDXL optimized prompt - cleaner and more focused
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

        # Cap steps for performance but ensure enough for quality
        actual_steps = min(50, steps) if device == "mps" else steps
        
        # SDXL-specific feature: Add compel for better prompt weighting
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
                num_inference_steps=actual_steps,
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
                num_inference_steps=actual_steps,
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
            f.write(f"Steps: {actual_steps}\n")
            f.write(f"Using SDXL: {True if 'sdxl' in str(pipe.__class__).lower() else False}\n")

        return FileResponse(image_paths[0])

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))