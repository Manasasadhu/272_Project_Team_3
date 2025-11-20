#!/bin/bash

# Exit on any error
set -e

echo "🧪 Testing local build..."

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose -f docker-compose.local.yml down 2>/dev/null || true

# Build all images
echo "Building images (this may take a few minutes)..."
docker-compose -f docker-compose.local.yml build --no-cache

# Start containers
echo "Starting containers..."
docker-compose -f docker-compose.local.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 15

# Check container status
echo ""
echo "=== Container Status ==="
docker-compose -f docker-compose.local.yml ps

# Test health endpoints
echo ""
echo "=== Testing Health Endpoints ==="

# Test nginx
if curl -f -s http://localhost/health > /dev/null; then
    echo "✅ Nginx: healthy"
else
    echo "❌ Nginx: failed"
fi

# Test backend
if curl -f -s http://localhost/api/actuator/health > /dev/null; then
    echo "✅ Backend: healthy"
else
    echo "❌ Backend: failed"
fi

# Test frontend
if curl -f -s http://localhost/ > /dev/null; then
    echo "✅ Frontend: healthy"
else
    echo "❌ Frontend: failed"
fi

echo ""
echo "=== View Logs ==="
echo "Frontend:      docker logs app_frontend_local"
echo "Backend:       docker logs app_backend_local"
echo "Tools-service: docker logs app_tools_service_local"
echo "Nginx:         docker logs app_nginx_local"
echo ""
echo "=== Test Complete! ==="
echo "Access the app at: http://localhost"
echo ""
echo "To stop: docker-compose -f docker-compose.local.yml down"
