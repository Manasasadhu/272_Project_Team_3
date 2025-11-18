"""State manager"""
from infrastructure.redis_storage import RedisStorage
from models.agent_state import AgentState
from datetime import datetime

class StateManager:
    """Agent state management"""
    
    def __init__(self, storage: RedisStorage):
        self.storage = storage
    
    def checkpoint(self, job_id: str, state: AgentState):
        """Save state checkpoint"""
        state.last_checkpoint = datetime.now()
        self.storage.save_agent_state(job_id, state.to_dict())
    
    def get_state(self, job_id: str) -> AgentState:
        """Get agent state"""
        state_dict = self.storage.get_agent_state(job_id)
        if state_dict:
            return AgentState.from_dict(state_dict)
        return None
    
    def save_state(self, job_id: str, state: AgentState):
        """Save agent state"""
        self.storage.save_agent_state(job_id, state.to_dict())

