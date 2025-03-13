@echo off
echo Setting up ImageAlchemy for Windows with GPU Optimization...

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install or upgrade pip
python -m pip install --upgrade pip

:: Install torch with CUDA support (latest version)
echo Installing PyTorch with CUDA support (latest version)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

:: Install xformers for memory efficiency (GPU optimization)
echo Installing xformers for GPU memory optimization...
pip install xformers

:: Install other dependencies including accelerate for even more optimization
echo Installing other dependencies with GPU optimizations...
pip install -r ..\requirements.txt

:: Install additional performance optimizers
echo Installing additional performance optimizers...
pip install accelerate>=0.27.0 --upgrade
pip install ninja>=1.11.0 --upgrade
pip install compel>=2.0.2 --upgrade

:: Create parent models directory if it doesn't exist
if not exist ..\models mkdir ..\models

echo Setup complete! System is optimized for maximum GPU performance.
echo.
echo Run setup_custom_sdxl.bat next to download the required model files.
echo Then use run_windows.bat to start the application.
echo.
echo Press any key to exit...
pause > nul