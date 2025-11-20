#!/bin/bash
# Deploy updates to EC2 by rebuilding from source

set -e

echo "🚀 Deploying updates..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_DIR"

echo "[1/4] Pulling latest code from GitHub..."
git pull origin feat/end-to-end-testing

echo "[2/4] Rebuilding Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "[3/4] Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

echo "[4/4] Starting updated containers..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "Waiting for services to start..."
sleep 10

echo ""
echo "📦 Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "Testing health endpoints..."
curl -f http://localhost:8080/api/agent/health && echo "✅ Backend healthy" || echo "❌ Backend failed"
curl -f http://localhost:5000/api/tools/health && echo "✅ Tools healthy" || echo "❌ Tools failed"

echo ""
echo "✅ Deployment completed successfully!"
