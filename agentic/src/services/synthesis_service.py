"""Synthesis service"""
from typing import List, Dict, Any
from infrastructure.llm_client import LLMClient

class SynthesisService:
    """Final synthesis and meta-analysis"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def synthesize(self, research_goal: str, extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform meta-analysis and generate synthesis"""
        
        if not extractions:
            return {
                "research_goal": research_goal,
                "executive_summary": "No sources were successfully extracted.",
                "primary_themes": [],
                "gaps_identified": [],
                "synthesis_text": "Insufficient data for synthesis."
            }
        
        # Prepare extraction summary
        methodologies = [e.get("methodology", "") for e in extractions]
        findings = []
        for e in extractions:
            findings.extend(e.get("key_findings", []))
        
        limitations = []
        for e in extractions:
            limitations.extend(e.get("limitations", []))
        
        # Generate synthesis using LLM
        prompt = f"""Perform a meta-analysis on the following research extractions and create a comprehensive synthesis.

Research Goal: {research_goal}

Extracted Data from {len(extractions)} sources:
Methodologies: {', '.join(methodologies[:5])}
Key Findings: {', '.join(findings[:10])}
Limitations: {', '.join(limitations[:10])}

Generate a synthesis that:
1. Identifies primary research themes
2. Highlights common methodologies
3. Detects conflicting approaches
4. Identifies research gaps
5. Suggests future directions

Provide a comprehensive, well-structured analysis.
"""
        
        try:
            synthesis_text = self.llm_client.generate_completion(prompt, temperature=0.7, max_tokens=2000)
        except Exception as e:
            from infrastructure.logging_setup import logger
            logger.error(f"Synthesis LLM call failed: {type(e).__name__}: {e}")
            synthesis_text = f"Based on analysis of {len(extractions)} sources, this research area shows significant activity with multiple methodological approaches."
        
        # Generate themes (simple extraction)
        themes = self._extract_themes(synthesis_text)
        gaps = self._extract_gaps(synthesis_text, limitations)
        
        return {
            "research_goal": research_goal,
            "executive_summary": synthesis_text[:300] + "..." if len(synthesis_text) > 300 else synthesis_text,
            "synthesis_text": synthesis_text,
            "primary_themes": themes,
            "gaps_identified": gaps,
            "sources_analyzed": len(extractions),
            "methodologies_found": len(set(methodologies))
        }
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract themes from synthesis text"""
        # Simple keyword extraction
        themes = []
        keywords = ["methodology", "approach", "technique", "framework", "algorithm"]
        for keyword in keywords:
            if keyword in text.lower():
                themes.append(f"Themes related to {keyword}")
        return themes[:5]
    
    def _extract_gaps(self, text: str, limitations: List[str]) -> List[str]:
        """Extract research gaps"""
        gaps = []
        if "gap" in text.lower() or "limitation" in text.lower():
            gaps.append("Research gaps identified in synthesis")
        if limitations:
            gaps.extend([f"Limitation: {l}" for l in limitations[:3]])
        return gaps[:5]

