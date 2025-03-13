# ImageAlchemy: Roblox Outfit Generator

**Transform character models with AI-powered Roblox outfit variations**

ImageAlchemy is an open-source image generation tool that specializes in creating variations of Roblox character models with different outfit colors and styles. The application uses Stable Diffusion XL to transform images with customizable Roblox-style outfits while maintaining the character's facial features.

![ImageAlchemy Demo](https://github.com/username/ImageAlchemy/raw/main/docs/demo.png)

## Features

- Create Roblox outfit variations with different colors and patterns
- Preserve the character's face and body structure
- Consistent pensive expression with slightly larger anime-like eyes
- Automatically cycles through reference images
- Customizable strength, guidance, and quality settings
- macOS optimized with Metal Performance Shaders support
- Windows and Linux compatible with CUDA acceleration

## Getting Started

### Prerequisites

- Python 3.8 or higher
- For GPU acceleration:
  - NVIDIA GPU with CUDA support (Windows/Linux)
  - Apple Silicon or Intel Mac with Metal support (macOS)

### Quick Start

For the fastest setup, follow these steps in order:

1. **Setup your environment**:
   ```bash
   # macOS
   chmod +x scripts/setup/01_setup_mac.sh
   ./scripts/setup/01_setup_mac.sh
   
   # Windows
   scripts\setup\01_setup_windows.bat
   ```

2. **Setup the AI model**:
   ```bash
   # macOS/Linux
   chmod +x scripts/setup/02_setup_sdxl.sh
   ./scripts/setup/02_setup_sdxl.sh
   
   # Optional custom model
   chmod +x scripts/setup/03_setup_custom_sdxl.sh
   ./scripts/setup/03_setup_custom_sdxl.sh
   ```

3. **Run the server**:
   ```bash
   # macOS
   chmod +x scripts/run/01_run_mac.sh
   ./scripts/run/01_run_mac.sh
   
   # Windows
   scripts\run\01_run_windows.bat
   ```

4. **Generate images**:
   ```bash
   # macOS
   chmod +x scripts/run/02_run_generator_mac.sh
   ./scripts/run/02_run_generator_mac.sh
   
   # Windows
   scripts\run\02_run_generator_windows.bat
   ```

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

## Usage

### Running the API Server

```bash
# macOS
./run_mac.sh

# Windows/Linux
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`

### Generating Images

1. Place reference images in the `images` directory
2. Run the batch generator:

```bash
python generator.py
```

Generated images are saved in a timestamped directory with format: `dress_colors_YYYYMMDD_HHMMSS/`

### API Endpoints

#### POST /generate/

Generate variations of an uploaded image based on a text prompt.

**Parameters:**
- `prompt`: Text description of the desired Roblox outfit
- `negative_prompt` (optional): Elements to avoid in the generated image
- `strength` (default=0.75): How much to transform the reference image (0-1)
- `guidance_scale` (default=10.0): How closely to follow the prompt
- `steps` (default=50): Number of denoising steps
- `batch_size` (default=1): Number of images to generate
- `file`: Input image file

**Example with cURL:**

```bash
curl -X POST "http://localhost:8000/generate/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/roblox_character.jpg" \
  -F "prompt=A Roblox character in a red outfit, pensive expression" \
  -F "strength=0.75" \
  -F "guidance_scale=10.0" \
  -F "steps=50"
```

## Customization

### Modifying Prompts

The application uses a modular prompt system to generate variations:

1. **Edit outfit styles**:
   - Modify `prompts/outfit_styles.json` to change colors or outfit descriptions
   - Add new outfit styles by following the existing format

2. **Edit face characteristics**:
   - Modify `prompts/face_styles.json` to change the facial expression or features
   - Adjust the "expression_modifier" for different looks

3. **Edit negative prompts**:
   - Modify `prompts/negative_prompts.json` to control what to avoid in generations

All prompt components are automatically combined using the prompt builder utility.

## Project Structure

```
ImageAlchemy/
├── config/                    # Configuration files
│   └── default_config.json    # Main configuration
├── docs/                      # Documentation
├── images/                    # Reference images directory
├── models/                    # AI model files
├── prompts/                   # Modular prompt components
│   ├── face_styles.json       # Face characteristic prompts
│   ├── negative_prompts.json  # Negative prompt components
│   └── outfit_styles.json     # Outfit style variations
├── scripts/                   # Organized scripts
│   ├── setup/                 # Installation scripts
│   │   ├── 01_setup_mac.sh    # macOS environment setup
│   │   ├── 02_setup_sdxl.sh   # SDXL model setup
│   │   └── 03_setup_custom_sdxl.sh  # Custom model setup
│   ├── run/                   # Execution scripts
│   │   └── 01_run_mac.sh      # macOS launcher
│   └── utils/                 # Utility scripts
│       ├── cleanup.sh         # Cleanup utilities
│       └── prompt_builder.py  # Prompt building utility
├── main.py                    # FastAPI server and image generation core
├── generator.py               # Batch generation script
├── requirements.txt           # Python dependencies
├── INSTALLATION.md            # Step-by-step installation guide
└── README.md                  # Project documentation
```

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md).

## Performance Notes

- **macOS**: First generation may be slower as models compile for Metal
- **Windows/Linux**: CUDA acceleration requires a compatible NVIDIA GPU
- Reduce batch size to 1 for better performance on lower-end hardware
- Adjust `steps` parameter based on your hardware capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- Utilizes [EpicJuggernautXL](https://civitai.com/models/133005) custom model
- Powered by [HuggingFace Diffusers](https://github.com/huggingface/diffusers)