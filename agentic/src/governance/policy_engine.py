"""Policy engine for governance"""
from datetime import datetime
from typing import Optional
# Note: ScopeParameters will be passed as dict from API layer

class Policies:
    """Governance policies"""
    def __init__(self):
        self.min_year = 1990  # Allow papers from 1990+ (covers foundational work)
        self.min_citations = 5  # Lowered from 20 to include more diverse sources
        self.require_peer_reviewed = False  # Allow preprints and non-peer-reviewed
        self.max_sources = 30
        self.include_preprints = True  # Enable preprints
    
    def to_dict(self) -> dict:
        return {
            "min_year": self.min_year,
            "min_citations": self.min_citations,
            "require_peer_reviewed": self.require_peer_reviewed,
            "max_sources": self.max_sources,
            "include_preprints": self.include_preprints
        }

class PolicyEngine:
    """Master system prompt and policy engine"""
    
    MASTER_SYSTEM_PROMPT = """
    You are an autonomous knowledge discovery agent operating under strict governance rules:
    
    SOURCE QUALITY RULES:
    - Sources MUST be peer-reviewed (unless explicitly allowed)
    - Sources MUST meet minimum citation threshold
    - Sources MUST be within specified publication timeframe
    - Sources MUST NOT be from blacklisted venues
    
    DECISION MAKING:
    - Every decision must be justified against governance rules
    - Log all decisions with reasoning in audit trail
    - Reject sources that violate any critical rule
    
    EXECUTION:
    - Operate autonomously but within governance boundaries
    - Self-correct if quality issues are detected
    - Prioritize source diversity when possible
    """
    
    IMPACT_THRESHOLDS = {
        "cutting_edge": 50,
        "high_impact": 20,
        "established": 10,
        "baseline": 0
    }
    
    DEPTH_SOURCE_MAP = {
        "rapid": 10,
        "focused": 15,
        "comprehensive": 30,
        "exhaustive": 50
    }
    
    def __init__(self):
        self.default_policies = Policies()
    
    def apply_user_constraints(self, scope_params: Optional[dict]) -> Policies:
        """Apply user Discovery Settings to governance policies"""
        policies = Policies()
        
        if not scope_params:
            return self.default_policies
        
        # Publication window
        if scope_params.get("temporal_boundary"):
            years = scope_params["temporal_boundary"].get("publication_window_years", 3)
            policies.min_year = datetime.now().year - years
        
        # Quality threshold
        if scope_params.get("quality_threshold"):
            impact_level = scope_params["quality_threshold"].get("impact_level", "high_impact")
            policies.min_citations = self.IMPACT_THRESHOLDS.get(impact_level, 20)
        
        # Discovery depth -> max sources
        if scope_params.get("discovery_depth"):
            policies.max_sources = self.DEPTH_SOURCE_MAP.get(
                scope_params["discovery_depth"], 30
            )
        
        # Include preprints (if in future we add this)
        # policies.include_preprints = scope_params.get("include_preprints", False)
        
        return policies
    
    def get_master_prompt(self) -> str:
        """Get master system prompt"""
        return self.MASTER_SYSTEM_PROMPT

