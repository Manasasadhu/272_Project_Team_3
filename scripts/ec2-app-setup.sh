#!/bin/bash
# Literature Review Application - EC2 Setup Script
# For Ubuntu 22.04 LTS on AWS EC2 (t3.medium recommended)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Lit Review App - EC2 Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}❌ Please do not run as root. Run as ubuntu user.${NC}"
   exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${GREEN}[1/9] Updating system packages...${NC}"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

echo -e "${GREEN}[2/9] Installing dependencies...${NC}"
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    git \
    htop \
    vim \
    unzip

echo -e "${GREEN}[3/9] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    sudo systemctl start docker
    sudo systemctl enable docker
    echo -e "${GREEN}✓ Docker installed${NC}"
else
    echo -e "${YELLOW}✓ Docker already installed${NC}"
fi

echo -e "${GREEN}[4/9] Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed${NC}"
else
    echo -e "${YELLOW}✓ Docker Compose already installed${NC}"
fi

echo -e "${GREEN}[5/9] Configuring Docker permissions...${NC}"
sudo usermod -aG docker $USER

echo -e "${GREEN}[6/9] Setting up environment file...${NC}"
cd "$PROJECT_DIR"

if [ ! -f .env ]; then
    # Prompt for agentic service URL
    echo ""
    echo -e "${YELLOW}================================================${NC}"
    echo -e "${YELLOW}⚠️  AGENTIC SERVICE CONFIGURATION${NC}"
    echo -e "${YELLOW}================================================${NC}"
    echo ""
    read -p "Enter your Agentic Service URL (e.g., http://3.145.123.45:80): " AGENTIC_URL
    
    cat > .env <<EOF
# IMPORTANT: Agentic service URL
# If agentic is on another EC2, use its private IP (if in same VPC) or public IP
AGENTIC_SERVICE_URL=${AGENTIC_URL}

# Service Ports (default, no need to change)
BACKEND_PORT=8080
FRONTEND_PORT=3000
TOOLS_PORT=5000
EOF
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${YELLOW}✓ .env file already exists${NC}"
fi

echo -e "${GREEN}[7/9] Building Docker images from source...${NC}"
echo "This may take several minutes..."

# Build images directly on EC2
# Use sudo for first build since docker group isn't active yet
sudo docker-compose -f docker-compose.prod.yml build

echo -e "${GREEN}[8/9] Pulling additional images (Redis, GROBID)...${NC}"
sudo docker pull redis:7-alpine
sudo docker pull lfoppiano/grobid:0.8.0

echo ""
echo -e "${GREEN}[9/9] Starting services...${NC}"
sudo docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "Waiting for services to start..."
sleep 15

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check status
echo "📦 Container Status:"
sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo -e "${BLUE}🌐 Your application is accessible at:${NC}"
echo "   Frontend: http://$PUBLIC_IP:3000"
echo "   Backend API: http://$PUBLIC_IP:8080/api"
echo "   Backend Health: http://$PUBLIC_IP:8080/api/agent/health"
echo "   Tools Service: http://$PUBLIC_IP:5000/api/tools/health"
echo ""

echo -e "${YELLOW}📝 Important Notes:${NC}"
echo "1. Log out and log back in for Docker permissions to take effect"
echo "   Then you can use docker commands without sudo"
echo ""
echo "2. Test your services:"
echo "   curl http://localhost:8080/api/agent/health"
echo "   curl http://localhost:5000/api/tools/health"
echo "   curl http://localhost:3000"
echo ""
echo "3. View logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo "   docker logs -f app_backend"
echo "   docker logs -f app_tools_service"
echo ""
echo "4. Restart services:"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "5. Stop services:"
echo "   docker-compose -f docker-compose.prod.yml down"
echo ""
echo "6. Update from ECR and restart:"
echo "   ./scripts/deploy-ec2.sh"
echo ""
echo -e "${YELLOW}🔒 Security Group Requirements:${NC}"
echo "   - Port 22 (SSH): Your IP only"
echo "   - Port 3000 (Frontend): 0.0.0.0/0"
echo "   - Port 8080 (Backend): 0.0.0.0/0"
echo "   - Port 5000 (Tools): Internal only (or your IP for testing)"
echo ""
echo -e "${GREEN}✓ Ready for deployment! 🚀${NC}"
echo ""
