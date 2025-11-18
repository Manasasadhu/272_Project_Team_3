# EC2 Application Deployment Guide

## Architecture Overview

### Single EC2 Instance Running:
```
┌─────────────────────────────────────────┐
│          EC2 Instance (Port 80)          │
├─────────────────────────────────────────┤
│  Nginx Gateway (Reverse Proxy)          │
│    ├─→ /          → Frontend            │
│    └─→ /api/*     → Backend             │
├─────────────────────────────────────────┤
│  Containers:                             │
│  ├─ Frontend (React + Nginx)            │
│  ├─ Backend (Spring Boot)               │
│  └─ Tools-service (Spring Boot)         │
└─────────────────────────────────────────┘
```

### Separate Agentic EC2:
- Agentic service on port 80
- Backend communicates with it via HTTP

---

## Prerequisites

### 1. AWS Setup
- AWS CLI installed and configured
- ECR repository: `616860869098.dkr.ecr.us-east-2.amazonaws.com/lit_review_agent_app`
- EC2 instance with:
  - Docker and Docker Compose installed
  - Security group allowing ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
  - IAM role with ECR pull permissions

### 2. Local Setup
```bash
# Clone repository
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3

# Checkout the deployment branch
git checkout feat/end-to-end-testing

# Copy environment template
cp .env.prod .env

# Edit .env with your values
nano .env
```

### 3. Configure Environment
Update `.env` file:
```bash
ECR_REGISTRY=616860869098.dkr.ecr.us-east-2.amazonaws.com
VERSION=latest
AGENTIC_SERVICE_URL=http://your-agentic-ec2-ip:80
AWS_REGION=us-east-2
AWS_ACCOUNT_ID=616860869098
```

---

## Deployment Process

### Option 1: Build Locally & Push to ECR

```bash
# 1. Make scripts executable
chmod +x scripts/*.sh

# 2. Build and push all images
./scripts/build-and-push.sh
```

This will:
- Build Frontend, Backend, and Tools-service images
- Tag with git commit hash + `latest`
- Push to ECR repository
- Always pulls latest code from `feat/end-to-end-testing` branch

### Option 2: Build on EC2 Directly

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# Clone/update repository
cd ~
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3
git checkout feat/end-to-end-testing
git pull

# Build and deploy
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## EC2 Deployment

### First Time Setup

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# Install Docker & Docker Compose (if not already)
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install AWS CLI
sudo yum install -y aws-cli

# Configure AWS CLI (use IAM role or credentials)
aws configure

# Clone repository
cd ~
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3
git checkout feat/end-to-end-testing

# Create .env file
cp .env.prod .env
nano .env  # Update with your values

# Make deploy script executable
chmod +x scripts/deploy-ec2.sh
```

### Deploy/Update Application

```bash
# Run deployment script
./scripts/deploy-ec2.sh
```

Or manually:
```bash
# Pull latest code
git pull origin feat/end-to-end-testing

# Login to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 616860869098.dkr.ecr.us-east-2.amazonaws.com

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Restart services
docker-compose -f docker-compose.prod.yml up -d
```

---

## Verification

### 1. Check Container Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

Expected output:
```
NAME                  STATUS        PORTS
app_nginx            Up (healthy)   80/tcp, 443/tcp
app_frontend         Up (healthy)   80/tcp
app_backend          Up (healthy)   8080/tcp
app_tools_service    Up (healthy)   5000/tcp
```

### 2. Check Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker logs app_backend
docker logs app_frontend
docker logs app_tools_service
docker logs app_nginx
```

### 3. Test Endpoints

```bash
# Get EC2 public IP
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Test health
curl http://$EC2_IP/health

# Test backend
curl http://$EC2_IP/api/actuator/health

# Test frontend (should return HTML)
curl http://$EC2_IP/

# Test full flow
curl -X POST http://$EC2_IP/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "researchGoal": "test deployment",
    "scopeParameters": {}
  }'
```

