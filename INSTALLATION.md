# ImageAlchemy Installation Guide

This guide provides step-by-step instructions for installing and running ImageAlchemy.

## Installation Process

Follow these steps in order:

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ImageAlchemy.git
cd ImageAlchemy
```

### Step 2: Setup the Environment

#### For macOS:

```bash
# Make the setup script executable
chmod +x scripts/setup/01_setup_mac.sh

# Run the macOS setup script
./scripts/setup/01_setup_mac.sh
```

#### For Windows:

```bash
# Run the Windows setup script
scripts\setup\01_setup_windows.bat
```

#### For Linux:

```bash
# Make the setup script executable
chmod +x scripts/setup/01_setup_linux.sh

# Run the Linux setup script
./scripts/setup/01_setup_linux.sh
```

### Step 3: Set Up the Stable Diffusion XL Model

```bash
# Make the script executable (macOS/Linux)
chmod +x scripts/setup/02_setup_sdxl.sh

# Run the SDXL setup script
./scripts/setup/02_setup_sdxl.sh
```

### Step 4: (Optional) Set Up the Custom Model

If you want to use the custom EpicJuggernautXL model:

```bash
# Make the script executable (macOS/Linux)
chmod +x scripts/setup/03_setup_custom_sdxl.sh

# Run the custom model setup script
./scripts/setup/03_setup_custom_sdxl.sh
```

## Running ImageAlchemy

### Step 1: Start the API Server

#### For macOS:

```bash
# Make the run script executable
chmod +x scripts/run/01_run_mac.sh

# Run the macOS startup script
./scripts/run/01_run_mac.sh
```

#### For Windows:

```bash
# Run the Windows startup script
scripts\run\01_run_windows.bat
```

#### For Linux:

```bash
# Make the run script executable
chmod +x scripts/run/01_run_linux.sh

# Run the Linux startup script
./scripts/run/01_run_linux.sh
```

### Step 2: Generate Images

1. Place reference images in the `images/` directory.
2. Run the generation script:

```bash
# Activate the virtual environment if not already activated
source venv/bin/activate  # For macOS/Linux
# OR
.\venv\Scripts\activate   # For Windows

# Run the generator
python generator.py
```

Generated images will be saved in a timestamped directory with format: `dress_colors_YYYYMMDD_HHMMSS/`.

## Advanced Usage

### Customizing Prompts

You can customize prompts by editing the following files:

- `prompts/outfit_styles.json` - Contains different outfit styles and colors
- `prompts/face_styles.json` - Controls the facial expression and preservation
- `prompts/negative_prompts.json` - Controls what to avoid in generated images

### Modifying Global Settings

Edit `config/default_config.json` to change global settings like:
- Image generation strength
- Guidance scale
- Number of steps
- Batch size

## Troubleshooting

If you encounter any issues:

1. Ensure all prerequisites are installed.
2. Check that virtual environment is activated.
3. Verify model files are downloaded correctly.
4. For macOS Metal issues, ensure you have the latest OS updates.
5. For CUDA issues on Windows/Linux, verify your GPU drivers are up to date.

## Cleanup

To clean up temporary files or reset the installation:

```bash
# Run the cleanup script
./scripts/utils/cleanup.sh
```