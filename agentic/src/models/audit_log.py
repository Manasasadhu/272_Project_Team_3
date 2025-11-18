"""Audit log models"""
from typing import Optional, List
from datetime import datetime

class AuditEntry:
    """Single audit log entry"""
    def __init__(self, phase: str, decision: str, reasoning: str,
                 tool_used: Optional[str] = None, context: Optional[dict] = None):
        self.timestamp = datetime.now()
        self.phase = phase
        self.decision = decision
        self.reasoning = reasoning
        self.tool_used = tool_used
        self.context = context or {}
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "phase": self.phase,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "tool_used": self.tool_used,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        entry = cls(
            phase=data.get("phase", ""),
            decision=data.get("decision", ""),
            reasoning=data.get("reasoning", ""),
            tool_used=data.get("tool_used"),
            context=data.get("context", {})
        )
        if "timestamp" in data:
            entry.timestamp = datetime.fromisoformat(data["timestamp"])
        return entry

class AuditLog:
    """Complete audit log"""
    def __init__(self, job_id: str, entries: List[AuditEntry] = None):
        self.job_id = job_id
        self.entries = entries or []
    
    def add_entry(self, entry: AuditEntry):
        """Add audit entry"""
        self.entries.append(entry)
    
    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "entries": [e.to_dict() for e in self.entries],
            "total_decisions": len(self.entries)
        }

