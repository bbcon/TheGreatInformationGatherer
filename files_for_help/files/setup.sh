#!/bin/bash
# Newsletter Summarizer - Quick Setup

set -e

echo "=========================================="
echo "Newsletter Summarizer - Setup"
echo "=========================================="
echo

# Create directories
mkdir -p output/summaries logs

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo
    echo "⚠️  IMPORTANT: Edit .env file with your settings!"
    echo "   1. Get Gmail App Password: https://myaccount.google.com/apppasswords"
    echo "   2. Get Anthropic API Key: https://console.anthropic.com"
    echo "   3. Edit .env: nano .env"
fi

# Make script executable
chmod +x main.py

echo
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "  1. Get Gmail App Password:"
echo "     https://myaccount.google.com/apppasswords"
echo
echo "  2. Get Anthropic API Key:"
echo "     https://console.anthropic.com"
echo
echo "  3. Edit .env with your settings:"
echo "     nano .env"
echo
echo "  4. Test it:"
echo "     python3 main.py"
echo
echo "  5. Automate (optional):"
echo "     crontab -e"
echo "     0 8 * * * cd $(pwd) && python3 main.py"
echo
echo "=========================================="
