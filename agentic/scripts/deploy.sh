#!/bin/bash

# Exit on any error
set -e

echo "Updating application..."

# Configure git to handle file permission changes
git config core.fileMode false

# Reset any local changes that might interfere with pull
git reset --hard HEAD

# Pull latest changes
echo "Getting latest code..."
git pull

# Ensure scripts are executable
chmod +x scripts/*.sh

# Rebuild and restart containers
echo "Rebuilding and restarting services..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "Update completed successfully!"
echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"
