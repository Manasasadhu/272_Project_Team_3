#!/bin/bash

# Exit on any error
set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found. Copy .env.prod to .env and configure it."
    exit 1
fi

# Get git commit hash for versioning
VERSION=$(git rev-parse --short HEAD)
echo "Building version: $VERSION"

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build and push Frontend
echo "Building Frontend..."
docker build -t $ECR_REGISTRY/lit_review_agent_app:frontend-$VERSION ./Frontend
docker tag $ECR_REGISTRY/lit_review_agent_app:frontend-$VERSION $ECR_REGISTRY/lit_review_agent_app:frontend-latest
echo "Pushing Frontend to ECR..."
docker push $ECR_REGISTRY/lit_review_agent_app:frontend-$VERSION
docker push $ECR_REGISTRY/lit_review_agent_app:frontend-latest

# Build and push Backend
echo "Building Backend..."
docker build -t $ECR_REGISTRY/lit_review_agent_app:backend-$VERSION ./backend
docker tag $ECR_REGISTRY/lit_review_agent_app:backend-$VERSION $ECR_REGISTRY/lit_review_agent_app:backend-latest
echo "Pushing Backend to ECR..."
docker push $ECR_REGISTRY/lit_review_agent_app:backend-$VERSION
docker push $ECR_REGISTRY/lit_review_agent_app:backend-latest

# Build and push Tools Service
echo "Building Tools Service..."
docker build -t $ECR_REGISTRY/lit_review_agent_app:tools-$VERSION ./backend/tools-service
docker tag $ECR_REGISTRY/lit_review_agent_app:tools-$VERSION $ECR_REGISTRY/lit_review_agent_app:tools-latest
echo "Pushing Tools Service to ECR..."
docker push $ECR_REGISTRY/lit_review_agent_app:tools-$VERSION
docker push $ECR_REGISTRY/lit_review_agent_app:tools-latest

echo "✅ All images built and pushed successfully!"
echo "Frontend: $ECR_REGISTRY/lit_review_agent_app:frontend-$VERSION"
echo "Backend: $ECR_REGISTRY/lit_review_agent_app:backend-$VERSION"
echo "Tools: $ECR_REGISTRY/lit_review_agent_app:tools-$VERSION"
