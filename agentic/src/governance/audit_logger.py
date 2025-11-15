"""Audit logger"""
from typing import Optional, List
from infrastructure.redis_storage import RedisStorage
from models.audit_log import AuditEntry

class AuditLogger:
    """Immutable audit logging"""
    
    def __init__(self, storage: RedisStorage):
        self.storage = storage
    
    def log_decision(self, job_id: str, phase: str, decision: str, 
                    reasoning: str, tool_used: Optional[str] = None,
                    context: Optional[dict] = None):
        """Log decision to audit trail"""
        entry = AuditEntry(
            phase=phase,
            decision=decision,
            reasoning=reasoning,
            tool_used=tool_used,
            context=context or {}
        )
        self.storage.append_audit_entry(job_id, entry.to_dict())
    
    def get_audit_log(self, job_id: str) -> List[dict]:
        """Get complete audit log"""
        return self.storage.get_audit_log(job_id)

