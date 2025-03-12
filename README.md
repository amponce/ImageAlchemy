# Image Generation API

This is a FastAPI-based web service that provides image generation capabilities using Stable Diffusion. The service allows users to upload an image and generate variations based on text prompts.

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU with at least 8GB VRAM (for Windows/Linux)
- CUDA toolkit installed (for Windows/Linux)
- macOS 12.0+ with Apple Silicon (for Mac users)
- Windows/Linux/macOS operating system

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd imageGen
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

Note: If you're using Windows and encounter issues with torch installation, you may need to install it separately first:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Mac Installation

For Mac Mini and other Apple Silicon (M1/M2/M3) devices, we provide optimized versions of the application in the `osx` folder:

1. Navigate to the osx directory:
```bash
cd osx
```

2. Run the Mac-specific setup script:
```bash
chmod +x setup_mac.sh
./setup_mac.sh
```

This will create a virtual environment and install all the required dependencies optimized for Apple Silicon.

## Running the Application

1. Activate the virtual environment if not already activated:
```bash
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

2. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### Running on Mac

To run on Mac, use the provided run script in the osx directory:
```bash
cd osx
./run_mac.sh
```

Or manually:
```bash
cd osx
source venv/bin/activate
uvicorn main:app --reload
```

## API Endpoints

### POST /generate/
Generates variations of an uploaded image based on a text prompt.

**Parameters:**
- `prompt` (string, required): Text description of the desired image modification
- `strength` (float, optional, default=0.6): How much to transform the reference image (0-1)
- `guidance_scale` (float, optional, default=7.5): How closely to follow the prompt
- `steps` (int, optional, default=50): Number of denoising steps
- `batch_size` (int, optional, default=1): Number of images to generate
- `file` (file, required): Input image file

**Response:**
- Returns the generated image as a file download

## Example Usage

You can use tools like cURL, Postman, or any HTTP client to interact with the API. Here's an example using cURL:

```bash
curl -X POST "http://localhost:8000/generate/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg" \
  -F "prompt=your text prompt here" \
  -F "strength=0.7" \
  -F "guidance_scale=7.5" \
  -F "steps=50" \
  -F "batch_size=1"
```

## Batch Generation with generator.py

The repository includes a `generator.py` script that can automatically generate multiple variations of an image using different styles, colors, and design elements.

### Setup for generator.py

1. Place your input image in the `images` directory
2. Configure the script parameters at the top of `generator.py`:
   - `input_image_path`: Path to your reference image
   - `num_variations`: Number of variations to generate (default: 5)

### Running the Generator

```bash
python generator.py
```

For Mac users:
```bash
cd osx
python generator.py
```

The script will:
- Automatically resize large images for optimal processing
- Generate variations using random combinations of:
  - Style modifiers (floral, polka dot, striped, etc.)
  - Color schemes (red, blue, green, etc.)
  - Design elements (sleeveless, v-neck, A-line, etc.)
- Save outputs in a timestamped directory
- Create a text file for each generation with the prompt details

### Output

The script creates a new directory named `dress_variations_YYYYMMDD_HHMMSS` containing:
- Generated images in PNG format
- Accompanying text files with generation parameters
- Resized input image (if applicable)

Each generated image filename includes the style, color, and design elements used in its creation.

## Mac-Specific Features

For Mac Mini and Apple Silicon users:
- Uses Metal Performance Shaders (MPS) instead of CUDA for acceleration
- Optimized parameters for better performance on Apple chips:
  - Default step count: 30 (vs 50 on CUDA)
  - Fixed batch size: 1
  - Increased timeout for first-time model compilation

## Notes

- The service requires a GPU for acceleration (CUDA on Windows/Linux, Metal on Mac)
- Input images are automatically resized to 768x768 pixels
- Generated images are saved in automatically created output directories
- For optimal performance:
  - Windows/Linux: Ensure your GPU has sufficient VRAM
  - Mac: First generation may be slower as models are compiled for Metal
