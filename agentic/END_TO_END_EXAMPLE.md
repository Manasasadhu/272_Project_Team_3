# End-to-End API Integration Example

## Complete Workflow Demo

This document shows a complete example of using all three APIs together.

---

## Scenario
**Goal:** Analyze recent advances in transformer architectures

**Expected Flow:**
1. User calls agentic server with research goal
2. Agentic server calls search API 3-5 times
3. Agentic server calls extraction API 9-30 times  
4. Agentic server synthesizes and returns results

---

## Step 1: Start Research Job

### Request
```bash
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "What are recent advances in transformer architectures?",
    "scope_parameters": {
      "temporal_boundary": {
        "publication_window_years": 2
      },
      "discovery_depth": "comprehensive"
    }
  }'
```

### Response (Immediate - ~1 second)
```json
{
  "job_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "status": "INITIALIZED",
  "autonomous_analysis": {
    "goal_decomposition": {
      "primary_objectives": [
        "Identify novel transformer architectures from 2023-2024",
        "Analyze efficiency improvements",
        "Extract methodology patterns"
      ]
    }
  },
  "execution_plan": {
    "phases": [
      {"phase": "Autonomous Exploration", "description": "Search academic databases"},
      {"phase": "Intelligent Validation", "description": "Filter by quality"},
      {"phase": "Deep Extraction", "description": "Extract from 30 papers"},
      {"phase": "Meta-Analysis", "description": "Synthesize findings"}
    ],
    "estimated_sources": 30,
    "estimated_duration_minutes": 2
  }
}
```

**Job started! Now the agent works autonomously...**

---

## Step 2: What Happens Behind the Scenes

### 2.1 Agent Generates Search Queries
The agent uses Gemini to create 5 targeted queries:
- "transformer architecture improvements 2023 2024"
- "efficient attention mechanisms large language models"
- "sparse transformer neural networks"
- "mixture of experts transformer architecture"
- "low rank adaptation transformers"

### 2.2 Agent Calls Search API (5 times)

**Example Call:**
```bash
# This happens automatically inside the agent
curl -X POST "http://search_service:5000/api/tools/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "transformer architecture improvements 2023 2024",
    "filters": {
      "year_range": {"start": 2023, "end": 2024},
      "min_quality_score": 0.7
    },
    "max_results": 20
  }'
```

**Search API Returns:**
```json
{
  "results": [
    {
      "url": "https://arxiv.org/abs/2401.12345",
      "title": "Sparse Attention Transformers: 40% Faster Training",
      "snippet": "We propose a novel sparse attention mechanism...",
      "relevance_score": 0.94,
      "year": 2024,
      "citations": 87,
      "authors": ["Chen, L.", "Smith, J."],
      "venue": "ICML 2024",
      "doi": "10.48550/arXiv.2401.12345"
    },
    // ... 19 more papers
  ],
  "total_found": 156
}
```

**Agent collects:** ~60-100 papers from all 5 queries

### 2.3 Agent Scores Relevance (Batch)

**Agent generates one prompt scoring 20 papers at once:**
```
Rate relevance (0.0-1.0) for each paper:
Goal: transformer architecture improvements

Papers:
0. Sparse Attention Transformers: 40% Faster Training
1. Mixture of Experts in Large Language Models
2. LoRA: Low-Rank Adaptation of Large Models
...
19. Quantum Computing for Neural Networks

Return: 0.95,0.88,0.92,...,0.23
```

**Filters:** Keeps papers with score ≥ 0.6, selects top 9-30

### 2.4 Agent Calls Extraction API (9-30 times)

**Example Call:**
```bash
# This happens automatically for each selected paper
curl -X POST "http://extraction_service:5000/api/tools/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "https://arxiv.org/abs/2401.12345",
    "extraction_parameters": {
      "required_elements": ["key_findings", "methodology", "conclusions"]
    }
  }'
```

