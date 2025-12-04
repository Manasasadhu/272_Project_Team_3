# Goal-Oriented Research Synthesis Agent

### AWS EC2 Instances

| Service | URL | Instance | Region | Port |
|---------|-----|----------|--------|------|
| **Web Application** | [ec2-18-219-157-24](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/) | `ec2-18-219-157-24.us-east-2.compute.amazonaws.com` | us-east-2 | 3000 |
| **Grafana Monitoring** | [ec2-3-236-6-48](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/) | `ec2-3-236-6-48.compute-1.amazonaws.com` | us-east-1 | 3000 |

- **[Open Research Agent](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)** - Submit research goals
- **[Grafana Dashboards](http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/)** - Live metrics (admin/admin)

---

## What It Does

Submit a research goal → System autonomously discovers papers → Validates sources → Extracts content → Generates comprehensive report

**Example**: "Comparison of RIP and OSPF routing protocols"
- 84 papers discovered → 56 validated (67%) → 26 extracted → 10,000+ word report in 120 seconds

---

## Quick Start

1. **[Open the app](http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/)**
2. Enter research goal (e.g., "Machine learning for network security")
3. Configure depth: Rapid (10) / Focused (15) / Comprehensive (30) / Exhaustive (50) papers
4. Get results in ~2 minutes

---

## Key Features

- **Multi-Agent System** - Planner, Executor, Governance, Synthesizer agents
- **Smart Scoring** - 70% semantic relevance + 15% citations + 10% recency + 5% metadata
- **96%+ Extraction** - GROBID PDF parser with high success rate
- **Fault Tolerant** - Redis checkpoints enable resume capability
- **Observable** - Prometheus + Grafana dashboards
- **Quality Governed** - Min year (1990+), min citations (5+), audit trails

---

## Tech Stack

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

## Architecture

![alt text](High_Level_Arch.png)

---

## Results Example

| Metric | Value |
|--------|-------|
| Papers Discovered | 84 |
| Papers Validated | 56 (67% pass) |
| PDFs Extracted | 26 (96.3% success) |
| Report Length | 10,000+ words |
| Quality Rating | 9/10 |
| Time | ~120 seconds |

---

## For Developers

See **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed local setup, environment configuration, and development workflow.

**Quick links:**
- Local access: http://localhost:3000 (Frontend)
- API: http://localhost:8080 (Backend)
- Monitoring: http://localhost:3000/d/agentic-metrics/ (Grafana)

---

## API Documentation

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

## Key Links

- **Live App**: http://ec2-18-219-157-24.us-east-2.compute.amazonaws.com:3000/
- **Grafana**: http://ec2-3-236-6-48.compute-1.amazonaws.com:3000/d/agentic-metrics/
- **GitHub**: https://github.com/Manasasadhu/272_Project_Team_3
- **OpenAPI Spec**: `openapi-spec.yaml`
- **Architecture Diagram**: `architecture-diagram.png`
