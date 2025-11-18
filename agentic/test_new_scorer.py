#!/usr/bin/env python3
"""Test the new dynamic semantic scorer against real papers

This script:
1. Calls the search API for both test queries
2. Fetches papers from the results
3. Generates semantic groups dynamically
4. Scores papers using the new scorer
5. Reports acceptance rate and efficiency metrics
"""

import sys
import json
import requests
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from governance.relevance_scorer import RelevanceScorer
from governance.semantic_groups_generator import SemanticGroupsGenerator
from infrastructure.llm_client import LLMClient
from infrastructure.logging_setup import logger

# Test queries
QUERIES = {
    "routing": "I would like to know about the previous papers of RIP and OSPF routing protocols",
    "agentic": "I want papers on agentic AI and reasoning capabilities"
}

SEARCH_API_URL = "http://localhost:9000/api/search"  # Backend search API (port 9000)
PAPERS_PER_QUERY = 50  # Get first 50 papers per query


def search_papers(query: str, limit: int = 50) -> list:
    """Call backend search API to get papers"""
    try:
        payload = {
            "query": query,
            "limit": limit
        }
        
        print(f"\n🔍 Searching for: '{query}'")
        response = requests.post(SEARCH_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        papers = data.get("results", [])
        
        print(f"   Found: {len(papers)} papers")
        return papers
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []


def score_papers(papers: list, research_goal: str, semantic_groups: dict) -> dict:
    """Score papers using the new dynamic semantic scorer
    
    Returns:
        {
            "papers_scored": int,
            "papers_passing": int,
            "acceptance_rate": float (0-100),
            "scores": [list of (title, score, passed)],
            "threshold": float,
            "score_distribution": {}
        }
    """
    if not papers:
        return {"papers_scored": 0, "papers_passing": 0}
    
    # Create scorer with dynamic semantic groups
    scorer = RelevanceScorer(
        logger=logger,
        llm_client=None,
        semantic_groups=semantic_groups
    )
    
    # Score all papers
    scores = scorer.batch_score(papers, research_goal, verbose=False)
    
    # Calculate dynamic threshold
    max_score = max(scores) if scores else 0
    if max_score < 0.45:
        threshold = 0.20
    elif max_score < 0.60:
        threshold = 0.25
    else:
        threshold = 0.35
    
    # Analyze results
    passing_papers = []
    failing_papers = []
    
    for i, paper in enumerate(papers):
        if i < len(scores):
            score = scores[i]
            title = paper.get('title', 'Unknown')[:70]
            
            if score >= threshold:
                passing_papers.append((title, score, True))
            else:
                failing_papers.append((title, score, False))
    
    acceptance_rate = (len(passing_papers) / len(papers) * 100) if papers else 0
    
    # Score distribution
    score_dist = {
        "min": f"{min(scores):.3f}" if scores else "N/A",
        "max": f"{max(scores):.3f}" if scores else "N/A",
        "avg": f"{sum(scores)/len(scores):.3f}" if scores else "N/A",
        "threshold": f"{threshold:.3f}"
    }
    
    return {
        "papers_scored": len(papers),
        "papers_passing": len(passing_papers),
        "papers_failing": len(failing_papers),
        "acceptance_rate": acceptance_rate,
        "threshold": threshold,
        "score_distribution": score_dist,
        "passing_papers": passing_papers,
        "failing_papers": failing_papers[:5]  # Show first 5 failing
    }


def generate_semantic_groups(research_goal: str) -> dict:
    """Generate semantic groups using LLM"""
    try:
        llm_client = LLMClient(logger=logger)
        gen = SemanticGroupsGenerator(llm_client=llm_client, logger=logger)
        
        print(f"   Generating semantic groups...")
        groups = gen.generate_groups(research_goal)
        
        print(f"   Generated {len(groups)} semantic groups:")
        for core, variants in list(groups.items())[:5]:
            print(f"     • {core}: {variants[:3]}")
        if len(groups) > 5:
            print(f"     ... and {len(groups)-5} more")
        
        return groups
        
    except Exception as e:
        print(f"⚠️  Failed to generate semantic groups: {e}")
        print(f"   Using empty groups (pure prefix matching)")
        return {}


def print_results(query_name: str, research_goal: str, result: dict):
    """Pretty print test results"""
    
    print(f"\n{'='*80}")
    print(f"📊 TEST RESULTS: {query_name.upper()}")
    print(f"{'='*80}")
    print(f"Query: {research_goal}")
    print(f"\n📈 SCORING RESULTS:")
    print(f"   Papers Scored:      {result.get('papers_scored', 0)}")
    print(f"   Papers Passing:     {result.get('papers_passing', 0)}")
    print(f"   Papers Failing:     {result.get('papers_failing', 0)}")
    
    acceptance_rate = result.get('acceptance_rate', 0)
    print(f"   ✅ Acceptance Rate:  {acceptance_rate:.1f}%")
    
    print(f"\n📊 SCORE DISTRIBUTION:")
    dist = result.get('score_distribution', {})
    print(f"   Min Score:  {dist.get('min', 'N/A')}")
    print(f"   Max Score:  {dist.get('max', 'N/A')}")
    print(f"   Avg Score:  {dist.get('avg', 'N/A')}")
    print(f"   Threshold:  {dist.get('threshold', 'N/A')} (dynamic)")
    
    # Show passing papers
    passing = result.get('passing_papers', [])
    if passing:
        print(f"\n✅ TOP PASSING PAPERS ({len(passing)} total):")
        for title, score, _ in passing[:5]:
            print(f"   • [{score:.3f}] {title}...")
        if len(passing) > 5:
            print(f"   ... and {len(passing)-5} more")
    
    # Show failing papers
    failing = result.get('failing_papers', [])
    if failing:
        print(f"\n❌ SAMPLE FAILING PAPERS:")
        for title, score, _ in failing[:3]:
            print(f"   • [{score:.3f}] {title}...")


def main():
    print("🚀 TESTING NEW DYNAMIC SEMANTIC SCORER")
    print("="*80)
    
    results = {}
    
    for query_name, research_goal in QUERIES.items():
        print(f"\n\n{'='*80}")
        print(f"TEST: {query_name.upper()}")
        print(f"{'='*80}")
        
        # Step 1: Search for papers
        papers = search_papers(research_goal, PAPERS_PER_QUERY)
        if not papers:
            print(f"❌ No papers found for {query_name}")
            continue
        
        # Step 2: Generate semantic groups
        semantic_groups = generate_semantic_groups(research_goal)
        
        # Step 3: Score papers
        print(f"\n   Scoring {len(papers)} papers...")
        result = score_papers(papers, research_goal, semantic_groups)
        
        # Step 4: Print results
        print_results(query_name, research_goal, result)
        
        results[query_name] = result
    
    # Summary comparison
    print(f"\n\n{'='*80}")
    print(f"📊 SUMMARY COMPARISON")
    print(f"{'='*80}")
    
    if results:
        for query_name, result in results.items():
            acceptance = result.get('acceptance_rate', 0)
            passing = result.get('papers_passing', 0)
            total = result.get('papers_scored', 0)
            print(f"\n{query_name.upper():15} | Papers: {total:3} | Passing: {passing:3} | Acceptance: {acceptance:6.1f}%")
    
    print(f"\n✅ Testing complete!")
    
    # Return exit code based on results
    # Success if at least one query has >0 papers passing
    if any(r.get('papers_passing', 0) > 0 for r in results.values()):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
