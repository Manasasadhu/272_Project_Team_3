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
        
        # Generate search queries using LLM
        prompt = f"""Decompose this research goal into 3-5 specific search queries for academic literature:
        
Goal: {research_goal}

Generate specific search queries that will find relevant academic papers. Return only a JSON array of query strings.

Example format: ["query 1", "query 2", "query 3"]
"""
        
        try:
            queries_json = self.llm_client.generate_json(prompt, temperature=0.7)
            queries = queries_json if isinstance(queries_json, list) else queries_json.get("queries", [])
        except:
            # Fallback queries
            queries = [
                f"{research_goal} academic research",
                f"recent advances in {research_goal}",
                f"{research_goal} methodology"
            ]
        
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

