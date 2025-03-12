#!/bin/bash

# Run script for ImageAlchemy AI on macOS

echo "Starting ImageAlchemy AI server on macOS..."

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "Starting FastAPI server with Metal acceleration..."
uvicorn main:app --reload

# The server will be available at http://localhost:8000 