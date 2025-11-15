# Setup Instructions

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Quick Start

1. **Set environment variable:**
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

2. **Start services:**
   ```bash
   cd agentic
   docker-compose up --build
   ```

3. **Access API:**
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Environment Variables

Set these before running:
- `OPENAI_API_KEY` - Required for LLM calls
- `LLM_MODEL` - Optional, defaults to `gpt-4o`

## Testing

### Execute Agent
```bash
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "Analyze emerging methodologies in distributed consensus",
    "scope_parameters": {
      "discovery_depth": "comprehensive"
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

## Troubleshooting

- **Redis connection error**: Ensure Redis container is healthy
- **OpenAI API error**: Check API key is set correctly
- **Import errors**: Ensure PYTHONPATH is set (handled in Dockerfile)

