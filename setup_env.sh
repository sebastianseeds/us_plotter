#!/bin/bash

# Create virtual environment setup script for us_plotter project

echo "Setting up virtual environment for us_plotter..."

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required dependencies
echo "Installing dependencies..."
pip install matplotlib numpy

echo ""
echo "Setup complete!"
echo "To activate the environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the analysis script:"
echo "  python analyze_timeseries.py example_data.txt"