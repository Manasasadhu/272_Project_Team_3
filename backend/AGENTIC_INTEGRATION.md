# Backend-Agentic Service Integration

## Overview
The backend (port 8080) now acts as an orchestrator that forwards research requests to the agentic service (port 80) and polls for results.

## Architecture Flow

```
Frontend (3000) → Backend (8080) → Agentic Service (80)
                      ↓
                  Poll Status
                      ↓
                  Get Results
                      ↓
                  Frontend
```

## Implementation Details

### Step 1: Submit Research Request
When frontend calls `POST /api/agent/execute`:

1. **Backend receives request** with `ResearchRequest`:
   - `researchGoal` (string, 10-500 chars)
   - `scopeParameters` (optional):
     - `timeRange` (integer, years)
     - `researchDepth` (string: rapid/focused/comprehensive/exhaustive)
     - `sourceQuality` (string: cutting_edge/high_impact/established/baseline)
     - `sourceDiversity` (boolean)

2. **Backend transforms to AgenticResearchRequest**:
   - Maps fields with snake_case naming (`research_goal`, `scope_parameters`)
   - Creates unique internal `jobId`

3. **Backend POSTs to Agentic Service**:
   ```
   POST http://localhost:80/api/agent/research
   Body: AgenticResearchRequest
   Response: { job_id, status }
   ```

4. **Backend returns immediately** (202 Accepted):
   - Returns `JobResponse` with internal `jobId`
   - Starts async polling in background thread

### Step 2: Poll Agentic Status
Background thread polls every 2 seconds (configurable):

```
GET http://localhost:80/api/agent/research/{agenticJobId}/status
Response: {
  job_id,
  status,
  current_phase,
  progress_percentage
}
```

**Updates internal JobStatus**:
- Maps `current_phase` from agentic service
- Converts `progress_percentage` to `sources_processed_count`
- Continues until status is `COMPLETED` or `FAILED`
- Max 150 attempts (5 minutes timeout)

### Step 3: Fetch Final Results
When agentic service returns `COMPLETED`:

```
GET http://localhost:80/api/agent/research/{agenticJobId}/results
Response: {
  job_id,
  status,
  sources: [...],
  detailed_analysis: {...},
  executive_summary: {...}
}
```

**Transforms AgenticJobResult to JobResult**:
- Maps source fields
- Converts detailed_analysis
- Transforms executive_summary
- Stores in internal cache

### Step 4: Frontend Retrieves Results
Frontend polls `GET /api/agent/status/{jobId}` and when complete, calls `GET /api/agent/results/{jobId}` to display results.

## Configuration

### application.properties
```properties
# Agentic Service Configuration
agentic.service.url=http://localhost:80
agentic.service.poll.interval.ms=2000
agentic.service.poll.max.attempts=150
```

### For Production (EC2)
Update `agentic.service.url` to your EC2 public IP:
```properties
agentic.service.url=http://<EC2_PUBLIC_IP>:80
```

## New Files Created

1. **RestTemplateConfig.java** - Spring RestTemplate bean configuration
2. **AgenticResearchRequest.java** - Request DTO for agentic service
3. **AgenticScopeParameters.java** - Scope parameters DTO
4. **AgenticJobResponse.java** - Initial job submission response
5. **AgenticJobStatus.java** - Status polling response
6. **AgenticJobResult.java** - Final results response with nested classes

## Data Transformation

### Request Mapping
| Backend Field | Agentic Field |
|--------------|---------------|
| researchGoal | research_goal |
| scopeParameters.timeRange | scope_parameters.time_range |
| scopeParameters.researchDepth | scope_parameters.research_depth |
| scopeParameters.sourceQuality | scope_parameters.source_quality |
| scopeParameters.sourceDiversity | scope_parameters.source_diversity |

### Response Mapping
| Agentic Field | Backend Field |
|--------------|---------------|
| sources[].source_id | sources[].sourceId |
| sources[].publication_year | sources[].publicationYear |
| detailed_analysis.main_findings | detailedAnalysis.mainFindings |
| detailed_analysis.key_takeaways | detailedAnalysis.keyTakeaways |
| executive_summary.highlights | executiveSummary.highlights |
| executive_summary.consolidated_conclusions | executiveSummary.consolidatedConclusions |

## Error Handling

- **Connection errors**: Caught and set job status to FAILED
- **Timeout**: Max 150 attempts (5 minutes), then FAILED
- **Service errors**: Propagated to job status with error message
- **Interrupted threads**: Properly handled with status update

## Testing the Integration

### 1. Start Agentic Service (Port 80)
```bash
cd agentic
docker-compose -f docker-compose.prod.yml up -d
# Verify: curl http://localhost/health
```

### 2. Start Backend (Port 8080)
```bash
cd backend
/tmp/apache-maven-3.8.8/bin/mvn spring-boot:run
```

### 3. Start Frontend (Port 3000)
```bash
cd Frontend
npm run dev -- --port 3000
```

### 4. Test End-to-End Flow
1. Open http://localhost:3000
2. Login/Signup
3. Submit research query
4. Watch progress updates
5. View results when complete

## Monitoring

### Backend Logs
Watch for:
- `Submitting to Agentic Service`
- `Processing by Agentic Service`
- Progress updates with phase names
- `COMPLETED` or `FAILED` status

### Agentic Service Logs
```bash
docker logs -f agentic_server
```

### Check Status Manually
```bash
# Backend job status
curl http://localhost:8080/api/agent/status/{jobId}

# Agentic job status
curl http://localhost:80/api/agent/research/{agenticJobId}/status
```

## Performance Considerations

- **Async processing**: Non-blocking job submission
- **Thread pool**: CachedThreadPool for concurrent jobs
- **Polling interval**: 2 seconds (configurable)
- **Timeout**: 5 minutes max (configurable)
- **In-memory storage**: ConcurrentHashMap for job state

## Future Enhancements

1. **Persistent storage**: Store jobs in Redis/database instead of memory
2. **WebSocket updates**: Push real-time updates instead of polling
3. **Retry logic**: Automatic retry on transient failures
4. **Circuit breaker**: Fail fast when agentic service is down
5. **Metrics**: Track success rate, latency, error types
