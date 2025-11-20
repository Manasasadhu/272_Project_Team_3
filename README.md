# 🤖 Goal-Oriented Research Synthesis Agent

**Autonomous Academic Research Discovery & Synthesis System**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Java 17+](https://img.shields.io/badge/java-17+-orange.svg)](https://www.oracle.com/java/technologies/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://reactjs.org/)

---

## 🚀 **Live Application Access**

### 🌐 **Web Application**
**Access the live research agent:** 
```
http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/
```
👉 **[Click here to open the application](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)**

### 📊 **Monitoring Dashboard (Grafana)**
**View real-time metrics and system health:**
```
http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/agentic-research-server-metrics
```
👉 **[Click here to open Grafana monitoring](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/agentic-research-server-metrics)**

**Grafana Login:**
- Username: `admin`
- Password: `admin` (change on first login)

---

## 📋 Table of Contents

- [Live Application Access](#live-application-access)
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Starting Services](#starting-services)
- [Usage](#usage)
- [Service Details](#service-details)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Goal-Oriented Research Synthesis Agent** is an enterprise-grade autonomous system designed to revolutionize academic research discovery and synthesis. Given a research goal (e.g., "Comparison of RIP and OSPF routing protocols"), the system autonomously:

1. **Plans** - Decomposes research goals into targeted search queries
2. **Discovers** - Searches academic databases for relevant papers
3. **Validates** - Scores and filters papers based on relevance and quality
4. **Extracts** - Parses PDFs and extracts structured content
5. **Synthesizes** - Generates comprehensive 10,000+ word research reports

### Key Highlights

- 🧠 **Agentic Intelligence**: 4 specialized agents (Planner, Executor, Governance, Synthesizer)
- 🎯 **Goal-Adherent**: Every stage traces back to the original research goal
- 📊 **Dynamic Semantic Matching**: Context-aware relevance scoring (not hardcoded)
- 📈 **High Success Rate**: 96%+ extraction success, 75% paper validation rate
- 📝 **Comprehensive Reports**: 17-section analysis with actionable insights
- 🔄 **Fault Tolerant**: Checkpoint recovery and graceful degradation

### Example Results

- **Papers Discovered**: 84
- **Papers Validated**: 56 (67%)
- **PDFs Extracted**: 26 (96.3% success)
- **Final Report**: 10,000+ words, 50-55 min read
- **Quality Rating**: 9/10

---

## 🏗️ System Architecture

```
User (Browser)
         ↓
    React Frontend (Port 3000/80)
         ↓
    Backend Gateway (Spring Boot - Port 8080)
         ↓
      NGINX (Port 80)
         ↓
    ┌─────────────────────────────────────┐
    │   Agentic Service (Python - 8000)   │
    │                                     │
    │  ┌──────────────────────────────┐   │
    │  │ Agentic Intelligence Layer   │   │
    │  │  • Planner Agent             │   │
    │  │  • Executor Agent            │←→│ Redis (Port 6379)
    │  │  • Governance Engine         │←→│ ChromaDB (Port 8001)
    │  │  • Synthesizer Agent         │   │ Prometheus (9090)
    │  └──────────────────────────────┘   │ Grafana (3000)
    │         ↓                           │
    │  Tools Service (Java - Port 5000)   │
    │  • OpenAlex API Integration         │
    │  • GROBID PDF Parser (Port 8070)    │
    │                                     │
    │  DevOps: Docker, GitHub, SonarQube  │
    └─────────────────────────────────────┘
              ↓ (External)
    OpenAlex API, Gemini LLM
```

---

## ✨ Features

### 🔍 Autonomous Research Discovery
- AI-driven paper discovery without manual searching
- Adaptive query expansion to fill coverage gaps
- Searches 84+ papers per research goal

### 🎯 Goal-Driven Synthesis
- Every output directly addresses user's research goals
- 17-section comprehensive analysis
- Executive summary, solution roadmap, implementation guide

### 📊 Dynamic Semantic Matching
- Context-aware relevance scoring (not hardcoded)
- Semantic keyword groups generated at runtime
- 70% semantic + 15% citation + 10% recency + 5% metadata scoring

### 🛡️ Quality Governance
- Multi-layer validation ensures authoritative sources
- Min year filter (≥1990), citation filter (≥5), peer-review check
- Transparent scoring for every paper

### 📄 PDF Extraction
- Automated content parsing from academic PDFs
- Extracts: Abstract, key findings, methodology
- 96%+ extraction success rate using GROBID

### 🔄 Fault Tolerance
- Redis checkpoint recovery at every stage
- Resume from any point if interrupted
- Graceful degradation for partial extractions

### 📈 Real-time Monitoring
- Prometheus metrics collection
- Grafana dashboards for visualization
- Track progress through all workflow stages

### 🔒 Security & Quality
- JWT authentication for secure access
- SonarQube static code analysis
- Unit testing with Jest and PyTest

---

## 🛠️ Technology Stack

### **Frontend**
- **React 18+** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls

### **Backend Services**
- **Python 3.9+** - API Service & Agentic Layer
  - FastAPI - High-performance web framework
  - Celery - Asynchronous task queue
- **Java 17+** - Tools Service
  - Spring Boot - Enterprise Java framework
  - GROBID - PDF parsing library

### **Data Layer**
- **Redis 7.0+** - In-memory cache & state management
- **ChromaDB** - Vector database for semantic search
- **Gemini 2.5-flash** - Google LLM for synthesis

### **Infrastructure**
- **NGINX** - Reverse proxy & load balancer
- **Docker** - Containerization
- **AWS EC2** - Cloud hosting
- **Prometheus** - Metrics & monitoring
- **Grafana** - Visualization dashboards

### **DevOps & Quality**
- **GitHub** - Version control & CI/CD
- **SonarQube** - Static code analysis
- **Jest / PyTest** - Unit testing
- **JWT** - Authentication & authorization

### **External APIs**
- **OpenAlex API** - Academic paper discovery
- **Google Gemini LLM** - AI-powered synthesis

---

## 📦 Prerequisites

Before starting, ensure you have the following installed:

### Required Software
- **Docker** 20.10+ and Docker Compose 2.0+
- **Python** 3.9 or higher
- **Java JDK** 17 or higher
- **Node.js** 18+ and npm 9+
- **Redis** 7.0+
- **Git**

### Optional (for local development)
- **NGINX** (for production deployment)
- **Prometheus** & **Grafana** (for monitoring)

### API Keys Required
- **Google Gemini API Key** - For LLM synthesis ([Get it here](https://ai.google.dev/))
- **OpenAlex API** - No key required (open access)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3
```

### 2. Set Up Environment Variables

Create `.env` files in each service directory:

#### **Agentic Service** (`.env` in `/agentic`)
Copy `.env.example` to `.env` and update:
```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# LLM Configuration
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=models/gemini-2.5-flash

# ChromaDB Configuration
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# Java Tools Service URL
JAVA_TOOLS_URL=http://localhost:5000
JAVA_TOOLS_SEARCH_URL=http://localhost:5000/api/tools/search
JAVA_TOOLS_EXTRACT_URL=http://localhost:5000/api/tools/extract

# Optional: Monitoring
INSTANA_ENABLED=false
LOG_LEVEL=INFO
```

#### **Backend Service** (in `/backend/src/main/resources/application.properties`)
Already configured - update only these if needed:
```properties
server.port=8080
agentic.service.url=http://localhost:80
spring.data.redis.host=localhost
spring.data.redis.port=6379
```

#### **Frontend** (`.env.development` and `.env.production` in `/Frontend`)
```bash
# Development
VITE_API_BASE_URL=http://localhost:8080

# Production (update to your backend URL)
VITE_API_BASE_URL=http://your-backend-url:8080
```

### 3. Install Dependencies

#### **Frontend (React + Vite)**
```bash
cd Frontend
npm install
cd ..
```

#### **Agentic Service (Python + FastAPI)**
```bash
cd agentic
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

#### **Backend (Spring Boot)**
```bash
cd backend
./mvnw clean install  # On Windows: mvnw.cmd clean install
cd ..
```

#### **Tools Service (Java)**
```bash
cd backend/tools-service
../mvnw clean install  # On Windows: ..\mvnw.cmd clean install
cd ../..
```

### 4. Set Up Data Services

#### **Start Redis**
```bash
# Using Docker
docker run -d --name redis -p 6379:6379 redis:7.0-alpine

# Or using local installation
redis-server
```

#### **Start ChromaDB**
```bash
# Using Docker
docker run -d --name chromadb -p 8001:8000 chromadb/chroma:latest

# Or using Python
pip install chromadb
chroma run --host localhost --port 8001
```

#### **Start GROBID (for PDF parsing)**
```bash
# Using Docker
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.0
```

---

## ▶️ Starting Services

### Option 1: Using Docker Compose (Recommended)

#### **Full Stack (Local Development)**
Starts all services: Frontend, Backend, Agentic (via EC2), Tools Service, GROBID, Redis

```bash
# From project root
docker-compose -f docker-compose.local.yml up -d

# View logs
docker-compose -f docker-compose.local.yml logs -f

# Stop all services
docker-compose -f docker-compose.local.yml down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Tools Service: http://localhost:5000
- GROBID: http://localhost:8070
- Redis: localhost:6379

#### **Agentic Service Only (Development)**
Starts Agentic service with Redis, ChromaDB, monitoring

```bash
cd agentic
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Agentic API (via NGINX): http://localhost:80
- Agentic API (direct): http://localhost:8000
- Redis: localhost:6379
- ChromaDB: localhost:8001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Loki: http://localhost:3100

#### **Agentic Service (Production)**
With Instana monitoring enabled

```bash
cd agentic
# Set environment variables first
export GEMINI_API_KEY=your_key_here
export INSTANA_AGENT_KEY=your_instana_key

docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Manual Start (for Development)

#### **Terminal 1: Start Redis**
```bash
# Using Docker
docker run -d --name redis -p 6379:6379 redis:7-alpine

# Or using local installation
redis-server
```

#### **Terminal 2: Start ChromaDB**
```bash
# Using Docker
docker run -d --name chromadb -p 8001:8000 chromadb/chroma:0.5.20

# Or using Python (install first: pip install chromadb)
chroma run --host localhost --port 8001
```

#### **Terminal 3: Start GROBID**
```bash
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.0
```

#### **Terminal 4: Start Tools Service (Java)**
```bash
cd backend/tools-service
# Make sure GROBID_URL is set
export GROBID_URL=http://localhost:8070
../mvnw spring-boot:run
# Service will start on http://localhost:5000
```

#### **Terminal 5: Start Agentic Service (Python)**
```bash
cd agentic
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Make sure .env file is configured
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# Service will start on http://localhost:8000
```

#### **Terminal 6: Start Backend (Spring Boot)**
```bash
cd backend
# Update application.properties if needed
./mvnw spring-boot:run
# Service will start on http://localhost:8080
```

#### **Terminal 7: Start Frontend (React + Vite)**
```bash
cd Frontend
# Make sure .env.development is configured
npm run dev
# Application will open on http://localhost:3000
```

#### **Optional: Start Monitoring**
```bash
# Prometheus
cd agentic
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Grafana
docker run -d --name grafana -p 3001:3000 grafana/grafana
# Note: Changed to 3001 to avoid conflict with Frontend on 3000
```

### Verify All Services Are Running

```bash
# Check service health
curl http://localhost:8000/health        # Agentic Service
curl http://localhost:8080/api/agent/health  # Backend
curl http://localhost:5000/api/tools/health  # Tools Service
curl http://localhost:3000              # Frontend
curl http://localhost:8070/api/isalive  # GROBID
redis-cli ping                          # Redis (should return PONG)
```

---

## 📖 Usage

### 🌟 Quick Start - Use the Live Application

**Try the live deployment immediately:**

👉 **[Open Application](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)** - `http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/`

👉 **[View Monitoring](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/agentic-research-server-metrics)** - Real-time metrics

---

### 1. Access the Application

**Live Production:**
```
http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/
```

**Local Development:**
```
http://localhost:3000
```

### 2. Login / Register

- Create a new account or login with existing credentials
- User profiles support roles: Student, Researcher, Professor

### 3. Submit a Research Goal

Example research goals:
- "Comparison of RIP and OSPF routing protocols"
- "Machine learning approaches for network intrusion detection"
- "Blockchain scalability solutions: sharding vs layer-2"

### 4. Configure Scope Parameters (Optional)

- **Discovery Depth**: Rapid (10 papers) | Focused (15) | Comprehensive (30) | Exhaustive (50)
- **Timeframe**: Last 1 year | 3 years | 5 years | All time
- **Quality Threshold**: Basic | Standard | High Impact

### 5. Monitor Progress

Track real-time progress through stages:
1. ✅ Planning (5-10 seconds)
2. ✅ Searching (20-40 seconds)
3. ✅ Validating (10-20 seconds)
4. ✅ Extracting (60-120 seconds)
5. ✅ Synthesizing (30-60 seconds)

### 6. Review Results

Your comprehensive report includes:
- Executive Summary
- 4-Phase Solution Roadmap
- Implementation Guide
- Decision Framework
- Literature Overview
- Methodology Analysis
- Comparison Matrix
- Research Gaps & Future Opportunities
- Full paper references

---

## 🔧 Service Details

### 1. **Frontend (React + Vite)**
**Location**: `/Frontend`  
**Port**: 3000 (development) / 80 (Docker production)  
**Purpose**: User interface for research goal submission and result visualization

**Key Features**:
- User authentication and session management
- Research goal input with scope parameters
- Real-time job status tracking via polling
- Interactive report viewer with markdown rendering
- Search history and saved research

**Technology**:
- React 19 with functional components and hooks
- Vite for fast development and optimized builds
- CSS for styling (no Tailwind in current implementation)
- Lucide React for icons
- React Markdown for report rendering

**API Integration**:
- Connects to Backend service (port 8080)
- Environment variable: `VITE_API_BASE_URL`

---

### 2. **Agentic Service (Python + FastAPI)**
**Location**: `/agentic`  
**Port**: 8000 (direct), 80 (via NGINX)  
**Purpose**: Core agentic intelligence system with autonomous research capabilities

**Key Components**:
- **Request Handler**: Receives research goals from Backend service
- **Agent Orchestration**: Coordinates 4 specialized agents
- **State Management**: Redis-based checkpointing and recovery
- **LLM Integration**: Gemini 2.5-flash for planning and synthesis

**Endpoints**:
```
POST   /api/research           - Submit new research goal
GET    /api/research/{job_id}  - Get job status and results  
GET    /health                 - Health check
GET    /metrics                - Prometheus metrics
```

**Technology**:
- FastAPI (high-performance async framework)
- Pydantic for request validation
- Redis client for state persistence
- ChromaDB client for vector operations
- Google Generative AI (Gemini) for LLM
- Instana for application monitoring (optional)

---

### 3. **Backend Gateway (Spring Boot)**
**Location**: `/backend`  
**Port**: 8080  
**Purpose**: API gateway between Frontend and Agentic service

**Key Components**:
- **Research Controller**: Proxies requests from Frontend to Agentic service
- **Polling Manager**: Polls Agentic service for job status updates
- **Redis Cache**: Caches research results and session data
- **CORS Configuration**: Handles cross-origin requests from Frontend

**Endpoints**:
```
POST   /api/agent/research         - Submit research request to Agentic
GET    /api/agent/research/{jobId} - Poll job status from Agentic
GET    /api/agent/health           - Health check
GET    /actuator/health            - Spring actuator health
```

**Configuration**:
- Connects to Agentic service via `agentic.service.url` (default: http://localhost:80)
- Polling interval: 2 seconds
- Max polling attempts: 150 (5 minutes)
- Redis for caching on port 6379

**Technology**:
- Spring Boot 3.2.1
- Spring Data Redis
- Spring Web with RestTemplate
- Spring Actuator for health monitoring

---

### 4. **Agentic Intelligence Layer (Python)**
**Location**: `/agentic/src/agent`  
**Purpose**: Core AI system with 4 specialized agents

#### **4.1 Planner Agent**
**Purpose**: Goal decomposition and execution planning

**Process**:
1. Parse research goal for key concepts
2. Use Gemini LLM to generate 3-5 search queries
3. Fallback to heuristic decomposition if LLM fails
4. Map scope parameters to execution targets
5. Create execution plan with phases

**Output**: Search queries, quality filters, max sources, execution phases

#### **4.2 Executor Agent**
**Purpose**: Orchestrates search and extraction workflows

**Process**:
1. **Search Phase**:
   - Execute primary search queries via Tools Service
   - Analyze result quality
   - Generate expansion queries if coverage gaps detected
   - Execute 2 additional refined searches
2. **Extraction Phase**:
   - Call Tools Service for each validated paper
   - Process PDFs and HTML sources
   - Store structured extractions in Redis

**Output**: 84 papers discovered, 26 successfully extracted

#### **4.3 Governance Engine**
**Purpose**: Relevance scoring and validation

**Process**:
1. **Dynamic Semantic Matching**:
   - Generate semantic keyword groups from research goal (runtime, not hardcoded)
   - Score each paper: 70% semantic + 15% citation + 10% recency + 5% metadata
   - Use ChromaDB for vector similarity matching
2. **Governance Policies**:
   - Min year filter (≥1990)
   - Min citations filter (≥5)
   - Peer-reviewed venue check
   - Dynamic threshold adjustment (0.35-0.65)

**Output**: 56 validated papers (67% acceptance rate) with scores

#### **4.4 Synthesizer Agent**
**Purpose**: NLP-based meta-analysis and report generation

**Process**:
1. Parse all extractions for recurring themes
2. Cluster papers by methodology and approach
3. Use Gemini LLM to generate 17-section report
4. Cross-reference citations and concepts
5. Validate coherence and accuracy

**17 Sections**:
1. Executive Summary
2. Solution Roadmap (4 phases)
3. Implementation Guide
4. Decision Framework
5. Success Metrics
6. Literature Overview
7. Methodology Analysis
8. Key Contributions
9. Comparison Matrix
10. Performance Analysis
11. Critical Analysis
12. Debates & Consensus
13. Case Studies
14. Security & Quality
15. Research Gaps
16. Future Opportunities
17. Detailed References

**Output**: 10,000+ word comprehensive report (50-55 min read)

**Technology**:
- Python 3.9+ with asyncio
- Gemini 2.5-flash for LLM operations
- ChromaDB for semantic matching
- Redis for state persistence

---

### 5. **Tools Service (Java + Spring Boot)**
**Location**: `/backend/tools-service`  
**Port**: 5000  
**Purpose**: External API integration and PDF processing

#### **5.1 OpenAlex API Integration**
**Purpose**: Academic paper discovery

**Process**:
1. Receive search queries from Executor Agent
2. Query OpenAlex API (https://api.openalex.org)
3. Extract metadata: title, author, year, citations, venue, URL
4. Return max 20 results per query
5. Handle rate limiting and retries

**Endpoints**:
```
POST /api/tools/search
```

#### **5.2 GROBID PDF Parser**
**Purpose**: Extract structured content from PDFs

**Process**:
1. Receive paper URLs from Executor Agent
2. Download PDF from source
3. Call GROBID service to parse PDF structure
4. Extract: Abstract, methodology, key findings, references
5. Return structured JSON
6. 96%+ success rate

**Endpoints**:
```
POST /api/tools/extract
```

**Technology**:
- Spring Boot 3.0+
- RestTemplate for HTTP calls
- GROBID 0.8.0 for PDF parsing
- Jackson for JSON processing

---

### 6. **Redis Cache**
**Port**: 6379  
**Purpose**: State management and checkpoint recovery

**Data Stored**:
- Job states: `job:{job_id}` → QUEUED, PLANNING, SEARCHING, etc.
- Discovered sources: `sources:{job_id}` → List of papers
- Validated sources: `validated_sources:{job_id}` → Scored papers
- Extractions: `extractions:{job_id}` → Structured content
- Final results: `results:{job_id}` → Complete synthesis

**Benefits**:
- Checkpoint recovery at any stage
- Fast in-memory access
- TTL for automatic cleanup
- Persistence option for durability

---

### 7. **ChromaDB**
**Port**: 8001  
**Purpose**: Vector database for semantic matching

**Usage**:
- Store paper embeddings for similarity search
- Semantic keyword matching
- Dynamic relevance scoring
- Theme clustering

**Technology**:
- ChromaDB (vector database)
- Embedding models for text vectorization

---

### 8. **Prometheus & Grafana**
**Ports**: 9090 (Prometheus), 3000 (Grafana)  
**Purpose**: Monitoring and visualization

**Live Grafana Dashboard:**
🔗 **[View Live Metrics](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/agentic-research-server-metrics)**
- URL: `http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/agentic-research-server-metrics`
- Login: `admin` / `admin`

**Metrics Collected**:
- Request rate and latency
- Job completion time by stage
- Success/failure rates
- Cache hit rates
- External API response times
- LLM API call rates (Gemini success/error)
- Redis memory usage
- HTTP request distribution by status

**Dashboards**:
- System health overview
- Job processing metrics
- Service dependencies
- Error tracking
- Real-time performance monitoring

---

### 9. **NGINX**
**Port**: 80/443  
**Purpose**: Reverse proxy and load balancer

**Configuration**:
- Route `/api/*` → Agentic Service (8000)
- Route `/` → Frontend (served by Backend or separate)
- SSL termination
- Rate limiting
- Request buffering

---

### 10. **DevOps Tools**

#### **Docker**
- Containerizes all services
- Docker Compose for orchestration
- Multi-stage builds for optimization

#### **GitHub**
- Version control
- CI/CD pipelines with GitHub Actions
- Automated testing on pull requests

#### **SonarQube**
- Static code analysis
- Code quality gates
- Security vulnerability detection
- Code coverage tracking

#### **JWT Authentication**
- Secure token-based authentication
- Role-based access control
- Token expiration and refresh

---

## ⚙️ Configuration

### Agentic Service Configuration

**File**: `agentic/.env` (copy from `.env.example`)

```bash
# Server Configuration
PORT=8000
HOST=0.0.0.0

# Redis Configuration
REDIS_HOST=redis  # or localhost for local dev
REDIS_PORT=6379
REDIS_DB=0

# LLM Configuration
GEMINI_API_KEY=your_key_here
LLM_MODEL=models/gemini-2.5-flash

# ChromaDB Configuration  
CHROMA_HOST=chromadb  # or localhost for local dev
CHROMA_PORT=8000

# Java Tools Service URLs
JAVA_TOOLS_URL=http://localhost:5000
JAVA_TOOLS_SEARCH_URL=http://localhost:5000/api/tools/search
JAVA_TOOLS_EXTRACT_URL=http://localhost:5000/api/tools/extract
JAVA_TOOLS_SEARCH_TIMEOUT=30.0
JAVA_TOOLS_EXTRACT_TIMEOUT=60.0

# Monitoring (Optional)
INSTANA_ENABLED=false
LOG_LEVEL=INFO
```

### Backend Service Configuration

**File**: `backend/src/main/resources/application.properties`

```properties
server.port=8080

# CORS Configuration
spring.web.cors.allowed-origins=http://localhost:3000,http://localhost:5173

# Redis Configuration
spring.data.redis.host=localhost
spring.data.redis.port=6379

# Agentic Service Configuration
agentic.service.url=http://localhost:80
agentic.service.poll.interval.ms=2000
agentic.service.poll.max.attempts=150
```

### Tools Service Configuration

**File**: `backend/tools-service/src/main/resources/application.properties`

```properties
# Server Configuration
server.port=5000

# GROBID Configuration
grobid.url=http://localhost:8070

# OpenAlex API (no authentication required)
openalex.api.url=https://api.openalex.org
```

### Frontend Configuration

**File**: `Frontend/.env.development` and `Frontend/.env.production`

```bash
# Development
VITE_API_BASE_URL=http://localhost:8080

# Production
VITE_API_BASE_URL=http://your-backend-url:8080
```

### Docker Compose Configuration

**Primary Files**:
- `docker-compose.local.yml` - Full stack local development (Frontend + Backend + Tools + Redis)
- `agentic/docker-compose.yml` - Agentic service development environment
- `agentic/docker-compose.prod.yml` - Agentic service production with Instana
- `agentic/docker-compose.free-tier.yml` - Free-tier deployment configuration

**Example**: `agentic/docker-compose.yml` (development)

```yaml
services:
  agentic_server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - CHROMA_HOST=chromadb
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - JAVA_TOOLS_URL=http://ec2-url:5000
    depends_on:
      - redis
      - chromadb

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  chromadb:
    image: chromadb/chroma:0.5.20
    ports:
      - "8001:8000"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - agentic_server
```

---

## 📚 API Documentation

### Backend Gateway API

Frontend communicates with Backend service on port 8080.

### Submit Research Job

**Endpoint**: `POST /api/agent/research`

**Request**:
```json
{
  "researchGoal": "Comparison of RIP and OSPF routing protocols",
  "scopeConfig": {
    "discoveryDepth": "comprehensive",
    "temporalBoundary": 3,
    "qualityThreshold": "high_impact"
  }
}
```

**Response**:
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "QUEUED",
  "message": "Research job submitted successfully"
}
```

### Get Job Status

**Endpoint**: `GET /api/agent/research/{jobId}`

**Response** (In Progress):
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "SEARCHING",
  "progress": {
    "currentStage": "SEARCHING",
    "stagesCompleted": ["PLANNING"],
    "percentage": 40
  }
}
```

**Response** (Completed):
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "progress": {
    "currentStage": "COMPLETED",
    "stagesCompleted": ["PLANNING", "SEARCHING", "VALIDATING", "EXTRACTING", "SYNTHESIZING"],
    "percentage": 100
  },
  "metrics": {
    "papers_discovered": 84,
    "papers_validated": 56,
    "papers_extracted": 26,
    "quality_rating": 9
  },
  "synthesis": {
    "full_text": "# GOAL-DRIVEN RESEARCH SYNTHESIS\n\n...",
    "word_count": 10063,
    "read_time_minutes": 52
  }
}
```

### Agentic Service API (Internal)

Backend calls Agentic service on port 80 (via NGINX) or 8000 (direct).

**Endpoints**:
```
POST   /api/research           - Submit research goal
GET    /api/research/{job_id}  - Get job status and results
GET    /health                 - Health check
GET    /metrics                - Prometheus metrics
```

---

## 🐛 Troubleshooting

### Common Issues

#### **1. Redis Connection Failed**
```bash
# Check if Redis is running
redis-cli ping

# Should return: PONG

# Restart Redis
docker restart redis

# Or if using docker-compose
cd agentic
docker-compose restart redis
```

#### **2. GROBID Service Not Responding**
```bash
# Check GROBID logs
docker logs grobid

# Restart GROBID
docker restart grobid

# Test GROBID endpoint
curl http://localhost:8070/api/isalive
```

#### **3. Backend Can't Connect to Agentic Service**
```bash
# Check if Agentic service is running
curl http://localhost:80/health  # via NGINX
curl http://localhost:8000/health  # direct

# Check agentic.service.url in backend/src/main/resources/application.properties
# Should be: http://localhost:80 for local with nginx
```

#### **4. Frontend Can't Reach Backend**
```bash
# Check Backend is running
curl http://localhost:8080/api/agent/health

# Check VITE_API_BASE_URL in Frontend/.env.development
# Should be: http://localhost:8080

# Check browser console for CORS errors
# Verify CORS settings in backend/src/main/resources/application.properties
```

#### **5. Tools Service Connection Issues**
```bash
# Check if Tools Service is running
curl http://localhost:5000/api/tools/health

# Check JAVA_TOOLS_URL in agentic/.env
# Should be: http://localhost:5000

# Check if GROBID is accessible from Tools Service
docker exec app_tools_local curl http://grobid:8070/api/isalive
```

#### **6. Gemini API Key Invalid**
```bash
# Verify API key is set in agentic/.env
cd agentic
grep GEMINI_API_KEY .env

# Test API key (replace with your key)
curl -H "Authorization: Bearer YOUR_KEY" \
  https://generativelanguage.googleapis.com/v1/models
```

#### **7. ChromaDB Connection Failed**
```bash
# Check ChromaDB is running
curl http://localhost:8001/api/v1/heartbeat

# Restart ChromaDB
docker restart chromadb

# Check logs
docker logs chromadb
```

### Logs

View logs for each service:

```bash
# Full stack (local)
docker-compose -f docker-compose.local.yml logs -f

# Specific services
docker logs app_frontend_local -f
docker logs app_backend_local -f
docker logs app_tools_local -f

# Agentic services (when running agentic/docker-compose.yml)
cd agentic
docker-compose logs -f

# Individual agentic services
docker logs agentic_server -f
docker logs agentic_redis -f
docker logs agentic_chromadb -f
```

---

### Code Style

- **Python**: Follow PEP 8 (use `black` formatter)
- **Java**: Follow Google Java Style Guide
- **JavaScript/React**: Use ESLint with Airbnb config

### Testing

```bash
# Python tests
cd api-service
pytest tests/

# Java tests
cd tools-service
./mvnw test

# Frontend tests
cd frontend
npm test
```

---

## 👥 Authors

- manasa.sadhu@sjsu.edu
- samvedsandeep.joshi@sjsu.edu

---

## 🙏 Acknowledgments

- **OpenAlex** - Open access to academic papers
- **Google Gemini** - AI-powered synthesis
- **GROBID** - PDF parsing library
- **ChromaDB** - Vector database
- All open-source contributors

---
