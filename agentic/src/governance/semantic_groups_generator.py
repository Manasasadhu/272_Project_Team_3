"""Generate dynamic semantic keyword groups from research goal using LLM

Instead of hardcoding synonym groups, use LLM to generate them ONCE per research goal.
This makes the system domain-agnostic and fully dynamic.
"""
import json
from typing import Dict, List, Any, Optional
from infrastructure.llm_client import LLMClient


class SemanticGroupsGenerator:
    """Generate semantic keyword groups dynamically from research goals"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        self.llm_client = llm_client
        self.logger = logger
        self.cache = {}  # Cache generated groups to avoid redundant LLM calls
    
    def generate_groups(self, research_goal: str) -> Dict[str, List[str]]:
        """Generate semantic keyword groups from research goal
        
        **Uses LLM ONCE** to extract core concepts and their variations
        
        Args:
            research_goal: The research goal string
            
        Returns:
            Dictionary mapping core term → list of semantic variants
            {
                "agentic": ["agents", "autonomous", "agent-based"],
                "reasoning": ["inference", "logic", "deduction"],
                "planning": ["orchestration", "scheduler", "planner"]
            }
        """
        # Check cache first
        cache_key = research_goal.lower().strip()
        if cache_key in self.cache:
            if self.logger:
                self.logger.debug(f"[SEMANTIC GROUPS] Using cached groups for: {research_goal[:50]}...")
            return self.cache[cache_key]
        
        prompt = f"""Extract semantic keyword groups from this research goal.

Research Goal: {research_goal}

For each core concept, provide 3-5 semantic variants and related terms.

Return JSON with structure:
{{
  "groups": [
    {{"core": "concept1", "variants": ["variant1", "variant2", "variant3"]}},
    {{"core": "concept2", "variants": ["variant1", "variant2"]}}
  ]
}}

IMPORTANT:
- Focus on core technical concepts (agents, reasoning, planning, etc.)
- Include synonyms, abbreviations, related terms
- Keep variants lowercase and concise
- Return ONLY valid JSON, no explanations
- At least 3 groups, maximum 8 groups
- At least 2 variants per group, maximum 5

Example:
Research Goal: "agentic AI and reasoning"
{{
  "groups": [
    {{"core": "agentic", "variants": ["agents", "autonomous", "agent-based", "ai"]}},
    {{"core": "reasoning", "variants": ["inference", "logic", "deduction", "thinking"]}},
    {{"core": "language", "variants": ["llm", "nlp", "text", "model"]}}
  ]
}}
"""
        
        try:
            # Call LLM to generate groups
            response = self.llm_client.generate_json(prompt, temperature=0.5, max_tokens=500)
            
            # Parse response
            if isinstance(response, dict) and "groups" in response:
                groups_list = response["groups"]
            elif isinstance(response, list):
                groups_list = response
            else:
                if self.logger:
                    self.logger.warning(f"Unexpected response format: {type(response)}")
                return self._fallback_groups(research_goal)
            
            # Convert list of {core, variants} to flat dictionary
            semantic_groups = {}
            for group in groups_list:
                if isinstance(group, dict) and "core" in group and "variants" in group:
                    core = group["core"].lower().strip()
                    variants = [v.lower().strip() for v in group["variants"] if isinstance(v, str)]
                    semantic_groups[core] = variants
            
            if not semantic_groups:
                if self.logger:
                    self.logger.warning(f"LLM returned empty groups, using fallback")
                return self._fallback_groups(research_goal)
            
            # Cache result
            self.cache[cache_key] = semantic_groups
            
            if self.logger:
                self.logger.info(f"[SEMANTIC GROUPS] Generated {len(semantic_groups)} groups from goal")
                for core, variants in list(semantic_groups.items())[:5]:  # Log first 5
                    self.logger.debug(f"  {core}: {variants}")
            
            return semantic_groups
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to generate semantic groups: {e}. Using fallback.")
            return self._fallback_groups(research_goal)
    
    def _fallback_groups(self, research_goal: str) -> Dict[str, List[str]]:
        """Fallback: Extract groups heuristically if LLM fails
        
        Extracts key terms from research goal and provides basic variants
        """
        goal_lower = research_goal.lower()
        groups = {}
        
        # Common technical term patterns with fallback variants
        patterns = {
            'agent': ['agents', 'autonomous', 'multi-agent', 'agentic'],
            'reasoning': ['inference', 'logic', 'thinking', 'cognition'],
            'planning': ['orchestration', 'scheduler', 'coordination', 'strategy'],
            'language': ['nlp', 'llm', 'text', 'model', 'transformer'],
            'learning': ['train', 'training', 'optimization', 'adaptation'],
            'routing': ['route', 'protocol', 'gateway', 'ospf', 'bgp'],
            'synthesis': ['aggregate', 'combine', 'merge', 'fusion'],
            'retrieval': ['search', 'lookup', 'query', 'fetch'],
        }
        
        # Check which patterns appear in goal
        for core, variants in patterns.items():
            if core in goal_lower or any(v in goal_lower for v in variants):
                groups[core] = variants
        
        # If no patterns matched, extract individual keywords
        if not groups:
            words = goal_lower.split()
            # Filter to 3+ char words that might be technical terms
            candidates = [w for w in words if len(w) >= 3 and w not in {
                'the', 'and', 'for', 'with', 'are', 'from', 'that', 'this', 'have'
            }]
            for word in candidates[:3]:  # Limit to first 3
                groups[word] = [word, f"{word}s", f"{word}ing"]
        
        if self.logger:
            self.logger.info(f"[SEMANTIC GROUPS] Fallback: Generated {len(groups)} groups")
        
        return groups
    
    def merge_groups(self, *group_lists) -> Dict[str, List[str]]:
        """Merge multiple semantic group dictionaries
        
        Useful for combining groups from multiple search queries
        """
        merged = {}
        for groups in group_lists:
            if isinstance(groups, dict):
                for core, variants in groups.items():
                    if core not in merged:
                        merged[core] = []
                    # Avoid duplicates
                    merged[core] = list(set(merged[core] + variants))
        return merged
