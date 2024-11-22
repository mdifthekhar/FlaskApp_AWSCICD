#!/bin/bash

echo "Starting the Flask application..."

# Navigate to the project directory
cd /home/ubuntu/PythonFlask || exit

# Activate the virtual environment
source venv/bin/activate

# Start the Flask application
nohup python3 main.py > app.log 2>&1 &
echo "Application started."
