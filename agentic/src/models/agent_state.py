"""Agent state model"""
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ExecutionStatus(str, Enum):
    INITIALIZING = "INITIALIZING"
    PLANNING = "PLANNING"
    SEARCHING = "SEARCHING"
    VALIDATING = "VALIDATING"
    EXTRACTING = "EXTRACTING"
    SYNTHESIZING = "SYNTHESIZING"
    COMPLETED = "COMPLETED"
    SELF_CORRECTING = "SELF_CORRECTING"

class AgentState:
    """Agent execution state"""
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = ExecutionStatus.INITIALIZING
        self.iteration_count = 0
        self.context_history: List[dict] = []
        self.sources_found: List[dict] = []
        self.sources_validated: List[dict] = []
        self.extractions_complete: List[dict] = []
        self.current_phase = "INITIALIZING"
        self.last_checkpoint: Optional[datetime] = None
        self.execution_plan: Optional[dict] = None
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "iteration_count": self.iteration_count,
            "context_history": self.context_history,
            "sources_found": self.sources_found,
            "sources_validated": self.sources_validated,
            "extractions_complete": self.extractions_complete,
            "current_phase": self.current_phase,
            "last_checkpoint": self.last_checkpoint.isoformat() if self.last_checkpoint else None,
            "execution_plan": self.execution_plan,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        state = cls(data["job_id"])
        state.status = ExecutionStatus(data.get("status", "INITIALIZING"))
        state.iteration_count = data.get("iteration_count", 0)
        state.context_history = data.get("context_history", [])
        state.sources_found = data.get("sources_found", [])
        state.sources_validated = data.get("sources_validated", [])
        state.extractions_complete = data.get("extractions_complete", [])
        state.current_phase = data.get("current_phase", "INITIALIZING")
        if data.get("last_checkpoint"):
            state.last_checkpoint = datetime.fromisoformat(data["last_checkpoint"])
        state.execution_plan = data.get("execution_plan")
        return state

