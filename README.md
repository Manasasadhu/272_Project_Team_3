# 🤖 Goal-Oriented Research Synthesis Agent

### **AWS EC2 Instances**

| Service | URL | Instance | Region | Port |
|---------|-----|----------|--------|------|
| **Web Application** | [ec2-18-219-157-24](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/) | `ec2-18-219-157-24.us-east-2.compute.amazonaws.com` | us-east-2 | 3000 |
| **Grafana Monitoring** | [ec2-3-236-6-48](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/) | `ec2-3-236-6-48.compute-1.amazonaws.com` | us-east-1 | 3000 |

- 👉 **[Open Research Agent](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)** - Submit research goals
- 📊 **[Grafana Dashboards](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/)** - Live metrics (admin/admin)

---

## 🎯 What It Does

Submit a research goal → System autonomously discovers papers → Validates sources → Extracts content → Generates comprehensive report

**Example**: "Comparison of RIP and OSPF routing protocols"
- 84 papers discovered → 56 validated (67%) → 26 extracted → 10,000+ word report in 120 seconds

---

## 🚀 Quick Start

1. **[Open the app](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)**
2. Enter research goal (e.g., "Machine learning for network security")
3. Configure depth: Rapid (10) / Focused (15) / Comprehensive (30) / Exhaustive (50) papers
4. Get results in ~2 minutes

---

## ✨ Key Features

- **Multi-Agent System** - Planner, Executor, Governance, Synthesizer agents
- **Smart Scoring** - 70% semantic relevance + 15% citations + 10% recency + 5% metadata
- **96%+ Extraction** - GROBID PDF parser with high success rate
- **Fault Tolerant** - Redis checkpoints enable resume capability
- **Observable** - Prometheus + Grafana dashboards
- **Quality Governed** - Min year (1990+), min citations (5+), audit trails

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 19, Vite, TypeScript |
| Backend Gateway | Spring Boot 3.2.1, Java 17 |
| Agentic Layer | Python FastAPI, LangChain |
| Search | OpenAlex API (no auth needed) |
| PDF Parsing | GROBID (96%+ success) |
| LLM | Google Gemini 2.5-flash |
| State | Redis 7, ChromaDB vectors |
| Monitoring | Prometheus + Grafana |
| Deployment | Docker, AWS EC2 |

---

## 📋 Architecture

```
Browser (React)
    ↓
Backend Gateway (Spring Boot - Port 8080)
    ↓
Agentic Service (Python FastAPI - Port 8000)
    ├─ Planner Agent
    ├─ Executor Agent
    ├─ Governance Engine
    ├─ Synthesizer Agent
    └─ Redis + ChromaDB + Prometheus
    ↓
Tools Service (Java - Port 5000)
    ├─ OpenAlex API → Paper discovery
    └─ GROBID → PDF extraction
```

---

## 📊 Results Example

| Metric | Value |
|--------|-------|
| Papers Discovered | 84 |
| Papers Validated | 56 (67% pass) |
| PDFs Extracted | 26 (96.3% success) |
| Report Length | 10,000+ words |
| Quality Rating | 9/10 |
| Time | ~120 seconds |

---

## 🏗️ For Developers

### Local Setup (Docker Compose)
```bash
git clone https://github.com/Manasasadhu/272_Project_Team_3.git
cd 272_Project_Team_3

# Set environment variables
export GEMINI_API_KEY=your_key_here
export JAVA_TOOLS_URL=http://localhost:5000

# Start all services
docker-compose -f agentic/docker-compose.yml up -d
```

### Access Points (Local)
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Agentic Service: http://localhost:8000
- Tools Service: http://localhost:5000
- Redis: localhost:6379
- ChromaDB: http://localhost:8001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Prerequisites
- Docker & Docker Compose 2.0+
- Python 3.9+, Java 17+, Node.js 18+
- Google Gemini API key

### Environment Variables (`.env` in `/agentic`)
```
GEMINI_API_KEY=your_gemini_api_key
REDIS_HOST=redis
REDIS_PORT=6379
CHROMA_HOST=chromadb
CHROMA_PORT=8000
JAVA_TOOLS_URL=http://localhost:5000
```

---

## 📚 API Documentation

**Submit Research**
```
POST /api/agent/execute
{
  "researchGoal": "Your research question",
  "scopeParameters": {
    "discovery_depth": "comprehensive",
    "quality_threshold": {"impact_level": "high_impact"},
    "temporal_boundary": {"publication_window_years": 3}
  }
}
```

Returns: 10,000+ word comprehensive report with 17 sections

**Check Status** (during execution)
```
GET /api/agent/status/{job_id}
```

**Full OpenAPI Spec**: See `openapi-spec.yaml`

---

## 🔗 Key Links

- **Live App**: http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/
- **Grafana**: http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/
- **GitHub**: https://github.com/Manasasadhu/272_Project_Team_3
- **OpenAPI Spec**: `openapi-spec.yaml`
- **Architecture Diagram**: See System Architecture section
- **Abstract**: `ABSTRACT.md`

---

## 🤝 Contributing

1. Clone the repo
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push: `git push origin feature/your-feature`
5. Open PR
