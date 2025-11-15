"""Redis storage implementation"""
import redis
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from infrastructure.config import config
from infrastructure.exceptions import StorageError

class RedisStorage:
    """Redis-based persistent storage"""
    
    def __init__(self):
        self.client = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis (lazy initialization)"""
        if self.client is None:
            self.client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Test connection (but don't fail if Redis is not available)
            try:
                self.client.ping()
            except Exception as e:
                # Log warning but allow server to start
                import warnings
                warnings.warn(f"Redis not available: {e}. Server will start but storage operations will fail.")
                self.client = None
    
    def _ensure_connected(self):
        """Ensure Redis connection"""
        if self.client is None:
            self._connect()
        if self.client is None:
            raise StorageError("Redis connection failed - please ensure Redis is running and accessible at {}:{}".format(
                config.REDIS_HOST, config.REDIS_PORT
            ))
    
    def create_job(self, job_id: str, research_goal: str, user_id: Optional[str] = None):
        """Create job record"""
        self._ensure_connected()
        job_data = {
            "job_id": job_id,
            "user_id": user_id or "anonymous",
            "research_goal": research_goal,
            "status": "INITIALIZED",
            "created_at": datetime.now().isoformat()
        }
        self.client.setex(f"job:{job_id}", 604800, json.dumps(job_data))
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job record"""
        self._ensure_connected()
        job_json = self.client.get(f"job:{job_id}")
        return json.loads(job_json) if job_json else None
    
    def save_agent_state(self, job_id: str, state: Dict[str, Any]):
        """Save agent state with 7-day TTL"""
        self._ensure_connected()
        state_json = json.dumps(state, default=str)
        self.client.setex(f"agent_state:{job_id}", 604800, state_json)
    
    def get_agent_state(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get agent state"""
        self._ensure_connected()
        state_json = self.client.get(f"agent_state:{job_id}")
        return json.loads(state_json) if state_json else None
    
    def append_source(self, job_id: str, source: Dict[str, Any]):
        """Append source to list"""
        self._ensure_connected()
        sources_json = self.client.get(f"sources:{job_id}")
        sources = json.loads(sources_json) if sources_json else []
        sources.append(source)
        self.client.setex(f"sources:{job_id}", 604800, json.dumps(sources))
    
    def get_sources(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all sources"""
        self._ensure_connected()
        sources_json = self.client.get(f"sources:{job_id}")
        return json.loads(sources_json) if sources_json else []
    
    def save_sources(self, job_id: str, sources: List[Dict[str, Any]]):
        """Save complete sources list"""
        self._ensure_connected()
        self.client.setex(f"sources:{job_id}", 604800, json.dumps(sources))
    
    def append_extraction(self, job_id: str, extraction: Dict[str, Any]):
        """Append extraction - checkpoint after each"""
        self._ensure_connected()
        extractions_json = self.client.get(f"extractions:{job_id}")
        extractions = json.loads(extractions_json) if extractions_json else []
        extractions.append(extraction)
        self.client.setex(f"extractions:{job_id}", 604800, json.dumps(extractions))
    
    def get_extractions(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all extractions"""
        self._ensure_connected()
        extractions_json = self.client.get(f"extractions:{job_id}")
        return json.loads(extractions_json) if extractions_json else []
    
    def append_audit_entry(self, job_id: str, entry: Dict[str, Any]):
        """Append audit log entry (immutable)"""
        self._ensure_connected()
        entry_json = json.dumps(entry, default=str)
        self.client.rpush(f"audit_log:{job_id}", entry_json)
        self.client.expire(f"audit_log:{job_id}", 604800)
    
    def get_audit_log(self, job_id: str) -> List[Dict[str, Any]]:
        """Get complete audit log"""
        self._ensure_connected()
        entries_json = self.client.lrange(f"audit_log:{job_id}", 0, -1)
        return [json.loads(e) for e in entries_json]
    
    def save_results(self, job_id: str, results: Dict[str, Any]):
        """Save final results"""
        self._ensure_connected()
        results_json = json.dumps(results, default=str)
        self.client.set(f"results:{job_id}", results_json)
    
    def get_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get results"""
        self._ensure_connected()
        results_json = self.client.get(f"results:{job_id}")
        return json.loads(results_json) if results_json else None

