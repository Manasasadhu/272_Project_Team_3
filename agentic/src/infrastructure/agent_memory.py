"""Agent memory for learning and evolution"""
import redis
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from infrastructure.config import config
from infrastructure.redis_storage import RedisStorage

class AgentMemory:
    """Cross-job memory for agent learning and evolution"""
    
    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self.client = storage.client
    
    # Pattern Learning
    def save_search_pattern(self, query: str, success_metrics: Dict[str, Any]):
        """Save successful search query patterns"""
        key = f"memory:search_pattern:{query[:50]}"
        pattern = {
            "query": query,
            "success_rate": success_metrics.get("success_rate", 0),
            "quality_score": success_metrics.get("quality_score", 0),
            "times_used": self._get_pattern_usage(query) + 1,
            "last_used": datetime.now().isoformat(),
            "avg_sources_found": success_metrics.get("avg_sources", 0)
        }
        self.client.setex(key, 2592000, json.dumps(pattern))  # 30 days
    
    def get_effective_search_patterns(self, research_goal: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get effective search patterns similar to goal"""
        # Simple similarity check - in production, use embeddings
        patterns = []
        keys = self.client.keys("memory:search_pattern:*")
        for key in keys[:100]:  # Check first 100 patterns
            pattern_json = self.client.get(key)
            if pattern_json:
                pattern = json.loads(pattern_json)
                if pattern.get("success_rate", 0) > 0.7:  # Only successful patterns
                    patterns.append(pattern)
        
        # Sort by success rate and recency
        patterns.sort(key=lambda x: (
            x.get("success_rate", 0),
            x.get("quality_score", 0)
        ), reverse=True)
        return patterns[:limit]
    
    def _get_pattern_usage(self, query: str) -> int:
        """Get pattern usage count"""
        key = f"memory:search_pattern:{query[:50]}"
        pattern_json = self.client.get(key)
        if pattern_json:
            return json.loads(pattern_json).get("times_used", 0)
        return 0
    
    # Source Quality Learning
    def save_source_quality(self, source_url: str, quality_metrics: Dict[str, Any]):
        """Save source quality metrics for future reference"""
        key = f"memory:source_quality:{source_url[:100]}"
        quality = {
            "url": source_url,
            "quality_score": quality_metrics.get("quality_score", 0),
            "extraction_success": quality_metrics.get("extraction_success", False),
            "citation_count": quality_metrics.get("citations", 0),
            "venue_reputation": quality_metrics.get("venue", ""),
            "times_referenced": self._get_source_references(source_url) + 1,
            "last_seen": datetime.now().isoformat()
        }
        self.client.setex(key, 2592000, json.dumps(quality))  # 30 days
    
    def get_source_quality(self, source_url: str) -> Optional[Dict[str, Any]]:
        """Get known quality metrics for a source"""
        key = f"memory:source_quality:{source_url[:100]}"
        quality_json = self.client.get(key)
        return json.loads(quality_json) if quality_json else None
    
    def _get_source_references(self, source_url: str) -> int:
        """Get how many times source was referenced"""
        key = f"memory:source_quality:{source_url[:100]}"
        quality_json = self.client.get(key)
        if quality_json:
            return json.loads(quality_json).get("times_referenced", 0)
        return 0
    
    # Execution Strategy Learning
    def save_execution_outcome(self, research_goal_type: str, strategy: Dict[str, Any], 
                              outcome: Dict[str, Any]):
        """Save what strategies worked for similar goals"""
        key = f"memory:strategy:{research_goal_type[:50]}"
        outcome_data = {
            "goal_type": research_goal_type,
            "strategy": strategy,
            "outcome": {
                "success_rate": outcome.get("success_rate", 0),
                "sources_found": outcome.get("sources_found", 0),
                "extraction_success": outcome.get("extraction_success", 0),
                "execution_time": outcome.get("execution_time", 0),
                "user_satisfaction": outcome.get("user_satisfaction", None)
            },
            "timestamp": datetime.now().isoformat()
        }
        # Store as list of outcomes for same goal type
        self.client.rpush(key, json.dumps(outcome_data))
        self.client.expire(key, 2592000)  # 30 days
    
    def get_effective_strategy(self, research_goal_type: str) -> Optional[Dict[str, Any]]:
        """Get most effective strategy for similar goal type"""
        key = f"memory:strategy:{research_goal_type[:50]}"
        outcomes_json = self.client.lrange(key, 0, -1)
        
        if not outcomes_json:
            return None
        
        # Analyze all outcomes, find best strategy
        outcomes = [json.loads(o) for o in outcomes_json]
        # Find strategy with highest success rate
        best = max(outcomes, key=lambda x: (
            x["outcome"].get("success_rate", 0),
            x["outcome"].get("user_satisfaction", 0) or 0
        ))
        return best.get("strategy")
    
    # Domain Knowledge Building
    def save_domain_knowledge(self, domain: str, knowledge: Dict[str, Any]):
        """Save domain-specific knowledge"""
        key = f"memory:domain:{domain}"
        knowledge_data = {
            "domain": domain,
            "key_themes": knowledge.get("themes", []),
            "top_sources": knowledge.get("top_sources", []),
            "effective_queries": knowledge.get("queries", []),
            "updated_at": datetime.now().isoformat()
        }
        self.client.setex(key, 2592000, json.dumps(knowledge_data))
    
    def get_domain_knowledge(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get accumulated domain knowledge"""
        key = f"memory:domain:{domain}"
        knowledge_json = self.client.get(key)
        return json.loads(knowledge_json) if knowledge_json else None
    
    # Performance Metrics
    def save_performance_metrics(self, job_id: str, metrics: Dict[str, Any]):
        """Save performance metrics for analysis"""
        key = f"memory:performance:{job_id}"
        metrics_data = {
            "job_id": job_id,
            "execution_time": metrics.get("execution_time", 0),
            "sources_discovered": metrics.get("sources_discovered", 0),
            "extraction_success_rate": metrics.get("extraction_success_rate", 0),
            "synthesis_quality": metrics.get("synthesis_quality", 0),
            "timestamp": datetime.now().isoformat()
        }
        self.client.setex(key, 2592000, json.dumps(metrics_data))
    
    def get_performance_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get performance trends over time"""
        keys = self.client.keys("memory:performance:*")
        cutoff = datetime.now() - timedelta(days=days)
        
        metrics_list = []
        for key in keys:
            metrics_json = self.client.get(key)
            if metrics_json:
                metrics = json.loads(metrics_json)
                if datetime.fromisoformat(metrics["timestamp"]) >= cutoff:
                    metrics_list.append(metrics)
        
        if not metrics_list:
            return {"trend": "insufficient_data"}
        
        avg_execution_time = sum(m.get("execution_time", 0) for m in metrics_list) / len(metrics_list)
        avg_sources = sum(m.get("sources_discovered", 0) for m in metrics_list) / len(metrics_list)
        avg_extraction_rate = sum(m.get("extraction_success_rate", 0) for m in metrics_list) / len(metrics_list)
        
        return {
            "avg_execution_time": avg_execution_time,
            "avg_sources_discovered": avg_sources,
            "avg_extraction_success_rate": avg_extraction_rate,
            "total_jobs_analyzed": len(metrics_list),
            "trend": "improving" if len(metrics_list) > 5 else "building_data"
        }

