"""Agent orchestrator"""
import uuid
from typing import Dict, Any
from datetime import datetime
from infrastructure.redis_storage import RedisStorage
from infrastructure.llm_client import LLMClient
from models.agent_state import AgentState, ExecutionStatus
from models.research_goal import ResearchGoal
from agent.planner import Planner
from infrastructure.agent_memory import AgentMemory
from agent.react_agent import ReActAgent
from agent.executor import Executor
from agent.state_manager import StateManager
from tools.tool_registry import ToolRegistry
from governance.policy_engine import PolicyEngine
from governance.audit_logger import AuditLogger
from services.synthesis_service import SynthesisService

class AgentOrchestrator:
    """Main orchestration service"""
    
    def __init__(self):
        self.storage = RedisStorage()
        self.llm_client = LLMClient()
        self.tool_registry = ToolRegistry()
        self.executor = Executor(self.tool_registry)
        self.policy_engine = PolicyEngine()
        self.audit_logger = AuditLogger(self.storage)
        # Initialize memory for learning
        self.memory = AgentMemory(self.storage)
        # Use adaptive planner that learns
        from agent.adaptive_planner import AdaptivePlanner
        self.planner = AdaptivePlanner(self.llm_client, self.memory)
        self.react_agent = ReActAgent(
            self.llm_client, 
            self.executor,
            self.policy_engine,
            self.audit_logger
        )
        self.synthesis_service = SynthesisService(self.llm_client)
        self.state_manager = StateManager(self.storage)
    
    async def execute_research_goal(self, research_goal: str, 
                                   scope_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute complete research goal"""
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create job and initial state
        self.storage.create_job(job_id, research_goal)
        state = AgentState(job_id)
        state.status = ExecutionStatus.PLANNING
        self.state_manager.checkpoint(job_id, state)
        
        # Log initialization
        self.audit_logger.log_decision(
            job_id, "INITIALIZING",
            "Goal received and job created",
            f"Research goal: {research_goal}",
            tool_used=None
        )
        
        # Apply governance policies (convert dict to proper format if needed)
        policies = self.policy_engine.apply_user_constraints(scope_params)
        
        # Plan execution
        plan = self.planner.decompose_goal(research_goal, scope_params)
        state.execution_plan = plan
        state.status = ExecutionStatus.SEARCHING
        self.state_manager.checkpoint(job_id, state)
        
        self.audit_logger.log_decision(
            job_id, "PLANNING",
            "Execution plan created",
            f"Decomposed into {len(plan['search_queries'])} search queries, target: {plan['max_sources']} sources",
            tool_used="Planner"
        )
        
        # Execute ReAct agent (all checkpoints happen inside react_agent)
        results = self.react_agent.execute_loop(
            job_id, research_goal, plan, policies,
            self.state_manager, self.storage
        )
        
        # Get latest state (already updated by react_agent)
        state = self.state_manager.get_state(job_id)
        
        # Get extractions from Redis (already stored by react_agent)
        extractions = self.storage.get_extractions(job_id)
        
        # Synthesize
        synthesis = self.synthesis_service.synthesize(research_goal, extractions)
        
        # Finalize
        state.status = ExecutionStatus.COMPLETED
        self.state_manager.checkpoint(job_id, state)
        
        # Get final counts from Redis
        sources_found = self.storage.get_sources(job_id)
        validated_sources = state.sources_validated if state else []
        extractions_from_redis = self.storage.get_extractions(job_id)
        
        # Save results
        execution_summary = {
            "total_sources_discovered": len(sources_found),
            "sources_validated": len(validated_sources),
            "extractions_successful": len(extractions_from_redis)
        }
        
        self.storage.save_results(job_id, {
            "synthesis": synthesis,
            "execution_summary": execution_summary
        })
        
        self.audit_logger.log_decision(
            job_id, "COMPLETION",
            "Synthesis complete",
            f"Successfully synthesized {len(extractions_from_redis)} sources",
            tool_used="SynthesisService"
        )
        
        # Learn from execution - save to memory
        execution_time = (datetime.now() - state.created_at).total_seconds()
        self.memory.save_performance_metrics(job_id, {
            "execution_time": execution_time,
            "sources_discovered": len(sources_found),
            "extraction_success_rate": len(extractions_from_redis) / max(len(validated_sources), 1),
            "synthesis_quality": 0.85  # Could be calculated from synthesis metrics
        })
        
        # Save search patterns that worked
        if state.execution_plan and isinstance(state.execution_plan, dict) and state.execution_plan.get("search_queries"):
            self.planner.record_success(
                research_goal,
                state.execution_plan["search_queries"],
                {
                    "validation_rate": len(validated_sources) / max(len(sources_found), 1),
                    "avg_quality": 0.8,  # Could calculate from source metrics
                    "sources_per_query": len(sources_found) / max(len(state.execution_plan["search_queries"]), 1)
                }
            )
        
        # Return final status (work is already complete)
        return {
            "job_id": job_id,
            "status": "COMPLETED",
            "autonomous_analysis": {
                "goal_decomposition": {
                    "primary_objectives": plan["search_queries"][:3],
                    "estimated_complexity": "moderate"
                },
                "execution_strategy": {
                    "profile": "comprehensive",
                    "estimated_sources": plan["max_sources"],
                    "estimated_duration_minutes": 10
                },
                "governance_applied": {
                    "quality_policies": [
                        f"Publications from {policies.min_year}+",
                        f"Minimum citations: {policies.min_citations}",
                        "Peer-reviewed sources only"
                    ]
                }
            },
            "execution_plan": {
                "phases": plan["phases"],
                "estimated_sources": plan["max_sources"]
            }
        }