### 4. Access in Browser
- Frontend: `http://your-ec2-ip/`
- Backend API: `http://your-ec2-ip/api/`
- Health: `http://your-ec2-ip/health`

---

## Security Group Configuration

### Inbound Rules
| Type  | Protocol | Port | Source      | Description          |
|-------|----------|------|-------------|----------------------|
| HTTP  | TCP      | 80   | 0.0.0.0/0   | Web traffic          |
| HTTPS | TCP      | 443  | 0.0.0.0/0   | Secure web (optional)|
| SSH   | TCP      | 22   | Your IP     | SSH access           |

### Outbound Rules
- All traffic: 0.0.0.0/0 (default)

---

## Updating the Application

### Quick Update (Latest Images)
```bash
# On EC2
cd ~/272_Project_Team_3
./scripts/deploy-ec2.sh
```

### Build New Version
```bash
# Locally
git pull origin feat/end-to-end-testing
./scripts/build-and-push.sh

# On EC2
./scripts/deploy-ec2.sh
```

---

## Rollback

### Rollback to Previous Version
```bash
# On EC2
cd ~/272_Project_Team_3

# View available versions
docker images | grep lit_review_agent_app

# Update .env with specific version
export VERSION=abc123  # Use git commit hash

# Deploy specific version
docker-compose -f docker-compose.prod.yml up -d
```

---

## Monitoring

### View Container Stats
```bash
docker stats
```

### View Disk Usage
```bash
docker system df
```

### Clean Up Old Images
```bash
docker system prune -a
```

---

## Troubleshooting

### Frontend Not Loading
```bash
# Check frontend logs
docker logs app_frontend

# Check nginx gateway logs
docker logs app_nginx

# Verify nginx config
docker exec app_nginx nginx -t
```

### Backend 500 Errors
```bash
# Check backend logs
docker logs app_backend

# Check if tools-service is running
docker logs app_tools_service

# Verify agentic service URL
echo $AGENTIC_SERVICE_URL
curl $AGENTIC_SERVICE_URL/health
```

### Containers Not Starting
```bash
# Check for port conflicts
sudo lsof -i :80
sudo lsof -i :443

# Check Docker daemon
sudo service docker status

# Restart Docker
sudo service docker restart
```

### ECR Pull Errors
```bash
# Re-login to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 616860869098.dkr.ecr.us-east-2.amazonaws.com

# Check IAM permissions
aws ecr describe-repositories
```

---

## Cost Optimization

### Recommended EC2 Instance Types
- **Development**: t3.medium (2 vCPU, 4 GB RAM) - ~$30/month
- **Production**: t3.large (2 vCPU, 8 GB RAM) - ~$60/month
- **High Traffic**: m5.large (2 vCPU, 8 GB RAM) - ~$70/month

### Resource Usage
- Frontend: ~50 MB RAM
- Backend: ~512 MB RAM
- Tools-service: ~512 MB RAM
- Nginx: ~10 MB RAM
- **Total**: ~1 GB RAM + overhead

---

## SSL/HTTPS Setup (Optional)

### Using Let's Encrypt

1. Install Certbot:
```bash
sudo yum install -y certbot python3-certbot-nginx
```

2. Get Certificate:
```bash
sudo certbot --nginx -d yourdomain.com
```

3. Update `nginx-gateway.conf` with SSL config

4. Restart nginx:
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

---

## CI/CD Integration (Future)

### GitHub Actions Example
```yaml
name: Deploy to EC2

on:
  push:
    branches: [feat/end-to-end-testing]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and Push
        run: ./scripts/build-and-push.sh
      - name: Deploy to EC2
        run: |
          ssh ec2-user@$EC2_IP 'cd ~/272_Project_Team_3 && ./scripts/deploy-ec2.sh'
```

---

## Support

For issues or questions:
1. Check logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify health: `curl http://localhost/health`
3. Review this guide's troubleshooting section
