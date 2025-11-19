# 🤖 Goal-Oriented Research Synthesis Agent

**Autonomous Academic Research Discovery & Synthesis System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Java 17+](https://img.shields.io/badge/java-17+-orange.svg)](https://www.oracle.com/java/technologies/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://reactjs.org/)

---

## 📋 Table of Contents

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
User (ec2.lit-agent.com)
         ↓
      NGINX (Load Balancer)
         ↓
    ┌─────────────────────────────────────┐
    │        AWS EC2 Region               │
    │                                     │
    │  React Frontend (Port 3000)         │
    │         ↓                           │
    │  API Service (Python - Port 8000)   │
    │         ↓                           │
    │  ┌──────────────────────────────┐   │
    │  │ Agentic Intelligence Layer   │   │
    │  │  • Planner Agent             │   │
    │  │  • Executor Agent            │←→│ Redis (Port 6379)
    │  │  • Governance Engine         │←→│ ChromaDB
    │  │  • Synthesizer Agent         │   │ Prometheus (9090)
    │  └──────────────────────────────┘   │ Grafana
    │         ↓                           │
    │  Tools Service (Java - Port 8080)   │
    │  • OpenAlex API Integration         │
    │  • GROBID PDF Parser                │
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
git clone https://github.com/your-org/goal-oriented-research-agent.git
cd goal-oriented-research-agent
```

### 2. Set Up Environment Variables

Create `.env` files in each service directory:

#### **API Service** (`.env` in `/api-service`)
```bash
# API Service Configuration
PORT=8000
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Gemini LLM Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8001

# Tools Service
TOOLS_SERVICE_URL=http://localhost:8080

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### **Tools Service** (`.env` in `/tools-service`)
```bash
# Tools Service Configuration
SERVER_PORT=8080

# OpenAlex API
OPENALEX_API_URL=https://api.openalex.org

# GROBID Configuration
GROBID_HOST=localhost
GROBID_PORT=8070

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

#### **Frontend** (`.env` in `/frontend`)
```bash
# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
PORT=3000
```

### 3. Install Dependencies

#### **Frontend**
```bash
cd frontend
npm install
cd ..
```

#### **API Service (Python)**
```bash
cd api-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

#### **Tools Service (Java)**
```bash
cd tools-service
./mvnw clean install  # On Windows: mvnw.cmd clean install
cd ..
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
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.7.3
```

---

## ▶️ Starting Services

### Option 1: Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Option 2: Manual Start (for Development)

#### **Terminal 1: Start Redis & ChromaDB**
```bash
# Redis
redis-server

# ChromaDB (in another tab)
chroma run --host localhost --port 8001
```

#### **Terminal 2: Start GROBID**
```bash
docker run -p 8070:8070 lfoppiano/grobid:0.7.3
```

#### **Terminal 3: Start Tools Service (Java)**
```bash
cd tools-service
./mvnw spring-boot:run
# Service will start on http://localhost:8080
```

#### **Terminal 4: Start API Service (Python)**
```bash
cd api-service
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Service will start on http://localhost:8000
```

#### **Terminal 5: Start Frontend (React)**
```bash
cd frontend
npm start
# Application will open on http://localhost:3000
```

#### **Optional: Start Monitoring**
```bash
# Prometheus
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Grafana
docker run -d --name grafana -p 3001:3000 grafana/grafana
```

### Verify All Services Are Running

```bash
# Check service health
curl http://localhost:8000/health  # API Service
curl http://localhost:8080/actuator/health  # Tools Service
curl http://localhost:3000  # Frontend
```

---

## 📖 Usage

### 1. Access the Application

Open your browser and navigate to:
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

### 1. **Frontend (React)**
**Location**: `/frontend`  
**Port**: 3000  
**Purpose**: User interface for research goal submission and result visualization

**Key Features**:
- User authentication and session management
- Research goal input with scope parameters
- Real-time job status tracking
- Interactive report viewer
- Search history and saved research

**Technology**:
- React 18 with functional components and hooks
- Axios for API communication
- Tailwind CSS for styling
- React Router for navigation

---

### 2. **API Service (Python)**
**Location**: `/api-service`  
**Port**: 8000  
**Purpose**: Gateway between frontend and agentic intelligence layer

**Key Components**:
- **Request Handler**: Receives and validates user requests
- **Job Router**: Creates job IDs and routes to agentic layer
- **Response Manager**: Fetches results from Redis and formats response
- **Authentication**: JWT-based user authentication

**Endpoints**:
```
POST   /api/research/submit    - Submit new research goal
GET    /api/research/{job_id}  - Get job status and results
GET    /api/research/history   - Get user's research history
POST   /api/auth/login         - User authentication
POST   /api/auth/register      - User registration
GET    /api/health             - Health check
```

**Technology**:
- FastAPI (high-performance async framework)
- Pydantic for request validation
- Redis client for state management
- JWT for authentication

---

### 3. **Agentic Intelligence Layer (Python)**
**Location**: `/api-service/agents`  
**Purpose**: Core AI system with 4 specialized agents

#### **3.1 Planner Agent**
**Purpose**: Goal decomposition and execution planning

**Process**:
1. Parse research goal for key concepts
2. Use Gemini LLM to generate 3-5 search queries
3. Fallback to heuristic decomposition if LLM fails
4. Map scope parameters to execution targets
5. Create execution plan with phases

**Output**: Search queries, quality filters, max sources, execution phases

#### **3.2 Executor Agent**
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

#### **3.3 Governance Engine**
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

#### **3.4 Synthesizer Agent**
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

### 4. **Tools Service (Java)**
**Location**: `/tools-service`  
**Port**: 8080  
**Purpose**: External API integration and PDF processing

#### **4.1 OpenAlex API Integration**
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

#### **4.2 GROBID PDF Parser**
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
- GROBID 0.7.3 for PDF parsing
- Jackson for JSON processing

---

### 5. **Redis Cache**
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

### 6. **ChromaDB**
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

### 7. **Prometheus & Grafana**
**Ports**: 9090 (Prometheus), 3001 (Grafana)  
**Purpose**: Monitoring and visualization

**Metrics Collected**:
- Request rate and latency
- Job completion time by stage
- Success/failure rates
- Cache hit rates
- External API response times

**Dashboards**:
- System health overview
- Job processing metrics
- Service dependencies
- Error tracking

---

### 8. **NGINX**
**Port**: 80/443  
**Purpose**: Reverse proxy and load balancer

**Configuration**:
- Route `/api/*` → API Service (8000)
- Route `/` → Frontend (3000)
- SSL termination
- Rate limiting
- Request buffering

---

### 9. **DevOps Tools**

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

### API Service Configuration

**File**: `api-service/config.py`

```python
# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# LLM Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# Scope Parameters
DISCOVERY_DEPTH_MAP = {
    "rapid": 10,
    "focused": 15,
    "comprehensive": 30,
    "exhaustive": 50
}

# Governance Policies
MIN_PUBLICATION_YEAR = 1990
MIN_CITATIONS = 5
RELEVANCE_THRESHOLD = 0.35
```

### Tools Service Configuration

**File**: `tools-service/src/main/resources/application.properties`

```properties
# Server Configuration
server.port=8080

# OpenAlex API
openalex.api.url=https://api.openalex.org
openalex.api.max-results=20

# GROBID Configuration
grobid.host=localhost
grobid.port=8070

# Redis Configuration
spring.redis.host=localhost
spring.redis.port=6379
```

### Docker Compose Configuration

**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://api-service:8000

  api-service:
    build: ./api-service
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - CHROMA_HOST=chromadb
      - TOOLS_SERVICE_URL=http://tools-service:8080
    depends_on:
      - redis
      - chromadb

  tools-service:
    build: ./tools-service
    ports:
      - "8080:8080"
    environment:
      - GROBID_HOST=grobid
    depends_on:
      - grobid

  redis:
    image: redis:7.0-alpine
    ports:
      - "6379:6379"

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"

  grobid:
    image: lfoppiano/grobid:0.7.3
    ports:
      - "8070:8070"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
```

---

## 📚 API Documentation

### Submit Research Job

**Endpoint**: `POST /api/research/submit`

**Request**:
```json
{
  "research_goal": "Comparison of RIP and OSPF routing protocols",
  "scope": {
    "discovery_depth": "comprehensive",
    "temporal_boundary": 3,
    "quality_threshold": "high_impact"
  }
}
```

**Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "QUEUED",
  "created_at": "2025-01-15T10:30:00Z",
  "message": "Research job created successfully"
}
```

### Get Job Status

**Endpoint**: `GET /api/research/{job_id}`

**Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "progress": {
    "current_stage": "SYNTHESIZING",
    "stages_completed": ["PLANNING", "SEARCHING", "VALIDATING", "EXTRACTING"],
    "percentage": 100
  },
  "metrics": {
    "papers_discovered": 84,
    "papers_validated": 56,
    "papers_extracted": 26,
    "quality_rating": 9
  },
  "synthesis": {
    "full_text": "GOAL-DRIVEN RESEARCH SYNTHESIS...",
    "word_count": 10063,
    "read_time_minutes": 52
  }
}
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

#### **3. API Service Can't Connect to Tools Service**
```bash
# Check if Tools Service is running
curl http://localhost:8080/actuator/health

# Check network connectivity
docker network inspect goal-oriented-research-agent_default
```

#### **4. Frontend Can't Reach API**
```bash
# Check CORS configuration in API service
# Verify REACT_APP_API_URL in .env
# Check browser console for errors
```

#### **5. Gemini API Key Invalid**
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Test API key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models
```

### Logs

View logs for each service:

```bash
# API Service
docker logs api-service -f

# Tools Service
docker logs tools-service -f

# Frontend
docker logs frontend -f

# Redis
docker logs redis -f
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
