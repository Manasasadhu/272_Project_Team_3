#!/bin/bash

# Exit on any error
set -e

echo "🚀 Deploying to EC2..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Get latest version
VERSION=$(git rev-parse --short HEAD)
export VERSION

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Pull latest images
echo "Pulling latest images..."
docker pull $ECR_REGISTRY/lit_review_agent_app:frontend-latest
docker pull $ECR_REGISTRY/lit_review_agent_app:backend-latest
docker pull $ECR_REGISTRY/lit_review_agent_app:tools-latest

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Start new containers
echo "Starting new containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for health checks
echo "Waiting for services to be healthy..."
sleep 10

# Check container status
echo "Container status:"
docker-compose -f docker-compose.prod.yml ps

# Test health endpoints
echo "Testing health endpoints..."
curl -f http://localhost/health && echo "✅ Nginx healthy" || echo "❌ Nginx failed"
curl -f http://localhost/api/actuator/health && echo "✅ Backend healthy" || echo "❌ Backend failed"

echo "✅ Deployment completed successfully!"
echo "Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "Backend API: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/api"
