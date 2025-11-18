#!/bin/bash
# Test 5 different research goals through the /execute endpoint

BASE_URL="http://localhost"

# Define 5 test inputs
declare -a GOALS=(
    "Model compression techniques for neural networks"
    "Transformer architecture improvements and optimization"
    "Knowledge distillation methods in deep learning"
    "Quantization techniques for efficient inference"
    "Neural architecture search and AutoML frameworks"
)

declare -a DEPTHS=(
    "comprehensive"
    "focused"
    "rapid"
    "exhaustive"
    "comprehensive"
)

echo "================================================================================================"
echo "PHASE 1: SUBMITTING 5 TEST INPUTS"
echo "================================================================================================"

declare -a JOB_IDS

for i in "${!GOALS[@]}"; do
    echo ""
    echo "[$(($i+1))/5] Submitting: ${GOALS[$i]}"
    
    # Create JSON payload
    PAYLOAD=$(cat <<EOF
{
    "research_goal": "${GOALS[$i]}",
    "scope_parameters": {
        "discovery_depth": "${DEPTHS[$i]}",
        "quality_threshold": {"min_citations": 5, "min_year": 2020},
        "temporal_boundary": {"start_year": 2020, "end_year": 2025}
    }
}
EOF
)
    
    # Submit request
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/agent/execute" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD")
    
    JOB_ID=$(echo "$RESPONSE" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)
    STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
    
    if [ -n "$JOB_ID" ]; then
        echo "  ✓ Job submitted successfully"
        echo "    Job ID: $JOB_ID"
        echo "    Status: $STATUS"
        JOB_IDS+=("$JOB_ID")
    else
        echo "  ✗ Error submitting request"
        echo "    Response: $RESPONSE"
    fi
done

echo ""
echo "================================================================================================"
echo "PHASE 2: POLLING FOR COMPLETION (max 3 minutes per job)"
echo "================================================================================================"

for job_id in "${JOB_IDS[@]}"; do
    echo ""
    echo "Polling: $job_id"
    
    counter=0
    max_iterations=36  # 36 * 5 seconds = 180 seconds
    
    while [ $counter -lt $max_iterations ]; do
        RESPONSE=$(curl -s "$BASE_URL/api/agent/status/$job_id")
        STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
        
        if [ "$STATUS" = "COMPLETED" ]; then
            echo "  [100%] COMPLETED"
            break
        else
            PROGRESS=$(echo "$RESPONSE" | grep -o '"progress_percentage":[0-9]*' | cut -d':' -f2)
            echo -ne "  [$PROGRESS%] $STATUS\r"
        fi
        
        ((counter++))
        sleep 5
    done
    
    if [ "$STATUS" != "COMPLETED" ]; then
        echo "  ✗ Timeout or error"
    fi
done

echo ""
echo "================================================================================================"
echo "PHASE 3: ANALYZING RESULTS"
echo "================================================================================================"

for i in "${!JOB_IDS[@]}"; do
    job_id="${JOB_IDS[$i]}"
    goal="${GOALS[$i]}"
    
    echo ""
    echo "─────────────────────────────────────────────────────────────────────────────────────────────"
    echo "ANALYSIS: $goal"
    echo "─────────────────────────────────────────────────────────────────────────────────────────────"
    
    RESPONSE=$(curl -s "$BASE_URL/api/results/$job_id")
    
    # Extract synthesis data
    echo "$RESPONSE" | python3 << 'PYTHON_ANALYSIS'
import sys
import json
import re

try:
    data = json.load(sys.stdin)
    synthesis = data.get("synthesis", {})
    
    if not synthesis:
        print("  ✗ No synthesis data available")
        sys.exit(0)
    
    # Count sections
    sections = {
        "executive_summary": synthesis.get("executive_summary", ""),
        "literature_overview": synthesis.get("literature_overview", ""),
        "methodology_analysis": synthesis.get("methodology_analysis", ""),
        "key_contributions": synthesis.get("key_contributions", ""),
        "gap_analysis": synthesis.get("gap_analysis", ""),
        "comparison_matrix": synthesis.get("comparison_matrix", ""),
        "trend_analysis": synthesis.get("trend_analysis", ""),
        "recommendations": synthesis.get("recommendations", ""),
        "paper_summaries": synthesis.get("paper_summaries", ""),
    }
    
    print("\n  Section breakdown:")
    total_words = 0
    for section_name, content in sections.items():
        word_count = len(content.split()) if content else 0
        total_words += word_count
        status = "✓" if word_count > 0 else "✗"
        print(f"    {status} {section_name:25} {word_count:6} words")
    
    print(f"\n  ─────────────────────────────────────────")
    print(f"    Total words (all sections):  {total_words:6}")
    full_syn_words = len(synthesis.get('full_synthesis', '').split())
    print(f"    Full synthesis length:       {full_syn_words:6} words")
    
    # Metadata
    papers_analyzed = synthesis.get("papers_analyzed", 0)
    primary_themes = synthesis.get("primary_themes", [])
    gaps_identified = synthesis.get("gaps_identified", [])
    
    print(f"\n  Metadata:")
    print(f"    Papers analyzed:             {papers_analyzed}")
    theme_str = ", ".join(primary_themes) if primary_themes else "None"
    print(f"    Primary themes:              {theme_str}")
    print(f"    Gaps identified:             {len(gaps_identified)} gaps")
    
except Exception as e:
    print(f"  ✗ Error analyzing: {e}")
PYTHON_ANALYSIS
    
done

echo ""
echo "================================================================================================"
echo "SUMMARY"
echo "================================================================================================"
echo "Total tests: ${#GOALS[@]}"
echo "Submitted: ${#JOB_IDS[@]}"
echo ""
echo "Job IDs:"
for job_id in "${JOB_IDS[@]}"; do
    echo "  $job_id"
done
