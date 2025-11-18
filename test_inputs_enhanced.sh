#!/bin/bash
# Enhanced test with 8 diverse research goals through the /execute endpoint

BASE_URL="http://localhost"

# Define 8 diverse test inputs
declare -a GOALS=(
    "Attention mechanisms and transformer architectures"
    "Adversarial robustness in deep learning"
    "Few-shot learning and meta-learning approaches"
    "Federated learning and privacy-preserving machine learning"
    "Vision transformers and their applications"
    "Reinforcement learning for robotics"
    "Neural network interpretability and explainability"
    "Graph neural networks and their variants"
)

declare -a DEPTHS=(
    "comprehensive"
    "focused"
    "rapid"
    "exhaustive"
    "comprehensive"
    "focused"
    "rapid"
    "comprehensive"
)

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║           ENHANCED PIPELINE TEST - 8 DIVERSE RESEARCH GOALS                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "================================================================================================"
echo "PHASE 1: SUBMITTING 8 TEST INPUTS"
echo "================================================================================================"

declare -a JOB_IDS

for i in "${!GOALS[@]}"; do
    idx=$((i+1))
    echo ""
    echo "[$idx/8] Submitting: ${GOALS[$i]}"
    
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
        echo "  ✓ Job submitted"
        echo "    Job ID: $JOB_ID"
        echo "    Status: $STATUS"
        JOB_IDS+=("$JOB_ID")
    else
        echo "  ✗ Error submitting request"
    fi
    
    sleep 1
done

echo ""
echo "================================================================================================"
echo "PHASE 2: WAITING FOR ALL JOBS TO COMPLETE (max 2 minutes per job)"
echo "================================================================================================"

COMPLETED_JOBS=()
for i in "${!JOB_IDS[@]}"; do
    job_id="${JOB_IDS[$i]}"
    idx=$((i+1))
    echo ""
    echo "[$idx/8] Polling: $job_id"
    
    counter=0
    max_iterations=24  # 24 * 5 seconds = 120 seconds
    
    while [ $counter -lt $max_iterations ]; do
        RESPONSE=$(curl -s "$BASE_URL/api/agent/status/$job_id")
        STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
        
        if [ "$STATUS" = "COMPLETED" ]; then
            echo "  ✓ [100%] COMPLETED"
            COMPLETED_JOBS+=("$job_id")
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
echo ""
echo "================================================================================================"
echo "PHASE 3: ANALYZING RESULTS FOR COMPLETED JOBS"
echo "================================================================================================"

for i in "${!COMPLETED_JOBS[@]}"; do
    job_id="${COMPLETED_JOBS[$i]}"
    goal_idx=$(printf '%d\n' "${!JOB_IDS[@]}" | grep -n "$job_id" | cut -d: -f1)
    goal_idx=$((goal_idx-1))
    goal="${GOALS[$goal_idx]}"
    idx=$((i+1))
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────────────────────────────────────┐"
    echo "│ JOB $idx: $goal"
    echo "│ ID: $job_id"
    echo "└─────────────────────────────────────────────────────────────────────────────────────────────┘"
    
    RESPONSE=$(curl -s "$BASE_URL/api/agent/results/$job_id")
    
    # Extract synthesis data using Python
    echo "$RESPONSE" | python3 << PYTHON_ANALYSIS
import sys, json, re

try:
    data = json.load(sys.stdin)
    synthesis = data.get("synthesis", {})
    
    if not synthesis:
        print("  ERROR: No synthesis data available")
        sys.exit(0)
    
    # Count sections
    sections = {
        "executive_summary": synthesis.get("executive_summary", ""),
        "literature_overview": synthesis.get("literature_overview", ""),
        "methodology_analysis": synthesis.get("methodology_analysis", ""),
        "key_contributions": synthesis.get("key_contributions", ""),
        "gap_analysis": synthesis.get("gap_analysis", ""),
        "comparison_matrix": synthesis.get("comparison_matrix", ""),
        "performance_analysis": synthesis.get("performance_analysis", ""),
        "critical_analysis": synthesis.get("critical_analysis", ""),
        "case_studies": synthesis.get("case_studies", ""),
        "trend_analysis": synthesis.get("trend_analysis", ""),
        "recommendations": synthesis.get("recommendations", ""),
        "paper_summaries": synthesis.get("paper_summaries", ""),
    }
    
    print("  Section Breakdown:")
    print("  " + "-" * 87)
    total_words = 0
    for section_name, content in sections.items():
        word_count = len(content.split()) if content else 0
        total_words += word_count
        status = "OK" if word_count > 0 else "X "
        is_new = section_name in ["performance_analysis", "critical_analysis", "case_studies"]
        marker = "[NEW]" if is_new else "     "
        print(f"    {status} {marker} {section_name:30} {word_count:6} words")
    
    print("  " + "=" * 87)
    full_syn_words = len(synthesis.get("full_synthesis", "").split())
    print(f"    Total (all sections):              {total_words:6} words")
    print(f"    Full synthesis document:           {full_syn_words:6} words")
    
    # Metadata
    papers_analyzed = synthesis.get("papers_analyzed", 0)
    primary_themes = synthesis.get("primary_themes", [])
    gaps_identified = synthesis.get("gaps_identified", [])
    
    print()
    print("  Analysis Metrics:")
    print("  " + "-" * 87)
    print(f"    Papers analyzed:                   {papers_analyzed:6}")
    print(f"    Primary themes:                    {len(primary_themes):6}")
    if primary_themes:
        theme_str = ", ".join(primary_themes[:3])
        print(f"      Themes: {theme_str}")
    print(f"    Research gaps identified:          {len(gaps_identified):6}")
    
    # Execution summary
    exec_summary = data.get("execution_summary", {})
    print()
    print("  Execution Summary:")
    print("  " + "-" * 87)
    print(f"    Sources discovered:                {exec_summary.get('total_sources_discovered', 0):6}")
    print(f"    Sources validated:                 {exec_summary.get('sources_validated', 0):6}")
    print(f"    Extractions successful:            {exec_summary.get('extractions_successful', 0):6}")
    
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

