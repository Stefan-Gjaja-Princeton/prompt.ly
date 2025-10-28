#!/bin/bash

# Start the Prompt.ly backend server
echo "Starting Prompt.ly backend server..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "Activating virtual environment..."
source backend/venv/bin/activate

set -a
[ -f backend/.env ] && source backend/.env
set +a

# Install dependencies
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY environment variable is not set!"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Or create a .env file in the backend directory with:"
    echo "OPENAI_API_KEY=your-api-key-here"
    echo ""
fi

# Start the server
echo "Starting Flask server on http://localhost:5001"
python app.py
