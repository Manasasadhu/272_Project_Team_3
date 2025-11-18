"""Goal planner"""
from typing import List, Dict, Any
from infrastructure.llm_client import LLMClient
from infrastructure.config import config
# Note: ScopeParameters passed as dict

class Planner:
    """Goal decomposition and planning"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def decompose_goal(self, research_goal: str, scope_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Decompose research goal into execution plan"""
        
        # Get max sources from scope params
        max_sources = 30
        if scope_params and scope_params.get("discovery_depth"):
            depth_map = {
                "rapid": 10,
                "focused": 15,
                "comprehensive": 30,
                "exhaustive": 50
            }
            max_sources = depth_map.get(scope_params["discovery_depth"], 30)
        
        # Generate search queries - IMPROVED fallback to heuristic decomposition
        # (LLM sometimes fails, so we have a deterministic fallback)
        prompt = f"""Decompose this research goal into 3-5 specific search queries for academic literature:
        
Goal: {research_goal}

Generate specific search queries that will find relevant academic papers. Return only a JSON array of query strings.

Example format: ["query 1", "query 2", "query 3"]
"""
        
        queries = None
        try:
            queries_json = self.llm_client.generate_json(prompt, temperature=0.7)
            queries = queries_json if isinstance(queries_json, list) else queries_json.get("queries", [])
            if queries and len(queries) > 0 and isinstance(queries[0], str):
                # Validate we got real queries, not empty/malformed
                queries = [q for q in queries if q and len(q.strip()) > 5]
        except Exception as e:
            queries = None
        
        # If LLM failed or returned empty, use smart heuristic decomposition
        if not queries or len(queries) == 0:
            queries = self._decompose_goal_heuristic(research_goal)
        
        # Create execution plan
        plan = {
            "search_queries": queries[:5],  # Limit to 5 queries
            "max_sources": max_sources,
            "phases": [
                {
                    "phase": "Autonomous Exploration",
                    "description": f"Execute {len(queries)} search queries to discover relevant sources",
                    "estimated_sources": max_sources * 2
                },
                {
                    "phase": "Intelligent Validation",
                    "description": "Apply governance rules to filter and validate sources",
                    "expected_acceptance_rate": "60-70%"
                },
                {
                    "phase": "Structured Extraction",
                    "description": "Extract structured data from validated sources",
                    "target_extraction_rate": ">95%"
                },
                {
                    "phase": "Emergent Synthesis",
                    "description": "Perform meta-analysis with gap identification"
                }
            ]
        }
        
        return plan
    
    def _decompose_goal_heuristic(self, research_goal: str) -> List[str]:
        """Smart heuristic decomposition when LLM fails
        
        Generates varied search queries without relying on LLM
        """
        goal = research_goal.lower().strip()
        queries = []
        
        # Query 1: Full goal as-is (most specific)
        queries.append(research_goal)
        
        # Query 2: Goal + "recent" (temporal variant)
        queries.append(f"recent {research_goal}")
        
        # Query 3: Extract key terms and search for first N words
        # This helps with compound goals like "pruning and quantization techniques"
        key_terms = goal.split()[:3]  # First 3 words usually most specific
        if len(key_terms) > 0:
            queries.append(" ".join(key_terms))
        
        # Query 4: Add "machine learning" or domain context if not already present
        if "machine learning" not in goal and "neural" not in goal and "deep" not in goal:
            queries.append(f"{research_goal} machine learning")
        else:
            # If already ML-focused, search for "survey" or "review" variant
            queries.append(f"{research_goal} survey")
        
        # Query 5: Technical variant - replace generic terms with specific ones
        # E.g., "techniques" -> "methods", "improvements" -> "optimization"
        technical_query = goal.replace("techniques", "methods")
        technical_query = technical_query.replace("improvements", "optimization")
        technical_query = technical_query.replace("advances", "breakthroughs")
        if technical_query != goal:
            queries.append(technical_query)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            if q not in seen and len(q.strip()) > 5:
                seen.add(q)
                unique_queries.append(q)
        
        return unique_queries[:5]  # Return up to 5 queries


