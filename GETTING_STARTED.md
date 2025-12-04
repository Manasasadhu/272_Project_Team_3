# Getting Started - Development Setup

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose 2.0+**
- **Python 3.9+**
- **Java 17+**
- **Node.js 18+**
- **Google Gemini API key** - [Get it here](https://ai.google.dev/)

## Quick Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3
```

### 2. Set Environment Variables

Create `.env` file in `/agentic` directory:

```bash
# Agentic Service Configuration
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_HOST=redis
REDIS_PORT=6379
CHROMA_HOST=chromadb
CHROMA_PORT=8000
JAVA_TOOLS_URL=http://localhost:5000
```

Also set in terminal:

```bash
export GEMINI_API_KEY=your_key_here
export JAVA_TOOLS_URL=http://localhost:5000
```

### 3. Start All Services

```bash
# Start agentic stack
docker-compose -f agentic/docker-compose.yml up -d

# In separate terminal, start backend
docker-compose -f backend/docker-compose.yml up -d

# In another terminal, start frontend
cd Frontend
npm install
npm run dev
```

Or use the all-in-one:

```bash
docker-compose -f docker-compose.local.yml up -d
```

### 4. Access Services

Once services are running, access them at:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web application |
| **Backend API** | http://localhost:8080 | API gateway |
| **Agentic Service** | http://localhost:8000 | AI orchestration |
| **Tools Service** | http://localhost:5000 | Paper search & PDF extraction |
| **Redis** | localhost:6379 | State management |
| **ChromaDB** | http://localhost:8001 | Vector database |
| **Prometheus** | http://localhost:9090 | Metrics collection |
| **Grafana** | http://localhost:3000 | Monitoring dashboard |

## Testing Services

Verify all services are healthy:

```bash
# Frontend
curl http://localhost:3000

# Backend API
curl http://localhost:8080/api/agent/health

# Agentic Service
curl http://localhost:8000/health

# Tools Service
curl http://localhost:5000/api/tools/health

# Grafana
curl http://localhost:3000
```

## Development Workflow

### Making Code Changes

#### **Frontend (React)**
```bash
cd Frontend
npm install
npm run dev     # Start dev server with hot reload
npm run build   # Production build
npm run test    # Run tests
```

#### **Backend (Spring Boot)**
```bash
cd backend
./mvnw clean install
./mvnw spring-boot:run
./mvnw test     # Run tests
```

#### **Agentic Service (Python)**
```bash
cd agentic
pip install -r requirements.txt
python src/main.py
pytest tests/   # Run tests
```

#### **Tools Service (Java)**
```bash
cd backend/tools-service
./mvnw clean install
./mvnw spring-boot:run
```

### Viewing Logs

```bash
# All services
docker-compose -f docker-compose.local.yml logs -f

# Specific service
docker logs app_frontend_local -f
docker logs app_backend_local -f
docker logs app_agentic -f

# Stream and filter
docker-compose -f docker-compose.local.yml logs -f | grep "ERROR"
```

## Database & Storage

### Redis

```bash
# Connect to Redis
redis-cli -h localhost -p 6379

# Basic commands
KEYS *              # List all keys
GET job_id_123      # Get job status
FLUSHDB             # Clear database (be careful!)
```

### ChromaDB

```bash
# ChromaDB API is at http://localhost:8001
# View collections
curl http://localhost:8001/api/v1/collections

# Check heartbeat
curl http://localhost:8001/api/v1/heartbeat
```

## Monitoring

### Prometheus

Access at: http://localhost:9090

Metrics include:
- Request latency
- Error rates
- Paper discovery metrics
- PDF extraction success rate

### Grafana

Access at: http://localhost:3000
- **Username**: admin
- **Password**: admin

Pre-configured dashboards show:
- System health
- Request throughput
- Service dependencies
- Resource utilization

## Common Development Tasks

### Running Tests

```bash
# All tests
docker-compose -f docker-compose.local.yml exec agentic pytest tests/

# Specific test file
docker-compose -f docker-compose.local.yml exec agentic pytest tests/test_planner.py

# With coverage
docker-compose -f docker-compose.local.yml exec agentic pytest tests/ --cov=src
```

### Static Code Analysis

```bash
# Python - using SonarQube
sonar-scanner

# Java
./mvnw sonar:sonar

# JavaScript
npm run lint
```

### Database Migrations

```bash
# Check schema
docker exec app_backend_local mysql -u root -ppassword -e "SHOW TABLES;"

# View migrations
ls backend/src/main/resources/db/migration/
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
docker-compose -f docker-compose.local.yml -e FRONTEND_PORT=3001 up -d
```

### Docker Permission Denied

```bash
# Add current user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Log out and back in
```

### Service Won't Start

```bash
# Check logs
docker logs <container_id>

# Rebuild images
docker-compose -f docker-compose.local.yml build --no-cache

# Remove and restart
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml up -d
```

### API Connection Issues

```bash
# Check if services are running
docker ps

# Check service logs
docker logs app_backend_local

# Verify network connectivity
docker network ls
docker network inspect 272_project_team_3_default
```

## Production Deployment

For EC2 deployment, see: [EC2_APP_DEPLOYMENT.md](EC2_APP_DEPLOYMENT.md)

Key files:
- `docker-compose.prod.yml` - Production configuration
- `scripts/deploy-ec2.sh` - EC2 deployment script
- `nginx-gateway.conf` - NGINX configuration

## Next Steps

1. **Submit a Research Goal** - Test the system with: "Machine learning for network security"
2. **Monitor Execution** - Watch Grafana dashboards during processing
3. **Review Results** - Check the generated synthesis report
4. **Explore Code** - Examine agent implementations in `agentic/src/agent/`
5. **Run Tests** - Execute full test suite to verify setup

## Additional Resources

- **API Documentation**: `openapi-spec.yaml`
- **System Architecture**: `README.md` (Architecture section)
- **Troubleshooting Guide**: `TROUBLESHOOTING.md`
- **Contributing Guidelines**: `CONTRIBUTING.md`
