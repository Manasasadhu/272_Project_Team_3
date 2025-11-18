"""Synthesis service"""
from typing import List, Dict, Any
from infrastructure.llm_client import LLMClient
from services.advanced_synthesizer import AdvancedSynthesizer

class SynthesisService:
    """Final synthesis and meta-analysis"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        # Use advanced synthesizer (non-LLM) for comprehensive synthesis
        self.advanced_synthesizer = AdvancedSynthesizer()
    
    def synthesize(self, research_goal: str, extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive synthesis using advanced non-LLM approach
        
        Generates 1500+ word synthesis with per-paper analysis and detailed methodology
        """
        
        if not extractions:
            return {
                "research_goal": research_goal,
                "executive_summary": "No sources were successfully extracted.",
                "primary_themes": [],
                "gaps_identified": [],
                "full_synthesis": "Insufficient data for synthesis.",
                "synthesis_method": "advanced_synthesizer",
                "papers_analyzed": 0
            }
        
        # Use advanced synthesizer for comprehensive synthesis
        synthesis_output = self.advanced_synthesizer.synthesize(extractions, research_goal)
        
        return synthesis_output

