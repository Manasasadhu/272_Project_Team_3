"""Source validator"""
from typing import List
from models.research_goal import SourceCandidate, ValidationResult
from governance.policy_engine import Policies

class SourceValidator:
    """Validate sources against governance policies"""
    
    def __init__(self, policies: Policies):
        self.policies = policies
    
    def validate_source(self, candidate: dict) -> ValidationResult:
        """Validate single source"""
        violations = []
        
        # Check publication year
        if candidate.get("year", 0) < self.policies.min_year:
            violations.append(f"Publication too old ({candidate.get('year')} < {self.policies.min_year})")
        
        # Check citations
        if candidate.get("citations", 0) < self.policies.min_citations:
            violations.append(f"Low citations ({candidate.get('citations')} < {self.policies.min_citations})")
        
        # Peer review check (assume all from academic APIs are peer-reviewed)
        # In real implementation, would check venue reputation
        
        is_valid = len(violations) == 0
        confidence = 1.0 if is_valid else max(0.0, 1.0 - len(violations) * 0.3)
        
        return ValidationResult(
            is_valid=is_valid,
            violations=violations,
            confidence_score=confidence
        )
    
    def validate_all_sources(self, sources: List[dict]) -> List[dict]:
        """Validate and filter all sources"""
        validated = []
        for source in sources:
            result = self.validate_source(source)
            if result.is_valid:
                validated.append(source)
        return validated

