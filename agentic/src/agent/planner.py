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
        Improves upon naive approach by extracting technical keywords
        """
        goal = research_goal.lower().strip()
        queries = []
        
        # Noise words that typically don't help academic searches
        noise_words = {
            'find', 'analyze', 'papers', 'on', 'about', 'what', 'is', 'the',
            'for', 'and', 'or', 'a', 'an', 'this', 'that', 'would', 'like',
            'to', 'know', 'of', 'previous', 'i', 'you', 'we', 'they', 'it',
            'get', 'set', 'see', 'make', 'do', 'have', 'be', 'help', 'give',
            'research', 'study', 'review', 'explore', 'investigate', 'examine'
        }
        
        # Extract key technical terms (words that aren't noise words and are longer)
        words = goal.split()
        key_terms = [w for w in words if w not in noise_words and len(w.strip()) > 2]
        
        if not key_terms:
            # Fallback: use all non-noise words if we have no key terms
            key_terms = [w for w in words if len(w.strip()) > 2]
        
        if not key_terms:
            # Last resort: use original goal
            key_terms = words
        
        # Query 1: Just the key technical terms (most effective for OpenAlex)
        if key_terms:
            queries.append(" ".join(key_terms[:6]))  # First 6 key terms
        
        # Query 2: Key terms + "survey" or "review" (often returns good survey papers)
        if key_terms:
            survey_query = " ".join(key_terms[:4]) + " survey"
            queries.append(survey_query)
        
        # Query 3: Key terms + domain context if not already present
        if key_terms:
            combined = " ".join(key_terms)
            # Check if research domain is already evident in key terms
            ml_indicators = {'learning', 'neural', 'deep', 'model', 'network', 'ai', 'llm', 'agent'}
            has_ml_context = any(term in combined for term in ml_indicators)
            
            if not has_ml_context and "routing" not in combined and "protocol" not in combined:
                # Add machine learning context if not present
                queries.append(combined + " learning")
            else:
                # Alternative: try first 3 key terms with different combination
                if len(key_terms) > 1:
                    queries.append(" ".join(key_terms[:3]))
        
        # Query 4: Individual key terms (broader search with primary topic)
        if len(key_terms) > 1:
            # Use the first and most important-seeming term
            primary_term = key_terms[0]
            if len(key_terms) > 1:
                # Find term that's not too short (likely more specific)
                primary_term = max(key_terms[:3], key=len)
            queries.append(primary_term)
        
        # Query 5: Compound key terms (2-3 most specific terms)
        if len(key_terms) >= 2:
            # Sort by length descending (longer = more specific terms usually)
            sorted_terms = sorted(key_terms, key=len, reverse=True)
            queries.append(" ".join(sorted_terms[:3]))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            q_stripped = q.strip()
            # Only include queries that have actual content (not just noise)
            if q_stripped not in seen and len(q_stripped) > 2:
                # Verify it has at least one non-noise word
                q_words = set(q_stripped.lower().split())
                if not q_words.issubset(noise_words):  # Has at least one good word
                    seen.add(q_stripped)
                    unique_queries.append(q_stripped)
        
        return unique_queries[:5]  # Return up to 5 queries


