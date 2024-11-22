#!/bin/bash

echo "Running MongoDB installation script..." >> /tmp/mongodb_install.log

# Import the public key for the MongoDB repository
echo "Importing MongoDB public key..." >> /tmp/mongodb_install.log
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg >> /tmp/mongodb_install.log 2>&1

# Add MongoDB repository to sources list
echo "Adding MongoDB repository to sources list..." >> /tmp/mongodb_install.log
echo "deb [signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list >> /tmp/mongodb_install.log 2>&1

# Update package database
echo "Updating package database..." >> /tmp/mongodb_install.log
sudo apt update >> /tmp/mongodb_install.log 2>&1

# Install MongoDB
echo "Installing MongoDB..." >> /tmp/mongodb_install.log
sudo apt install -y mongodb-org >> /tmp/mongodb_install.log 2>&1

# Start MongoDB service
echo "Starting MongoDB service..." >> /tmp/mongodb_install.log
sudo systemctl start mongod >> /tmp/mongodb_install.log 2>&1

# Enable MongoDB service to start on boot
echo "Enabling MongoDB service to start on boot..." >> /tmp/mongodb_install.log
sudo systemctl enable mongod >> /tmp/mongodb_install.log 2>&1

# Verify MongoDB status
echo "Verifying MongoDB service status..." >> /tmp/mongodb_install.log
if sudo systemctl is-active --quiet mongod; then
  echo "MongoDB is running successfully." >> /tmp/mongodb_install.log
else
  echo "MongoDB failed to start!" >> /tmp/mongodb_install.log
  sudo systemctl status mongod >> /tmp/mongodb_install.log
  exit 1
fi

echo "MongoDB installation script completed successfully." >> /tmp/mongodb_install.log
