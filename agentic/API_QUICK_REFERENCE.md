# Quick Reference: Backend API Integration

## 🚀 TL;DR - What You Need to Know

### Main API: Execute Research
```bash
# Start a research job
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "What are recent advances in AI?",
    "scope_parameters": {
      "discovery_depth": "comprehensive"
    }
  }'

# Returns immediately with job_id
# {"job_id": "uuid", "status": "INITIALIZED", ...}

# Get results (wait ~60-120 seconds)
curl "http://localhost:8000/api/agent/results/{job_id}"
```

---

### Search API Response (EXACT format)
```json
{
  "results": [{
    "url": "https://arxiv.org/abs/2401.12345",        // REAL URL!
    "title": "Paper title",
    "snippet": "Abstract excerpt",
    "relevance_score": 0.92,                           // NOT quality_score
    "year": 2024,                                      // NUMBER, not string
    "citations": 150,
    "authors": ["Smith, J."],
    "venue": "NeurIPS 2024",
    "doi": "10.48550/arXiv.2401.12345"
  }],
  "total_found": 45,
  "search_metrics": {
    "query_time_ms": 234,
    "sources_searched": 3
  }
}
```

### Extraction API Response (EXACT format)
```json
{
  "extracted_content": {
    "title": "Paper Title",
    "abstract": "Full abstract text...",
    "key_findings": [
      "Specific finding 1 with numbers/results",
      "Specific finding 2 with numbers/results",
      "Specific finding 3 with numbers/results"
    ],
    "methodology": "Experimental approach description...",
    "citations": ["Author et al., 2024. Title. Venue."]
  },
  "metadata": {
    "extraction_success": true,        // ⚠️ CRITICAL - WE CHECK THIS!
    "source_url": "https://arxiv.org/abs/2401.12345",
    "extraction_timestamp": "2025-11-08T19:30:00Z"
  },
  "extraction_metrics": {
    "processing_time_ms": 3450,
    "confidence_score": 0.89
  }
}
```

---

## ⚠️ CRITICAL FIELDS (Don't mess these up!)

### Search API
- ✅ `relevance_score` (NOT `quality_score`)
- ✅ `year` as NUMBER (NOT string)
- ✅ `url` must be REAL and FETCHABLE

### Extraction API
- 🚨 **`metadata.extraction_success`** - WE CHECK THIS FIRST!
- ✅ `extracted_content.title`
- ✅ `extracted_content.abstract`
- ✅ `extracted_content.key_findings` - MUST have 2+ items
- ✅ `extracted_content.methodology`

---

## 🧪 Quick Test Commands

```bash
# Test Search
curl -X POST "http://localhost:5000/api/tools/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI trends", "max_results": 5}'

# Test Extraction (use URL from search)
curl -X POST "http://localhost:5000/api/tools/extract" \
  -H "Content-Type: application/json" \
  -d '{"source_url": "https://arxiv.org/abs/2401.12345"}'
```

---

## 🔥 Common Mistakes to Avoid

❌ **DON'T:**
- Return `quality_score` (we expect `relevance_score`)
- Return `publication_date: "2024-01-01"` (we expect `year: 2024`)
- Return fake URLs like `example.com/paper_1`
- Forget `extraction_success: true/false` flag
- Return empty `key_findings: []` with `extraction_success: true`

✅ **DO:**
- Return real arXiv/DOI URLs
- Set `extraction_success: false` if parsing fails
- Include at least 3 findings in `key_findings`
- Match field names exactly as specified

---

## 📊 Performance Targets

| API | Max Time | Calls per Request |
|-----|----------|-------------------|
| Search | 5 sec | 3-5 calls |
| Extraction | 10 sec | 9-30 calls |

**Total workflow:** ~60-120 seconds

---

## 🆘 Emergency Contact

If integration fails, check:
1. Field names match exactly (case-sensitive!)
2. Data types correct (number vs string)
3. `extraction_success` flag set correctly
4. URLs are real and fetchable

**Full docs:** See `BACKEND_API_SPECIFICATION.md`
