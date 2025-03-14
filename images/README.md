# Reference Images

This directory contains reference Roblox character images used by the ImageAlchemy generator.

## Included Images

The repository includes sample Roblox character images for demonstration:

- `runway_model.jpeg` - Example Roblox character model
- `runway_model_2.jpeg` - Additional Roblox character example
- `runway_model_3.jpeg` - Additional Roblox character example

## Adding Your Own Images

1. Place your own Roblox character reference images in this directory
2. Supported formats: `.jpg`, `.jpeg`, `.png`
3. For best results:
   - Use high-quality Roblox character images
   - Choose images with clear, well-lit characters
   - Select images with neutral backgrounds
   - Prefer full-body or 3/4 shots of characters

## How Images Are Used

The generator script (`generator.py`) will:

1. Discover all images in this directory automatically
2. Cycle through them when creating different Roblox outfit variations
3. Preserve the character's face and pose while changing outfit colors and styles
4. Output variations that match each reference image