PYTHON_ANALYSIS
    
done

echo ""
echo ""
echo "================================================================================================"
echo "PHASE 4: CROSS-JOB ANALYSIS AND COMPARISON"
echo "================================================================================================"

# Fetch all results and compare
echo ""
echo "Analyzing patterns across all ${#COMPLETED_JOBS[@]} completed jobs..."
echo ""

python3 << 'CROSS_ANALYSIS'
import sys, json, re
import subprocess
from collections import defaultdict

# Fetch all results
jobs_data = []
BASE_URL = "http://localhost"

job_ids = sys.argv[1:]

for job_id in job_ids:
    try:
        response = subprocess.run(
            ["curl", "-s", f"{BASE_URL}/api/agent/results/{job_id}"],
            capture_output=True,
            text=True
        )
        data = json.loads(response.stdout)
        synthesis = data.get("synthesis", {})
        exec_summary = data.get("execution_summary", {})
        
        jobs_data.append({
            "job_id": job_id,
            "synthesis": synthesis,
            "exec_summary": exec_summary
        })
    except Exception as e:
        print(f"Error fetching {job_id}: {e}")

# Calculate statistics
print("  CROSS-JOB STATISTICS:")
print("  " + "-" * 87)

total_papers = sum(j["synthesis"].get("papers_analyzed", 0) for j in jobs_data)
total_words = sum(len(j["synthesis"].get("full_synthesis", "").split()) for j in jobs_data)
avg_words_per_job = total_words // len(jobs_data) if jobs_data else 0

print(f"    Total papers analyzed across all jobs:    {total_papers:6}")
print(f"    Total synthesis words generated:          {total_words:6}")
print(f"    Average words per job:                    {avg_words_per_job:6}")
print(f"    Jobs completed successfully:              {len(jobs_data):6}")
print()

# Min/Max analysis
word_counts = [len(j["synthesis"].get("full_synthesis", "").split()) for j in jobs_data]
if word_counts:
    print(f"    Min synthesis:                           {min(word_counts):6} words")
    print(f"    Max synthesis:                           {max(word_counts):6} words")
    print(f"    Avg synthesis:                           {sum(word_counts)//len(word_counts):6} words")
print()

# Theme analysis
all_themes = defaultdict(int)
all_gaps = defaultdict(int)

for job in jobs_data:
    themes = job["synthesis"].get("primary_themes", [])
    gaps = job["synthesis"].get("gaps_identified", [])
    
    for theme in themes:
        all_themes[theme] += 1
    for gap in gaps:
        all_gaps[gap] += 1

print("  TOP THEMES ACROSS ALL JOBS:")
print("  " + "-" * 87)
sorted_themes = sorted(all_themes.items(), key=lambda x: x[1], reverse=True)[:5]
for theme, count in sorted_themes:
    print(f"    • {theme:40} {count:2} jobs")
print()

print("  SYNTHESIS QUALITY DISTRIBUTION:")
print("  " + "-" * 87)
under_1000 = len([w for w in word_counts if w < 1000])
between_1000_2000 = len([w for w in word_counts if 1000 <= w < 2000])
between_2000_3000 = len([w for w in word_counts if 2000 <= w < 3000])
over_3000 = len([w for w in word_counts if w >= 3000])

print(f"    < 1,000 words:                           {under_1000:2} jobs")
print(f"    1,000-2,000 words:                       {between_1000_2000:2} jobs")
print(f"    2,000-3,000 words:                       {between_2000_3000:2} jobs")
print(f"    > 3,000 words:                           {over_3000:2} jobs")

CROSS_ANALYSIS "${COMPLETED_JOBS[@]}"

echo ""
echo "================================================================================================"
echo "SUMMARY"
echo "================================================================================================"
echo "  Test execution completed!"
echo "  Total jobs submitted:          ${#JOB_IDS[@]}"
echo "  Jobs completed successfully:   ${#COMPLETED_JOBS[@]}"
echo "  Jobs failed:                   $((${#JOB_IDS[@]} - ${#COMPLETED_JOBS[@]}))"
echo ""
echo "  Completed Job IDs:"
for job_id in "${COMPLETED_JOBS[@]}"; do
    echo "    • $job_id"
done
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ TEST EXECUTION COMPLETE                                 ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
