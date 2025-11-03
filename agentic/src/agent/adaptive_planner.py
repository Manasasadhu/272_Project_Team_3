"""Adaptive planner that learns from memory"""
from typing import Dict, Any, Optional
from infrastructure.llm_client import LLMClient
from infrastructure.agent_memory import AgentMemory
from agent.planner import Planner

class AdaptivePlanner(Planner):
    """Planner that uses memory to improve planning"""
    
    def __init__(self, llm_client: LLMClient, memory: AgentMemory):
        super().__init__(llm_client)
        self.memory = memory
    
    def decompose_goal(self, research_goal: str, scope_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Decompose goal using learned patterns"""
        
        # Try to get effective patterns from memory
        learned_patterns = self.memory.get_effective_search_patterns(research_goal, limit=3)
        
        # Extract domain/keywords from goal
        domain_keywords = self._extract_domain_keywords(research_goal)
        domain_knowledge = None
        if domain_keywords:
            domain_knowledge = self.memory.get_domain_knowledge(domain_keywords[0])
        
        # Build enhanced prompt with learned patterns
        prompt = self._build_enhanced_prompt(research_goal, learned_patterns, domain_knowledge)
        
        # Generate queries using LLM
        try:
            queries_json = self.llm_client.generate_json(prompt, temperature=0.7)
            queries = queries_json if isinstance(queries_json, list) else queries_json.get("queries", [])
        except:
            # Fallback: use learned patterns if available
            if learned_patterns:
                queries = [p.get("query", "") for p in learned_patterns[:3]]
            else:
                queries = self._generate_fallback_queries(research_goal)
        
        # Get max sources
        max_sources = 30
        if scope_params and scope_params.get("discovery_depth"):
            depth_map = {
                "rapid": 10,
                "focused": 15,
                "comprehensive": 30,
                "exhaustive": 50
            }
            max_sources = depth_map.get(scope_params["discovery_depth"], 30)
        
        plan = {
            "search_queries": queries[:5],
            "max_sources": max_sources,
            "phases": [
                {
                    "phase": "Autonomous Exploration",
                    "description": f"Execute {len(queries)} search queries with learned patterns",
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
            ],
            "learned_patterns_used": len(learned_patterns),
            "domain_knowledge_used": domain_knowledge is not None
        }
        
        return plan
    
    def _extract_domain_keywords(self, research_goal: str) -> list:
        """Extract domain keywords from research goal"""
        # Simple keyword extraction
        keywords = []
        common_domains = ["blockchain", "machine learning", "distributed", "consensus", 
                         "federated", "privacy", "security", "scalability"]
        goal_lower = research_goal.lower()
        for domain in common_domains:
            if domain in goal_lower:
                keywords.append(domain)
        return keywords
    
    def _build_enhanced_prompt(self, research_goal: str, learned_patterns: list, 
                               domain_knowledge: Optional[Dict]) -> str:
        """Build prompt enhanced with learned knowledge"""
        base_prompt = f"""Decompose this research goal into 3-5 specific search queries for academic literature:

Goal: {research_goal}
"""
        
        if learned_patterns:
            patterns_text = "\n".join([
                f"- {p.get('query')} (Success rate: {p.get('success_rate', 0):.1%})"
                for p in learned_patterns[:3]
            ])
            base_prompt += f"""
Consider these effective query patterns from past executions:
{patterns_text}
"""
        
        if domain_knowledge:
            themes = ", ".join(domain_knowledge.get("key_themes", [])[:3])
            base_prompt += f"""
Domain context: Key themes include {themes}
"""
        
        base_prompt += "\nGenerate specific search queries. Return only a JSON array of query strings."
        return base_prompt
    
    def _generate_fallback_queries(self, research_goal: str) -> list:
        """Generate fallback queries"""
        return [
            f"{research_goal} academic research",
            f"recent advances in {research_goal}",
            f"{research_goal} methodology"
        ]
    
    def record_success(self, research_goal: str, queries: list, metrics: Dict[str, Any]):
        """Record successful execution for learning"""
        for query in queries:
            self.memory.save_search_pattern(query, {
                "success_rate": metrics.get("validation_rate", 0),
                "quality_score": metrics.get("avg_quality", 0),
                "avg_sources": metrics.get("sources_per_query", 0)
            })

