"""Structured extraction model"""
from typing import List
from datetime import datetime

class StructuredExtraction:
    """Structured extraction from source"""
    def __init__(self, source_url: str, methodology: str = "", 
                 key_findings: List[str] = None, datasets: List[str] = None,
                 limitations: List[str] = None):
        self.source_url = source_url
        self.methodology = methodology
        self.key_findings = key_findings or []
        self.datasets = datasets or []
        self.limitations = limitations or []
        self.extracted_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "source_url": self.source_url,
            "methodology": self.methodology,
            "key_findings": self.key_findings,
            "datasets": self.datasets,
            "limitations": self.limitations,
            "extracted_at": self.extracted_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            source_url=data.get("source_url", ""),
            methodology=data.get("methodology", ""),
            key_findings=data.get("key_findings", []),
            datasets=data.get("datasets", []),
            limitations=data.get("limitations", [])
        )

