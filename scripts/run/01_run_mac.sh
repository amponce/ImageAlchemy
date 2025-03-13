#!/bin/bash

# Run script for macOS
# This script activates the virtual environment and starts the FastAPI server

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Activate the virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Print message
echo "Starting ImageAlchemy API Server..."
echo "Project root: $PROJECT_ROOT"
echo "Make sure you have placed your reference images in the 'images' directory."
echo "------------------------------------"

# Run the FastAPI server
cd "$PROJECT_ROOT"
python -m uvicorn main:app --reload

# Deactivate the virtual environment when the server is stopped
deactivate