# Goal-Oriented Knowledge Discovery Agent

Autonomous agentic server for knowledge discovery and research synthesis.

## Quick Start

1. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

2. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Usage

### Execute Agent
```bash
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "Analyze emerging methodologies in distributed consensus",
    "scope_parameters": {
      "discovery_depth": "comprehensive",
      "temporal_boundary": {"publication_window_years": 3},
      "quality_threshold": {"impact_level": "high_impact"}
    }
  }'
```

### Check Status
```bash
curl "http://localhost:8000/api/agent/status/{job_id}"
```

### Get Results
```bash
curl "http://localhost:8000/api/agent/results/{job_id}"
```

## Architecture

- **Infrastructure Layer**: Config, Redis, LLM client
- **Domain Models**: Data structures
- **Governance Layer**: Policy engine, validator, audit logger
- **Tool Layer**: Search and extraction tools
- **Agent Core**: ReAct agent, planner, executor
- **Service Layer**: Orchestrator, synthesis service
- **API Layer**: FastAPI endpoints

## Storage

Redis is used for persistent storage with AOF persistence enabled. All agent state, sources, extractions, and audit logs are stored in Redis.

