#!/bin/bash

# Setup script for ImageAlchemy AI on macOS with Apple Silicon

echo "Setting up ImageAlchemy AI for macOS with Apple Silicon..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Install PyTorch with MPS support
echo "Installing PyTorch with Metal support for Apple Silicon..."
pip install torch torchvision

# Install the remaining requirements
echo "Installing other dependencies..."
pip install -r requirements.txt

# Create images directory if it doesn't exist
mkdir -p images

# Make run script executable
chmod +x run_mac.sh

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run the application on your Mac:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start the server: uvicorn main:app --reload"
echo "3. The application will be available at http://localhost:8000"
echo ""
echo "You can also use the run_mac.sh script to start the server: ./run_mac.sh" 