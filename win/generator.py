import requests
import json
import os
import time
import random
from PIL import Image
import datetime
import traceback
import shutil

# Configuration
api_url = "http://localhost:8000/generate/"  # Your FastAPI endpoint
# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir) 

# Load configuration file
config_path = os.path.join(parent_dir, "config.json")
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    print(f"Loaded configuration from {config_path}")
except Exception as e:
    print(f"Error loading configuration: {e}")
    print("Using default configuration")
    config = {
        "global_settings": {
            "strength": 0.75,
            "guidance_scale": 10.0,
            "steps": 50,
            "batch_size": 1
        },
        "dress_colors": []
    }

# Reference images for context (all images in the parent images directory)
reference_images_dir = os.path.join(parent_dir, "images")
reference_image_paths = [os.path.join(reference_images_dir, f) for f in os.listdir(reference_images_dir) 
                        if f.endswith(('.jpg', '.jpeg', '.png')) and os.path.isfile(os.path.join(reference_images_dir, f))]
print(f"Found {len(reference_image_paths)} reference images: {[os.path.basename(p) for p in reference_image_paths]}")

# Rotating through all reference images
if not reference_image_paths:
    print("Error: No reference images found in the images directory.")
    exit(1)

output_folder = f"dress_colors_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
num_variations = min(len(config["dress_colors"]), 7)  # Number of different dress colors to generate, limited by config

print(f"Will generate {num_variations} variations based on config file")

# Create output folder if it doesn't exist
output_folder = f"dress_colors_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(output_folder, exist_ok=True)

print(f"Starting generation process. Images will be saved to: {os.path.abspath(output_folder)}")

# Copy all reference images to output folder
try:
    # Create a reference subfolder in the output directory
    reference_output_dir = os.path.join(output_folder, "reference_images")
    os.makedirs(reference_output_dir, exist_ok=True)
    
    # Copy all reference images to the output folder for context
    for ref_img_path in reference_image_paths:
        ref_img_name = os.path.basename(ref_img_path)
        ref_img_output_path = os.path.join(reference_output_dir, ref_img_name)
        shutil.copy2(ref_img_path, ref_img_output_path)
        print(f"Copied reference image {ref_img_name} to output folder for context")
    
except Exception as e:
    print(f"Error: Could not process reference images: {e}")
    exit(1)

# Copy the configuration file to output folder for reference
try:
    config_output_path = os.path.join(output_folder, "used_config.json")
    shutil.copy2(config_path, config_output_path)
    print(f"Copied configuration file to output folder for reference")
except Exception as e:
    print(f"Warning: Could not copy configuration file: {e}")

# Get global settings from config
global_settings = config.get("global_settings", {})
strength = global_settings.get("strength", 0.75)
guidance_scale = global_settings.get("guidance_scale", 10.0)
steps = global_settings.get("steps", 50)
batch_size = global_settings.get("batch_size", 1)

# Generate variations using all reference images
for i, variation in enumerate(config["dress_colors"][:num_variations]):
    print(f"\nGenerating variation {i+1}/{num_variations}: {variation['name']}")
    
    # Use a different reference image for each variation (cycling through them)
    input_image_path = reference_image_paths[i % len(reference_image_paths)]
    print(f"Using reference image: {os.path.basename(input_image_path)}")
    
    prompt = variation["prompt"]
    negative_prompt = variation["negative_prompt"]
    
    # Make API request
    try:
        print(f"  Prompt: {prompt}")
        print(f"  Negative prompt: {negative_prompt}")
        print("  Sending request to API...")
        
        with open(input_image_path, 'rb') as img_file:
            files = {
                'file': (os.path.basename(input_image_path), img_file),
            }
            
            data = {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'strength': str(strength),
                'guidance_scale': str(guidance_scale),
                'steps': str(steps),
                'batch_size': str(batch_size)
            }
            
            # Add timeout to prevent hanging indefinitely
            response = requests.post(api_url, files=files, data=data, timeout=300)
            
            print(f"  Response received! Status code: {response.status_code}")
            
            if response.status_code == 200:
                # Include reference image name in the output filename
                ref_img_basename = os.path.basename(input_image_path).split('.')[0]
                image_filename = os.path.join(
                    output_folder, 
                    f"{variation['name']}_{ref_img_basename}.png"
                )
                
                # Save the image received from the API
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"  Successfully saved: {image_filename}")
                
            else:
                print(f"  Error: {response.status_code}")
                try:
                    error_details = response.json()
                    print(f"  Error details: {json.dumps(error_details, indent=2)}")
                except:
                    print(f"  Response text: {response.text[:200]}...")
    
    except Exception as e:
        print(f"  Error: {e}")
        traceback.print_exc()
    
    # Add a delay between requests
    delay = random.uniform(2.0, 3.0)
    print(f"  Waiting {delay:.1f} seconds before next generation...")
    time.sleep(delay)

print("\nAll variations generated!")
print(f"Output saved to {os.path.abspath(output_folder)}")
print("Generation process complete.")