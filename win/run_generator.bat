@echo off
echo Running ImageAlchemy Generator with GPU optimization...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables for optimal performance
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set HUGGINGFACE_HUB_CACHE=../models/huggingface_cache

:: Make sure the server is running
echo Please ensure that the server is running (run_windows.bat) in another terminal window.
echo.
echo Press any key to start the generator...
pause > nul

:: Run the generator script
echo Running generator script...
python generator.py

echo Generator process complete.
echo.
echo Press any key to exit...
pause > nul