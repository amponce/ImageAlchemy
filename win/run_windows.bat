@echo off
echo Running ImageAlchemy with GPU optimization...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables for optimal performance
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set HUGGINGFACE_HUB_CACHE=../models/huggingface_cache

:: Start the server - using host 0.0.0.0 to make it accessible from other devices on the network
echo Starting FastAPI server with GPU optimization...
python -m uvicorn main:app --host 0.0.0.0 --reload

echo Server stopped.
echo.
echo Press any key to exit...
pause > nul