**Extraction API Returns:**
```json
{
  "extracted_content": {
    "title": "Sparse Attention Transformers: 40% Faster Training",
    "abstract": "We propose a novel sparse attention mechanism that reduces computational complexity...",
    "key_findings": [
      "Sparse attention reduces training time by 40% vs dense attention",
      "Model achieves 96.3% accuracy on GLUE, matching dense baseline",
      "Memory footprint reduced by 50% for sequences >2048 tokens",
      "Scales to 175B parameters with linear complexity"
    ],
    "methodology": "Experimented with various sparsity patterns on GPT-3 architecture. Training on 300B tokens using 512 A100 GPUs. Compared against dense attention baseline across 5 benchmarks.",
    "citations": [
      "Vaswani et al., 2017. Attention is All You Need",
      "Child et al., 2019. Generating Long Sequences with Sparse Transformers"
    ]
  },
  "metadata": {
    "extraction_success": true,
    "source_url": "https://arxiv.org/abs/2401.12345",
    "extraction_timestamp": "2025-11-08T19:35:22Z"
  },
  "extraction_metrics": {
    "processing_time_ms": 4230,
    "confidence_score": 0.91
  }
}
```

**Agent collects:** 9-30 extracted papers with real findings

### 2.5 Agent Synthesizes with Gemini

**Agent creates synthesis prompt:**
```
Synthesize research findings from 9 papers on transformer architectures.

Papers analyzed:
1. Sparse Attention Transformers: Findings - [40% faster training, 96.3% accuracy...]
2. Mixture of Experts Architecture: Findings - [...]
...

Generate:
- Executive summary
- Primary themes (3-5)
- Key patterns across papers
- Identified gaps
```

**Gemini generates comprehensive synthesis**

---

## Step 3: Poll Status (Optional)

```bash
# Check progress while agent is working
curl "http://localhost:8000/api/agent/status/a1b2c3d4-5678-90ab-cdef-1234567890ab"
```

### Response During Execution
```json
{
  "job_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "status": "EXTRACTING",
  "current_phase": {
    "phase_name": "EXTRACTING",
    "progress_percentage": 65,
    "intelligent_actions_taken": [
      "Discovered 78 sources",
      "Filtered to 15 highly relevant sources",
      "Extracted 9 sources successfully"
    ]
  },
  "autonomous_decisions": [
    {
      "timestamp": "2025-11-08T19:34:15Z",
      "decision_type": "RELEVANCE_FILTER",
      "reasoning": "Batch relevance scoring complete",
      "action_taken": "Kept 15 highly relevant sources"
    }
  ],
  "quality_metrics": {
    "sources_discovered": 78,
    "sources_validated": 78,
    "sources_accepted": 15,
    "average_quality_score": 0.87
  }
}
```

---

## Step 4: Get Final Results

```bash
# After ~60-120 seconds, results are ready
curl "http://localhost:8000/api/agent/results/a1b2c3d4-5678-90ab-cdef-1234567890ab"
```

