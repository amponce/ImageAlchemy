import requests
import json
import os
import time
import random
from PIL import Image
import datetime
import traceback

# Configuration
api_url = "http://localhost:8000/generate/"  # Your FastAPI endpoint
input_image_path = "images/dress_1.jpeg"  # Your reference dress image
output_folder = f"dress_variations_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
num_variations = 5  # Number of variations to generate

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

print(f"Starting generation process. Images will be saved to: {os.path.abspath(output_folder)}")

# Check if input image exists and resize it if needed
try:
    input_img = Image.open(input_image_path)
    width, height = input_img.size
    print(f"Input image dimensions: {width}x{height}")
    
    # If image is very large, resize it to help with processing
    if width > 1024 or height > 1024:
        # Keep aspect ratio
        if width > height:
            new_width = 1024
            new_height = int((height / width) * 1024)
        else:
            new_height = 1024
            new_width = int((width / height) * 1024)
            
        resized_path = os.path.join(output_folder, "resized_input.jpg")
        input_img.resize((new_width, new_height), Image.LANCZIN).save(resized_path, quality=95)
        input_image_path = resized_path
        print(f"Resized image to {new_width}x{new_height} to optimize for processing")
except Exception as e:
    print(f"Warning: Could not process input image: {e}")
    print("Continuing with original image...")

# Enhanced style and color modifiers for variety
style_modifiers = [
    "floral pattern", "polka dot", "striped", "elegant", "vintage", 
    "modern", "summer", "formal", "casual", "couture", "embroidered",
    "lace", "silk", "satin", "cotton", "tulle", "sequined", "minimalist",
    "bohemian", "artistic", "geometric", "abstract", "paisley", "checkered",
    "tie-dye", "damask", "houndstooth", "herringbone", "baroque"
]

color_modifiers = [
    "red", "blue", "green", "yellow", "purple", "pink", "black", "white", 
    "teal", "orange", "navy", "burgundy", "emerald", "gold", "silver",
    "pastel", "multicolored", "ombre", "monochrome", "coral", "turquoise",
    "lavender", "mint", "olive", "peach", "rose gold", "champagne", "ivory"
]

design_elements = [
    "sleeveless", "short sleeve", "long sleeve", "off-shoulder", "strapless",
    "v-neck", "high neck", "halter", "A-line", "fitted", "pleated", "tiered",
    "asymmetrical", "midi length", "maxi length", "mini length", "belted",
    "peplum", "bodycon", "wrap", "shift", "sheath", "mermaid", "ballgown",
    "princess", "empire waist", "pencil", "column", "trumpet", "tea length",
    "high-low", "cape", "backless", "cutout", "one-shoulder"
]

# Additional quality and context modifiers
photo_quality = [
    "8k resolution", "high definition", "studio lighting", "professional photography",
    "magazine cover", "high fashion editorial", "catwalk", "fashion week",
    "professional model", "sharp focus", "perfect lighting", "award-winning photography"
]

# Generate variations
for i in range(num_variations):
    print(f"\nGenerating variation {i+1}/{num_variations}")
    
    # Choose random modifiers
    style = random.choice(style_modifiers)
    color = random.choice(color_modifiers)
    design = random.choice(design_elements)
    
    # Build varied prompt
    base_prompt = f"a beautiful {style} {color} {design} dress on runway model, fashion show, high quality, detailed fabric"
    
    # Add 1-2 quality modifiers for better results
    quality_mods = random.sample(photo_quality, k=random.randint(1, 2))
    quality_text = ", " + ", ".join(quality_mods)
    
    # Build final prompt
    prompt = base_prompt + quality_text
    
    # Occasionally add seasonal or occasion-specific modifiers
    if random.random() < 0.4:
        seasons = ["spring", "summer", "fall", "winter"]
        occasions = ["evening", "cocktail", "wedding", "casual", "office", "party", "gala", "red carpet"]
        extra = random.choice(seasons + occasions)
        prompt += f", {extra} wear"
    
    # Randomize strength parameter - lower values preserve more of the original structure
    strength = random.uniform(0.55, 0.70)
    
    # Make API request
    try:
        print(f"  Prompt: {prompt}")
        print(f"  Strength: {strength}")
        print("  Sending request to API...")
        
        # Use context manager for file handling to ensure it closes properly
        with open(input_image_path, 'rb') as img_file:
            files = {
                'file': (os.path.basename(input_image_path), img_file),
            }
            
            data = {
                'prompt': prompt,
                'strength': str(strength),
                'guidance_scale': '7.0',  # Slightly lower guidance scale for more creative results
                'steps': '30',  # Reduced steps for faster generation while maintaining quality
                'batch_size': '1'
            }
            
            # Add timeout to prevent hanging indefinitely
            response = requests.post(api_url, files=files, data=data, timeout=180)
            
            print(f"  Response received! Status code: {response.status_code}")
            
            if response.status_code == 200:
                # Generate filename with style info
                style_slug = style.replace(" ", "_")
                color_slug = color.replace(" ", "_")
                design_slug = design.replace(" ", "_")
                
                image_filename = os.path.join(
                    output_folder, 
                    f"dress_{style_slug}_{color_slug}_{design_slug}_{i+1}.png"
                )
                
                # Save the image received from the API
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                # Save prompt info alongside image
                info_filename = os.path.join(
                    output_folder,
                    f"dress_{style_slug}_{color_slug}_{design_slug}_{i+1}.txt"
                )
                
                with open(info_filename, "w") as f:
                    f.write(f"Prompt: {prompt}\n")
                    f.write(f"Strength: {strength}\n")
                    f.write(f"Guidance Scale: 7.0\n")
                    f.write(f"Steps: 30\n")
                    f.write(f"Generation {i+1} of {num_variations}\n")
                    f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                print(f"  Successfully saved: {image_filename}")
                
                # Optional: display a thumbnail in the console output
                try:
                    img = Image.open(image_filename)
                    print(f"  Image dimensions: {img.width}x{img.height}")
                except:
                    print("  (Could not read image dimensions)")
                
            else:
                print(f"  Error: {response.status_code}")
                try:
                    error_details = response.json()
                    print(f"  Error details: {json.dumps(error_details, indent=2)}")
                except:
                    print(f"  Response text: {response.text[:200]}...")
    
    except requests.exceptions.Timeout:
        print("  Error: Request timed out after 180 seconds. The server may be overloaded.")
        print("  Try reducing the number of steps or the image resolution.")
        
    except requests.exceptions.ConnectionError:
        print("  Error: Connection error. Make sure the API server is running at:", api_url)
        
    except Exception as e:
        print(f"  Request error: {e}")
        print("  Detailed error information:")
        traceback.print_exc()
    
    # Add a delay between requests to avoid overwhelming the API
    delay = random.uniform(1.0, 3.0)
    print(f"  Waiting {delay:.1f} seconds before next generation...")
    time.sleep(delay)

print("\nAll variations generated!")
print(f"Output saved to {os.path.abspath(output_folder)}")
print("Generation process complete.")