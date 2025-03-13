#!/bin/bash
# cleanup.sh - Clean up temporary output folders

echo "Cleaning up temporary output directories..."

# Remove all output folders
find . -type d -name "output_*" -exec rm -rf {} \; 2>/dev/null
find . -type d -name "tmp_*" -exec rm -rf {} \; 2>/dev/null

echo "Cleanup complete!"