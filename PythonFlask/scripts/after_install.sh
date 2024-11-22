#!/bin/bash

echo "Running AfterInstall hook..."

# Move the flaskec.service file to /etc/systemd/system/
if [ -f "/home/ubuntu/PythonFlask/systemd/flaskec.service" ]; then
  echo "Copying flaskec.service to /etc/systemd/system/" >> /tmp/codedeploy.log
  cp /home/ubuntu/PythonFlask/systemd/flaskec.service /etc/systemd/system/flaskec.service
else
  echo "flaskec.service not found in /home/ubuntu/PythonFlask/systemd!" >> /tmp/codedeploy.log
  exit 1
fi

# Reload systemd daemon to recognize the new service
echo "Reloading systemd daemon..." >> /tmp/codedeploy.log
systemctl daemon-reload

# Enable the Flask service to start on boot
echo "Enabling flaskec.service..." >> /tmp/codedeploy.log
systemctl enable flaskec.service

# Start the Flask service
echo "Starting flaskec.service..." >> /tmp/codedeploy.log
systemctl start flaskec.service

# Replace the default Nginx configuration file with the custom one
if [ -f "/home/ubuntu/PythonFlask/nginx/default" ]; then
  echo "Copying Nginx default config to /etc/nginx/sites-available/default" >> /tmp/deploy.log
  sudo cp /home/ubuntu/PythonFlask/nginx/default /etc/nginx/sites-available/default
else
  echo "Nginx default config not found!" >> /tmp/codedeploy.log
  exit 1
fi

# Reload Nginx to apply changes
echo "Reloading Nginx..." >> /tmp/codedeploy.log
sudo systemctl reload nginx

echo "AfterInstall hook completed." >> /tmp/codedeploy.log
