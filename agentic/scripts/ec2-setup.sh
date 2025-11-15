#!/bin/bash
# Agentic Research Server - EC2 Setup Script
# For Ubuntu 22.04 LTS on AWS Free Tier (t2.micro)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Agentic Research Server Setup${NC}"
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

echo -e "${GREEN}[1/8] Updating system packages...${NC}"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

echo -e "${GREEN}[2/8] Installing dependencies...${NC}"
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    git \
    htop \
    vim

echo -e "${GREEN}[3/8] Installing Docker...${NC}"
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

echo -e "${GREEN}[4/8] Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose installed${NC}"
else
    echo -e "${YELLOW}✓ Docker Compose already installed${NC}"
fi

echo -e "${GREEN}[5/8] Configuring Docker permissions...${NC}"
sudo usermod -aG docker $USER

echo -e "${GREEN}[6/8] Setting up swap (important for t2.micro)...${NC}"
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo -e "${GREEN}✓ 2GB swap configured${NC}"
else
    echo -e "${YELLOW}✓ Swap already configured${NC}"
fi

echo -e "${GREEN}[7/8] Setting up environment file...${NC}"
cd "$PROJECT_DIR"

if [ ! -f .env ]; then
    cat > .env <<EOF
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyC-_WIfYRW_oKoD50WWBz_H0gXolU82db4

# LLM Model
LLM_MODEL=models/gemini-2.5-flash

# Instana (Optional - set to false for free tier)
INSTANA_ENABLED=false
INSTANA_AGENT_KEY=your_instana_key_if_you_have_one
INSTANA_SERVICE_NAME=agentic-research-service

# These defaults are fine:
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
CHROMA_HOST=chromadb
CHROMA_PORT=8000
MAX_ITERATIONS=50
CONTEXT_WINDOW_SIZE=8000
EOF
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo ""
    echo -e "${YELLOW}================================================${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env with your API key!${NC}"
    echo -e "${YELLOW}================================================${NC}"
    echo ""
    echo -e "Run: ${BLUE}nano $PROJECT_DIR/.env${NC}"
    echo ""
    echo "Replace 'your_gemini_api_key_here' with your actual Gemini API key"
    echo ""
    read -p "Press ENTER after you've updated the .env file with your API key..."
else
    echo -e "${YELLOW}✓ .env file already exists${NC}"
fi

echo -e "${GREEN}[8/8] Starting services...${NC}"
echo "Using docker-compose.free-tier.yml (optimized for t2.micro)..."

# Use sudo for first run (docker group not active yet in this session)
sudo docker compose -f docker-compose.free-tier.yml up -d

echo ""
echo "Waiting for services to start..."
sleep 10

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
echo -e "${BLUE}🌐 Your server is accessible at:${NC}"
echo "   Health: http://$PUBLIC_IP/health"
echo "   API Docs: http://$PUBLIC_IP/docs"
echo "   API: http://$PUBLIC_IP/api/"
echo ""

echo -e "${YELLOW}📝 Important Notes:${NC}"
echo "1. Log out and log back in for Docker permissions to work properly"
echo "   Then you can use docker commands without sudo"
echo ""
echo "2. Test your API:"
echo "   curl http://localhost/health"
echo ""
echo "3. View logs:"
echo "   docker logs -f agentic_server"
echo ""
echo "4. Restart services:"
echo "   cd $PROJECT_DIR"
echo "   docker-compose -f docker-compose.free-tier.yml restart"
echo ""
echo "5. Stop services:"
echo "   docker-compose -f docker-compose.free-tier.yml down"
echo ""
echo "6. Update code and restart:"
echo "   git pull"
echo "   docker-compose -f docker-compose.free-tier.yml up -d --build"
echo ""
echo -e "${GREEN}✓ Ready for your presentation! 🎓${NC}"
echo ""