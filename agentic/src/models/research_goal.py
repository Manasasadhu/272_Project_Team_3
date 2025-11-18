"""Research goal and source models"""
from typing import List, Optional
from datetime import datetime

class ResearchGoal:
    """Research goal model"""
    def __init__(self, job_id: str, goal_text: str, user_id: Optional[str] = None):
        self.job_id = job_id
        self.goal_text = goal_text
        self.user_id = user_id or "anonymous"
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "goal_text": self.goal_text,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }

class SourceCandidate:
    """Source candidate model"""
    def __init__(self, url: str, title: str, authors: List[str], year: int, 
                 citations: int = 0, source_type: str = "academic_paper", venue: Optional[str] = None):
        self.url = url
        self.title = title
        self.authors = authors
        self.year = year
        self.citations = citations
        self.source_type = source_type
        self.venue = venue
    
    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "citations": self.citations,
            "source_type": self.source_type,
            "venue": self.venue
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            url=data.get("url", ""),
            title=data.get("title", ""),
            authors=data.get("authors", []),
            year=data.get("year", 2024),
            citations=data.get("citations", 0),
            source_type=data.get("source_type", "academic_paper"),
            venue=data.get("venue")
        )

class ValidationResult:
    """Validation result"""
    def __init__(self, is_valid: bool, violations: List[str] = None, confidence_score: float = 1.0):
        self.is_valid = is_valid
        self.violations = violations or []
        self.confidence_score = confidence_score
    
    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "violations": self.violations,
            "confidence_score": self.confidence_score
        }

