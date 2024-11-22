#!/bin/bash

# Log file for this script
LOG_FILE="/tmp/nginx_install.log"

echo "Starting Nginx setup..." >> $LOG_FILE

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
  echo "Nginx not found. Installing Nginx..." >> $LOG_FILE
  sudo apt update >> $LOG_FILE 2>&1
  sudo apt install -y nginx >> $LOG_FILE 2>&1
else
  echo "Nginx is already installed." >> $LOG_FILE
fi

# Replace Nginx default configuration
echo "Copying new Nginx configuration..." >> $LOG_FILE
sudo cp /home/ubuntu/PythonFlask/nginx/default /etc/nginx/sites-available/default

# Restart Nginx to apply changes
echo "Restarting Nginx..." >> $LOG_FILE
sudo systemctl restart nginx

# Enable Nginx to start on boot
echo "Enabling Nginx to start on boot..." >> $LOG_FILE
sudo systemctl enable nginx

echo "Nginx setup completed successfully." >> $LOG_FILE