### Response (Final Synthesis)
```json
{
  "job_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "status": "COMPLETED",
  "synthesis": {
    "research_goal": "What are recent advances in transformer architectures?",
    "executive_summary": "## Recent Advances in Transformer Architectures (2023-2024)\n\nAnalysis of 9 high-impact papers reveals three major trends: sparse attention mechanisms achieving 40-50% training speedups, mixture-of-experts architectures enabling efficient scaling to 1T+ parameters, and parameter-efficient fine-tuning methods like LoRA reducing adaptation costs by 90%. Key finding: efficiency improvements no longer compromise accuracy, with several papers matching or exceeding dense baseline performance.",
    
    "synthesis_text": "### 1. Sparse Attention Mechanisms\n\nFour papers (Chen et al., 2024; Liu et al., 2023; Wang et al., 2024; Zhang et al., 2024) explored sparse attention patterns. Consistent finding: 40-50% reduction in training time while maintaining >95% accuracy. The most promising approach combines local and global attention patterns, achieving O(n√n) complexity vs O(n²) for dense attention.\n\n**Key Evidence:**\n- Chen et al.: 40% faster training, 96.3% GLUE accuracy\n- Liu et al.: 50% memory reduction for long sequences\n- Wang et al.: Scales to 100K token context windows\n\n### 2. Mixture of Experts (MoE) Architectures\n\nThree papers demonstrated MoE as the path to trillion-parameter models...",
    
    "primary_themes": [
      "Sparse attention mechanisms (4 papers): 40-50% efficiency gains",
      "Mixture of Experts architectures (3 papers): Scaling to 1T+ parameters",
      "Parameter-efficient fine-tuning (2 papers): LoRA, adapters reduce costs by 90%",
      "Long-context modeling: 100K-1M token context windows now feasible"
    ],
    
    "gaps_identified": [
      "Limited exploration of mobile/edge deployment",
      "Interpretability of sparse patterns unclear",
      "Few studies on multi-modal sparse transformers",
      "Training stability at extreme scales (>1T params) under-studied"
    ],
    
    "sources_analyzed": 9,
    "methodologies_found": 5
  },
  
  "execution_summary": {
    "total_sources_discovered": 78,
    "sources_validated": 78,
    "extractions_successful": 9
  },
  
  "audit_trail_summary": {
    "total_decisions_logged": 27,
    "full_audit_log_available": true
  }
}
```

---

## Timeline Summary

```
T+0s:     User calls /api/agent/execute
T+1s:     Agent returns job_id, starts working
T+1-15s:  Search API called 5 times → 78 papers found
T+15-20s: Batch relevance scoring → 15 papers selected
T+20-90s: Extraction API called 9 times → 9 successful extractions
T+90-120s: Gemini synthesis → Final report generated
T+120s:   Results available at /api/agent/results/{job_id}
```

**Total Time:** ~2 minutes for comprehensive research

---

## Key Integration Points

### 1. URL Flow
```
Search returns:     "url": "https://arxiv.org/abs/2401.12345"
                         ↓
Extraction receives: "source_url": "https://arxiv.org/abs/2401.12345"
                         ↓
Extraction fetches:  PDF from arXiv, parses content
```

### 2. Success Validation
```python
# Agent checks extraction success for EVERY paper:
if extraction_response["metadata"]["extraction_success"] == true:
    use_in_synthesis()
else:
    skip_paper()
```

### 3. Quality Control
- Search: Filters by relevance_score ≥ 0.6
- Extraction: Only uses papers with extraction_success = true
- Synthesis: Gemini analyzes only successfully extracted content

---

## What Makes This Work

✅ **Real URLs:** Search returns fetchable arXiv/DOI links  
✅ **Real Content:** Extraction parses actual PDFs  
✅ **Real Findings:** Extraction extracts specific results, not "Finding 1/2/3"  
✅ **Real Synthesis:** Gemini analyzes actual research patterns  

**Result:** Credible, valuable research insights in 2 minutes

---

## Testing Your Integration

### Minimal Test
```bash
# 1. Start job
JOB_ID=$(curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{"research_goal": "Recent AI trends"}' | jq -r '.job_id')

# 2. Wait
sleep 120

# 3. Get results
curl "http://localhost:8000/api/agent/results/$JOB_ID" | jq '.synthesis.primary_themes'
```

### Expected Output
```json
[
  "Machine learning interpretability (5 papers)",
  "Large language model efficiency (4 papers)",
  "Multimodal learning advances (3 papers)"
]
```

**NOT:**
```json
[
  "Themes related to methodology"  // ← Generic mock data!
]
```

---

## Success Criteria

Your integration is working when:
1. ✅ Synthesis contains specific findings with numbers
2. ✅ Primary themes reference actual paper topics
3. ✅ Sources_analyzed matches extractions_successful
4. ✅ No "Finding 1/2/3" or "Mock methodology" in output
5. ✅ Execution completes in < 3 minutes

---

**Ready to integrate!** 🚀
