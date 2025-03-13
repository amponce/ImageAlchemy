# Model Files

This directory is used to store AI model files for ImageAlchemy.

## Required Models

The application uses the following models:

- **EpicJuggernautXL_vxvXI** - A custom Stable Diffusion XL model optimized for fashion and portrait photography
- **sd_xl_offset_example-lora_1.0.safetensors** (optional) - A LoRA for improved face quality

## Getting the Models

The models will be automatically downloaded when running the setup scripts:

- `setup_custom_sdxl.sh` (macOS/Linux)
- `win\setup_custom_sdxl.bat` (Windows)

You can also manually download them:

1. EpicJuggernautXL: [https://civitai.com/models/133005](https://civitai.com/models/133005)
2. Place the downloaded model file in this directory and rename it to `epicjuggernautxl_vxvXI.safetensors`

## Using Different Models

To use a different SDXL model:

1. Place your model file (in safetensors format) in this directory
2. Update the `custom_model_path` variable in `main.py` to point to your model file

```python
custom_model_path = "models/your_model_filename.safetensors"
```

## Alternative Model Sources

- [Civitai](https://civitai.com/)
- [Hugging Face](https://huggingface.co/models)