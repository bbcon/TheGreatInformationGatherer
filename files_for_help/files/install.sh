#!/bin/bash
# Bloomberg Markets Summarizer - Installation Script

set -e

echo "=========================================="
echo "Bloomberg Markets Summarizer - Installer"
echo "=========================================="
echo

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if ffmpeg is installed
echo
echo "Checking for ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found"
    echo "Installing ffmpeg..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "Please install ffmpeg manually for your system"
        exit 1
    fi
else
    echo "✓ ffmpeg found"
fi

# Install Python dependencies
echo
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo
    echo "⚠️  IMPORTANT: Edit .env file with your API keys before running!"
    echo "   nano .env"
fi

# Create directories
echo
echo "Creating directories..."
mkdir -p logs output/summaries output/transcripts temp

# Make scripts executable
echo "Setting permissions..."
chmod +x main.py setup_cron.py test_setup.py

echo
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "  1. Edit .env with your API keys:"
echo "     nano .env"
echo
echo "  2. Test your setup:"
echo "     python3 test_setup.py"
echo
echo "  3. Run your first summary:"
echo "     python3 main.py"
echo
echo "  4. Setup daily automation:"
echo "     python3 setup_cron.py"
echo
echo "For help, see README.md or QUICKSTART.md"
echo "=========================================="
