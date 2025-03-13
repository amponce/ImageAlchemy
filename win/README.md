# ImageAlchemy for Windows with GPU Optimization

This directory contains Windows-specific scripts for running ImageAlchemy with optimized GPU support.

## System Requirements

- Windows 10 or 11
- NVIDIA GPU with CUDA support
- Python 3.10 or newer (Python 3.10 is recommended)
- Git (for downloading the repository)

## GPU Memory Requirements

- 8GB+ VRAM: Recommended for optimal performance
- 4-6GB VRAM: Will work with optimizations
- <4GB VRAM: May require model pruning or lower resolution

## Quick Setup Guide

1. **Initial Setup**: Run `setup_windows.bat` to create the virtual environment and install dependencies
2. **Download Models**: Run `setup_custom_sdxl.bat` to download required model files
3. **Start Server**: Run `run_windows.bat` to start the FastAPI server
4. **Run Generator**: In a separate command prompt, run `run_generator.bat` to generate variations

## Advanced Configuration

You can modify `config.json` in the parent directory to customize:
- Dress colors and styles
- Face and body preservation settings
- Negative prompts
- Global generation settings

## Performance Optimizations

This Windows version includes:
- CUDA optimization with xformers
- Float16 precision for faster processing
- Automatic batch size adjustment based on available VRAM
- cuDNN benchmark mode for optimal performance
- Memory-efficient attention mechanisms

## Troubleshooting

**Out of Memory (OOM) errors**:
- Reduce batch size in config.json
- Reduce image resolution
- Make sure no other GPU-intensive applications are running

**Slow Generation**:
- Verify CUDA is being used (check console output)
- Reduce step count in config.json
- Update GPU drivers

## Additional Resources

- Original project documentation is in the parent directory
- Check NVIDIA drivers are up to date
- Use `nvidia-smi` command to monitor GPU usage

*The Windows version maintains full compatibility with the main project while adding GPU optimizations.*