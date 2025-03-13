#!/bin/bash

# Generator script for macOS
# This script activates the virtual environment and runs the generator

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Activate the virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Print message
echo "Starting ImageAlchemy Generator..."
echo "Project root: $PROJECT_ROOT"
echo "Make sure the API server is running and reference images are in the 'images' directory."
echo "------------------------------------"

# Run the generator
cd "$PROJECT_ROOT"
python src/generator.py

# Deactivate the virtual environment when done
deactivate