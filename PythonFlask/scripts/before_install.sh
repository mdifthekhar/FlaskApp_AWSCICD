#!/bin/bash

echo "Running BeforeInstall hook..."

# Ensure the destination directory exists (CodeDeploy should handle this, but a safeguard doesn't hurt)
if [ ! -d "/home/ubuntu/PythonFlask" ]; then
  echo "/home/ubuntu/PythonFlask directory does not exist! Exiting..." >> /tmp/codedeploy.log
  exit 1
fi

# Navigate to the application directory
cd /home/ubuntu/PythonFlask

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed! Installing..." >> /tmp/codedeploy.log
  sudo apt-get update -y
  sudo apt-get install -y python3
fi

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
  echo "python3-venv is not installed! Installing..." >> /tmp/codedeploy.log
  sudo apt-get install -y python3-venv
fi

# Create a virtual environment if it doesn't already exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..." >> /tmp/codedeploy.log
  sudo python3 -m venv venv
else
  echo "Virtual environment already exists." >> /tmp/codedeploy.log
fi

# Activate the virtual environment
echo "Activating virtual environment..." >> /tmp/codedeploy.log
source /home/ubuntu/PythonFlask/venv/bin/activate

# Install dependencies from requirements.txt if available
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..." >> /tmp/codedeploy.log
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Skipping dependency installation." >> /tmp/codedeploy.log
fi

# Install MongoDB
echo "Installing MongoDB..." >> /tmp/codedeploy.log
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB and enable it to start on boot
echo "Starting MongoDB..." >> /tmp/codedeploy.log
sudo systemctl start mongod
sudo systemctl enable mongod

# Install Nginx
echo "Installing Nginx..." >> /tmp/codedeploy.log
sudo apt-get install -y nginx

# Start Nginx and enable it to start on boot
echo "Starting Nginx..." >> /tmp/codedeploy.log
sudo systemctl start nginx
sudo systemctl enable nginx


echo "BeforeInstall hook completed." >> /tmp/codedeploy.log
