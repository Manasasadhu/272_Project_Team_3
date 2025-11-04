#!/bin/bash

# Exit on any error
set -e

echo "Starting automated setup..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    git

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker << END

# Clone repository
echo "Cloning repository..."
cd ~
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3/agentic

# Setup environment file
echo "Setting up environment file..."
cp .env.example .env
echo "Please edit .env file with your configuration"
read -p "Press enter when you have updated the .env file"

# Start services
echo "Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "Setup completed successfully!"
echo "Your services should now be running. Check status with: docker-compose -f docker-compose.prod.yml ps"
END