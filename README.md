# ImageAlchemy: AI Outfit Generator

**Transform character models with AI-powered outfit variations**

ImageAlchemy is an open-source image generation tool that specializes in creating outfit variations for character models in different colors and styles. The application uses Stable Diffusion XL to transform images with customizable outfits while maintaining the character's core facial features.

## Showcase Gallery


| Yellow | Teal | Red | Purple |
|--------|------|-----|--------|
| <img src="https://github.com/user-attachments/assets/e5f158fd-ba9a-4f12-813f-0b7f50a7d1a4" width="180"> | <img src="https://github.com/user-attachments/assets/85c807d6-5807-4ff3-b3c7-c9a6c17c5905" width="180"> | <img src="https://github.com/user-attachments/assets/73462ec0-44b4-479f-8875-2dfe0900d247" width="180"> | <img src="https://github.com/user-attachments/assets/df2ca571-49e6-4eb4-8b35-591773779dbf" width="180"> |

| Pink | Green | Blue |
|------|-------|------|
| <img src="https://github.com/user-attachments/assets/650232aa-44c9-4145-af47-75b8a358f053" width="180"> | <img src="https://github.com/user-attachments/assets/0c61361d-fd8e-494b-a222-8ecc63785a41" width="180"> | <img src="https://github.com/user-attachments/assets/7d07d5f6-c943-4632-a23c-44ebcc453717" width="180"> |



| Yellow | Teal | Red | Purple |
|--------|------|-----|--------|
| <img src="https://github.com/user-attachments/assets/349b04df-b459-403d-9681-bef806d27bab" width="180"> | <img src="https://github.com/user-attachments/assets/6aee3916-4b3e-4068-afad-94bac88c9d36" width="180"> | <img src="https://github.com/user-attachments/assets/691224c3-bc28-4d43-86fc-156bccbc0d8d" width="180"> | <img src="https://github.com/user-attachments/assets/268cde57-d037-488b-8209-d251e2bad8fa" width="180"> |

| Pink | Green | Blue |
|------|-------|------|
| <img src="https://github.com/user-attachments/assets/a5dd6da9-08e8-4d1f-8912-7af98bebdca4" width="180"> | <img src="https://github.com/user-attachments/assets/d961e3ca-0a7e-406a-ae51-92c19fc5d958" width="180"> | <img src="https://github.com/user-attachments/assets/806b6f6c-ba97-450e-8994-d9d086652eac" width="180"> |



| Yellow | Teal | Red | Purple |
|--------|------|-----|--------|
| <img src="https://github.com/user-attachments/assets/768390ff-88e6-4ecb-ba6e-9eabebc75bef" width="180"> | <img src="https://github.com/user-attachments/assets/e5a2b1d5-7d3b-426b-89e6-5d26ea672a69" width="180"> | <img src="https://github.com/user-attachments/assets/abfa1bd0-f82c-42ef-b925-f7af498079d3" width="180"> | <img src="https://github.com/user-attachments/assets/09058a7c-6db9-482d-8ef4-468119885c56" width="180"> |

| Pink | Green | Blue |
|------|-------|------|
| <img src="https://github.com/user-attachments/assets/243aaf95-8aa5-4953-a90f-b2ed440de9f9" width="180"> | <img src="https://github.com/user-attachments/assets/6e93828f-20bf-42aa-b914-dda00ee37ac4" width="180"> | <img src="https://github.com/user-attachments/assets/6083bad4-f3f5-44a8-b03d-e5dd25e7c4e6" width="180"> |



### Examples and Control Images


| Control 1 | Control 2 | Control 3 |
|-----------|-----------|-----------|
| <img src="https://github.com/user-attachments/assets/7b3c4879-4457-4b9e-beb7-922cb969d9d5" width="180"> | <img src="https://github.com/user-attachments/assets/9ad63f95-7ada-4d89-bffc-52e766f1fec2" width="180"> | <img src="https://github.com/user-attachments/assets/072742ec-d08a-44e5-a522-774ea2b38a94" width="180"> |






## Features

- Create outfit variations for any character style with different colors and patterns
- Support for multiple style configurations (anime, cartoon, realistic, and more)
- Preserve the character's face and body structure
- Maintain consistent expressions and key character features
- Automatically cycle through reference images
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

Generated images are saved in a timestamped directory with format: `variations_YYYYMMDD_HHMMSS/`

### API Endpoints

#### POST /generate/

Generate variations of an uploaded image based on a text prompt.

**Parameters:**
- `prompt`: Text description of the desired outfit
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
  -F "file=@path/to/your/character.jpg" \
  -F "prompt=A character in a red dress with elegant design" \
  -F "strength=0.75" \
  -F "guidance_scale=10.0" \
  -F "steps=50"
```

## Style Showcase

ImageAlchemy supports multiple character styles that can be configured through prompt settings:

### NieR Automata Style
Transform your character with YoRHa-inspired outfits, blindfolds, and android aesthetics.

### Cartoon Style
Create bright, colorful cartoon character variations with stylized proportions.

### Anime Style
Generate anime-inspired character outfits with typical anime aesthetics.

And many more styles limited only by your imagination and prompt engineering skills!

## Customization

### Modifying Prompts

The application uses a modular prompt system to generate variations:

1. **Edit outfit styles**:
   - Modify `prompts/outfit_styles.json` to change colors or outfit descriptions
   - Add new outfit styles by following the existing format

2. **Edit character characteristics**:
   - Modify `prompts/character_styles.json` to change the expression or features
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
│   ├── character_styles.json  # Character characteristic prompts
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
