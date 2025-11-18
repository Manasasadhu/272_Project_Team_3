#!/usr/bin/env python3
"""Test 5 different research goals through the /execute endpoint"""
import httpx
import json
import time
from datetime import datetime

BASE_URL = "http://localhost"

# 5 diverse research goals
TEST_INPUTS = [
    {
        "research_goal": "Model compression techniques for neural networks",
        "scope_parameters": {
            "discovery_depth": "comprehensive",
            "quality_threshold": {"min_citations": 5, "min_year": 2020},
            "temporal_boundary": {"start_year": 2020, "end_year": 2025}
        }
    },
    {
        "research_goal": "Transformer architecture improvements and optimization",
        "scope_parameters": {
            "discovery_depth": "focused",
            "quality_threshold": {"min_citations": 10, "min_year": 2021},
            "temporal_boundary": {"start_year": 2021, "end_year": 2025}
        }
    },
    {
        "research_goal": "Knowledge distillation methods in deep learning",
        "scope_parameters": {
            "discovery_depth": "rapid",
            "quality_threshold": {"min_citations": 0, "min_year": 2019}
        }
    },
    {
        "research_goal": "Quantization techniques for efficient inference",
        "scope_parameters": {
            "discovery_depth": "exhaustive",
            "quality_threshold": {"min_citations": 5, "min_year": 2020}
        }
    },
    {
        "research_goal": "Neural architecture search and AutoML frameworks",
        "scope_parameters": {
            "discovery_depth": "comprehensive",
            "quality_threshold": {"min_citations": 3, "min_year": 2018}
        }
    }
]

def submit_research_goal(test_input):
    """Submit a research goal and return job_id"""
    print(f"\n{'='*80}")
    print(f"Submitting: {test_input['research_goal']}")
    print(f"{'='*80}")
    
    try:
        response = httpx.post(
            f"{BASE_URL}/api/agent/execute",
            json=test_input,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        job_id = result.get("job_id")
        status = result.get("status")
        print(f"✓ Job submitted successfully")
        print(f"  Job ID: {job_id}")
        print(f"  Status: {status}")
        return job_id
    except Exception as e:
        print(f"✗ Error submitting request: {e}")
        return None

def poll_status(job_id, max_wait=120):
    """Poll job status until completion"""
    print(f"\nPolling status for job {job_id}...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = httpx.get(
                f"{BASE_URL}/api/agent/status/{job_id}",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            status = result.get("status")
            progress = result.get("current_phase", {}).get("progress_percentage", 0)
            
            print(f"  [{progress}%] {status}", end="\r")
            
            if status == "COMPLETED":
                print(f"  [100%] COMPLETED                                      ")
                return True
        except Exception as e:
            print(f"  Error polling status: {e}")
        
        time.sleep(5)
    
    print(f"\n  Timeout waiting for completion")
    return False

def get_results(job_id):
    """Get synthesis results for a job"""
    print(f"\nFetching results for job {job_id}...")
    
    try:
        response = httpx.get(
            f"{BASE_URL}/api/results/{job_id}",
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get("synthesis", {})
    except Exception as e:
        print(f"✗ Error fetching results: {e}")
        return None

def analyze_synthesis(synthesis, goal):
    """Analyze synthesis output"""
    if not synthesis:
        print("No synthesis data available")
        return
    
    print(f"\n{'─'*80}")
    print(f"ANALYSIS: {goal}")
    print(f"{'─'*80}")
    
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
    
    # Count words per section
    print(f"\nSection breakdown:")
    total_words = 0
    for section_name, content in sections.items():
        word_count = len(content.split()) if content else 0
        total_words += word_count
        status = "✓" if word_count > 0 else "✗"
        print(f"  {status} {section_name:25} {word_count:6} words")
    
    print(f"\n{'─'*30}")
    print(f"  Total words (all sections):  {total_words:6}")
    print(f"  Full synthesis length:       {len(synthesis.get('full_synthesis', '').split()):6} words")
    
    # Metadata
    papers_analyzed = synthesis.get("papers_analyzed", 0)
    primary_themes = synthesis.get("primary_themes", [])
    gaps_identified = synthesis.get("gaps_identified", [])
    
    print(f"\nMetadata:")
    print(f"  Papers analyzed:             {papers_analyzed}")
    print(f"  Primary themes:              {', '.join(primary_themes) if primary_themes else 'None'}")
    print(f"  Gaps identified:             {len(gaps_identified)} gaps")
    if gaps_identified:
        for i, gap in enumerate(gaps_identified[:3], 1):
            print(f"    {i}. {gap[:70]}{'...' if len(gap) > 70 else ''}")

if __name__ == "__main__":
    print("Starting comprehensive pipeline tests...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    job_results = {}
    
    # Submit all 5 test inputs
    print("\n" + "="*80)
    print("PHASE 1: SUBMITTING 5 TEST INPUTS")
    print("="*80)
    
    for i, test_input in enumerate(TEST_INPUTS, 1):
        print(f"\n[{i}/5]", end=" ")
        job_id = submit_research_goal(test_input)
        if job_id:
            job_results[job_id] = {
                "goal": test_input["research_goal"],
                "submitted_at": datetime.now(),
                "status": "SUBMITTED"
            }
    
    # Poll and wait for all to complete
    print("\n" + "="*80)
    print("PHASE 2: WAITING FOR ALL JOBS TO COMPLETE")
    print("="*80)
    
    completed_jobs = {}
    for job_id, info in job_results.items():
        if poll_status(job_id, max_wait=180):
            completed_jobs[job_id] = info
            info["status"] = "COMPLETED"
    
    # Fetch results for all completed jobs
    print("\n" + "="*80)
    print("PHASE 3: ANALYZING RESULTS")
    print("="*80)
    
    for job_id, info in completed_jobs.items():
        synthesis = get_results(job_id)
        if synthesis:
            analyze_synthesis(synthesis, info["goal"])
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total tests: {len(TEST_INPUTS)}")
    print(f"Completed: {len(completed_jobs)}")
    print(f"Failed: {len(TEST_INPUTS) - len(completed_jobs)}")
    
    if completed_jobs:
        print(f"\nCompleted Job IDs:")
        for job_id, info in completed_jobs.items():
            print(f"  {job_id}: {info['goal'][:60]}")
