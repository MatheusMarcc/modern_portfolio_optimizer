#!/bin/bash

# Portfolio Optimizer - Automated Setup Script
# Run: bash setup.sh

echo "========================================"
echo "Portfolio Optimizer - Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+ first."
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found: Python $PYTHON_VERSION"

# Extract major and minor version
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8+ required. Found: $PYTHON_VERSION"
    exit 1
fi

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 13 ]; then
    echo "WARNING: Python 3.13+ may have compatibility issues. Python 3.11 recommended."
fi

echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip install numpy pandas scipy yfinance plotly streamlit

echo ""

# Optional: Install Jupyter for notebooks
read -p "Install Jupyter for notebooks? (y/n) " jupyter
if [ "$jupyter" = "y" ] || [ "$jupyter" = "Y" ]; then
    echo "Installing Jupyter, matplotlib, seaborn..."
    pip install jupyter matplotlib seaborn
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""

# Test imports
echo "Testing installation..."
if python3 -c "import numpy, pandas, scipy, yfinance, plotly, streamlit" 2>/dev/null; then
    echo "All dependencies working!"
else
    echo "WARNING: Some packages failed to import"
fi

echo ""
echo "Next steps:"
echo "1. cd dashboard"
echo "2. streamlit run app.py"
echo ""
echo "For notebooks:"
echo "1. cd notebooks"
echo "2. jupyter notebook"
echo ""
