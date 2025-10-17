#!/bin/bash

# Start the Prompt.ly frontend server
echo "Starting Prompt.ly frontend server..."

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start the React development server
echo "Starting React development server on http://localhost:3000"
cd frontend
DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
