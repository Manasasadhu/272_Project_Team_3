# Agentic Research Server - API Documentation

## Base URL
```
http://ec2-3-236-6-48.compute-1.amazonaws.com
```

---

## 1. Execute Research Agent

### Endpoint
```
POST /api/agent/execute
```

### Description
Submits a research goal to the autonomous agent and returns a job ID for tracking.

### Request Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "research_goal": "string (required, 10-500 characters)",
  "scope_parameters": {
    "discovery_depth": "rapid | focused | comprehensive | exhaustive",
    "temporal_boundary": {
      "publication_window_years": 1-10
    },
    "quality_threshold": {
      "impact_level": "cutting_edge | high_impact | established | baseline"
    },
    "source_diversity_requirement": true
  }
}
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `research_goal` | string | ✅ Yes | The research question or goal (10-500 chars) |
| `scope_parameters.discovery_depth` | string | ❌ No | Search depth: `rapid` (quick), `comprehensive` (thorough). Default: `comprehensive` |
| `scope_parameters.temporal_boundary.publication_window_years` | integer | ❌ No | Years to search (1-10). Default: 3 |
| `scope_parameters.quality_threshold.impact_level` | string | ❌ No | Paper impact level. Default: `high_impact` |
| `scope_parameters.source_diversity_requirement` | boolean | ❌ No | Require diverse sources. Default: true |

### Response (200 OK)
```json
{
  "job_id": "string (UUID)",
  "status": "queued",
  "autonomous_analysis": {
    "goal_decomposition": {},
    "execution_strategy": {},
    "governance_applied": {}
  },
  "execution_plan": {
    "phases": [
      {
        "phase": "phase_name",
        "description": "phase_description"
      }
    ],
    "estimated_sources": 15,
    "estimated_duration_minutes": 5
  }
}
```

### Example Request
```bash
curl -X POST http://ec2-3-236-6-48.compute-1.amazonaws.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "What are the latest breakthroughs in transformer-based language models?",
    "scope_parameters": {
      "discovery_depth": "comprehensive",
      "temporal_boundary": {
        "publication_window_years": 2
      },
      "quality_threshold": {
        "impact_level": "cutting_edge"
      }
    }
  }'
```

### Example Response
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "autonomous_analysis": {
    "goal_decomposition": {
      "sub_goals": ["Identify recent transformer architectures", "Find performance improvements"]
    },
    "execution_strategy": {
      "search_strategy": "multi-source",
      "validation_level": "high"
    },
    "governance_applied": {
      "policy_checks": ["academic_integrity", "source_verification"]
    }
  },
  "execution_plan": {
    "phases": [
      {
        "phase": "search",
        "description": "Search for relevant research papers"
      },
      {
        "phase": "synthesis",
        "description": "Synthesize findings"
      }
    ],
    "estimated_sources": 20,
    "estimated_duration_minutes": 8
  }
}
```

### Status Codes
- `200 OK` - Research job successfully created
- `422 Unprocessable Entity` - Invalid request body
- `500 Internal Server Error` - Server error

---

## 2. Get Research Results

### Endpoint
```
GET /api/agent/results/{job_id}
```

### Description
Retrieves the synthesized research results for a completed job.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string (UUID) | ✅ Yes | The job ID returned from `/execute` endpoint |

### Response (200 OK)
```json
{
  "job_id": "string",
  "status": "completed | running | failed",
  "synthesis": {
    "key_findings": [
      {
        "title": "string",
        "description": "string",
        "evidence": [
          {
            "source": "string",
            "citation": "string"
          }
        ]
      }
    ],
    "research_summary": "string",
    "conclusion": "string"
  },
  "metadata": {
    "started_at": "2025-11-16T21:00:00Z",
    "completed_at": "2025-11-16T21:05:30Z",
    "processing_time_seconds": 330,
    "sources_analyzed": 15
  }
}
```

### Example Request
```bash
curl -X GET http://ec2-3-236-6-48.compute-1.amazonaws.com/api/agent/results/550e8400-e29b-41d4-a716-446655440000
```

### Example Response
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "synthesis": {
    "key_findings": [
      {
        "title": "Attention Mechanism Improvements",
        "description": "Recent papers show 30% efficiency gains in transformer attention mechanisms",
        "evidence": [
          {
            "source": "arXiv:2025.xxxxx",
            "citation": "Smith et al., 2025"
          }
        ]
      }
    ],
    "research_summary": "Transformer models continue to improve with focus on efficiency and scalability...",
    "conclusion": "The field is rapidly evolving with emphasis on practical deployment."
  },
  "metadata": {
    "started_at": "2025-11-16T21:00:00Z",
    "completed_at": "2025-11-16T21:05:30Z",
    "processing_time_seconds": 330,
    "sources_analyzed": 18
  }
}
```

### Status Codes
- `200 OK` - Results retrieved successfully
- `404 Not Found` - Job ID not found
- `400 Bad Request` - Job still processing or failed
- `500 Internal Server Error` - Server error

---

## Usage Workflow

### Step 1: Submit Research Request
```bash
# Call execute endpoint
JOB_ID=$(curl -s -X POST http://ec2-3-236-6-48.compute-1.amazonaws.com/api/agent/execute \
  -H "Content-Type: application/json" \
  -d '{"research_goal":"Your research question"}' \
  | jq -r '.job_id')

echo "Job ID: $JOB_ID"
```

### Step 2: Wait for Completion
```bash
# Poll status until complete (typical: 2-10 minutes)
while true; do
  STATUS=$(curl -s http://ec2-3-236-6-48.compute-1.amazonaws.com/api/agent/status/$JOB_ID \
    | jq -r '.status')
  
  if [ "$STATUS" = "completed" ]; then
    echo "Research complete!"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Research failed!"
    break
  else
    echo "Status: $STATUS... waiting"
    sleep 10
  fi
done
```

### Step 3: Retrieve Results
```bash
# Get the final results
curl -s http://ec2-3-236-6-48.compute-1.amazonaws.com/api/agent/results/$JOB_ID | jq
```

---

## Error Handling

### Common Errors

#### Invalid Research Goal
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "research_goal"],
      "msg": "ensure this value has at least 10 characters",
      "input": "short"
    }
  ]
}
```

#### Job Not Found
```json
{
  "detail": "Job not found"
}
```

#### Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits
- No rate limiting currently enabled
- Concurrent jobs: Limited by server resources (typical: 1-3 concurrent)

## Timeout
- Request timeout: 300 seconds per job
- Research duration: 2-15 minutes typically

---

## Support
For issues or questions, contact the development team.
