"""ReAct agent implementation"""
from typing import List, Dict, Any
from infrastructure.llm_client import LLMClient
from agent.executor import Executor
from governance.policy_engine import PolicyEngine
from governance.audit_logger import AuditLogger
from models.agent_state import ExecutionStatus
from infrastructure.config import config

class ReActAgent:
    """ReAct (Reasoning and Acting) agent"""
    
    def __init__(self, llm_client: LLMClient, executor: Executor, 
                 policy_engine: PolicyEngine, audit_logger: AuditLogger):
        self.llm_client = llm_client
        self.executor = executor
        self.policy_engine = policy_engine
        self.audit_logger = audit_logger
        self.max_iterations = config.MAX_ITERATIONS
    
    def execute_loop(self, job_id: str, research_goal: str, plan: Dict[str, Any],
                    policies: Any, state_manager: Any, storage: Any) -> Dict[str, Any]:
        """Execute ReAct loop with Redis checkpoints at every stage"""
        
        # Phase 1: Search - Store sources to Redis after each search batch
        all_sources = []
        for query in plan["search_queries"]:
            self.audit_logger.log_decision(
                job_id, "SEARCHING", 
                f"Executing search: {query}",
                f"Searching for sources using query: {query}",
                tool_used="SearchTool"
            )
            
            result = self.executor.execute_tool("SearchTool", {"query": query, "limit": 20})
            if result.success:
                # Store each source to Redis immediately
                for source in result.data:
                    storage.append_source(job_id, source)
                all_sources.extend(result.data)
                
                # Update state and checkpoint
                state = state_manager.get_state(job_id)
                if state:
                    state.sources_found = all_sources
                    state.current_phase = "SEARCHING"
                    state_manager.checkpoint(job_id, state)
        
        # Phase 2: Validate - Store validated sources to Redis immediately
        from governance.validator import SourceValidator
        validator = SourceValidator(policies)
        validated_sources = validator.validate_all_sources(all_sources)
        
        # Limit to max_sources
        validated_sources = validated_sources[:plan["max_sources"]]
        
        # Save validated sources to Redis
        storage.save_sources(job_id, validated_sources)
        
        # Update state with validated sources
        state = state_manager.get_state(job_id)
        if state:
            state.sources_validated = validated_sources
            state.status = ExecutionStatus.VALIDATING
            state.current_phase = "VALIDATING"
            state_manager.checkpoint(job_id, state)
        
        self.audit_logger.log_decision(
            job_id, "VALIDATING",
            f"Validated {len(validated_sources)} sources",
            f"Applied governance rules, accepted {len(validated_sources)}/{len(all_sources)} sources",
            tool_used="Validator"
        )
        
        # Phase 3: Extract - Store each extraction to Redis immediately (checkpoint pattern)
        extractions = []
        state = state_manager.get_state(job_id)
        if state:
            state.status = ExecutionStatus.EXTRACTING
            state.current_phase = "EXTRACTING"
            state_manager.checkpoint(job_id, state)
        
        for i, source in enumerate(validated_sources):
            self.audit_logger.log_decision(
                job_id, "EXTRACTING",
                f"Extracting from source {i+1}/{len(validated_sources)}",
                f"Extracting structured data from {source.get('title', 'source')}",
                tool_used="ExtractionTool"
            )
            
            result = self.executor.execute_tool("ExtractionTool", {"source_url": source.get("url", "")})
            if result.success:
                extraction = result.data
                extractions.append(extraction)
                
                # Store extraction to Redis immediately (checkpoint after each)
                storage.append_extraction(job_id, extraction)
                
                # Update state and checkpoint after each extraction
                state = state_manager.get_state(job_id)
                if state:
                    state.extractions_complete = extractions
                    state_manager.checkpoint(job_id, state)
            else:
                self.audit_logger.log_decision(
                    job_id, "EXTRACTING",
                    f"Extraction failed for source {i+1}",
                    f"Error: {result.error}, skipping source",
                    tool_used="ExtractionTool"
                )
        
        # Final state update
        state = state_manager.get_state(job_id)
        if state:
            state.status = ExecutionStatus.SYNTHESIZING
            state.current_phase = "SYNTHESIZING"
            state_manager.checkpoint(job_id, state)
        
        return {
            "sources_found": all_sources,
            "sources_validated": validated_sources,
            "extractions_complete": extractions
        }

