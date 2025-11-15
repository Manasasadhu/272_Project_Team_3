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
                # result.data is a dict with "results" key containing the list
                sources = result.data.get("results", []) if isinstance(result.data, dict) else result.data
                for source in sources:
                    storage.append_source(job_id, source)
                all_sources.extend(sources)
                
                # Update state and checkpoint
                state = state_manager.get_state(job_id)
                if state:
                    state.sources_found = all_sources
                    state.current_phase = "SEARCHING"
                    state_manager.checkpoint(job_id, state)
        
        # Adaptive Refinement: If insufficient sources found, generate new queries
        target_sources = plan.get("max_sources", 20)
        if len(all_sources) < target_sources // 2:  # Less than 50% of target
            self.audit_logger.log_decision(
                job_id, "ADAPTIVE_REFINEMENT",
                f"Insufficient sources: {len(all_sources)}/{target_sources}",
                "Generating refined search queries",
                tool_used="AdaptivePlanner"
            )
            
            try:
                # Generate new queries
                refinement_prompt = f"""Initial searches found only {len(all_sources)} sources (target: {target_sources}).
Research Goal: {research_goal}
Original Queries: {', '.join(plan['search_queries'][:3])}

Generate 2 alternative search queries using different terminology or angles.
Return only the queries, one per line."""
                
                new_queries_text = self.llm_client.generate_completion(refinement_prompt, temperature=0.7, max_tokens=150)
                new_queries = [q.strip() for q in new_queries_text.strip().split('\n') if q.strip() and len(q.strip()) > 5][:2]
                
                # Execute new queries
                for query in new_queries:
                    self.audit_logger.log_decision(
                        job_id, "SEARCHING",
                        f"Refined search: {query}",
                        "Executing adaptive search query",
                        tool_used="SearchTool"
                    )
                    result = self.executor.execute_tool("SearchTool", {"query": query, "limit": 20})
                    if result.success:
                        sources = result.data.get("results", []) if isinstance(result.data, dict) else result.data
                        for source in sources:
                            storage.append_source(job_id, source)
                        all_sources.extend(sources)
            except Exception as e:
                # Silently continue if refinement fails
                self.audit_logger.log_decision(
                    job_id, "ADAPTIVE_REFINEMENT",
                    "Refinement skipped",
                    f"Continuing with {len(all_sources)} sources",
                    tool_used="AdaptivePlanner"
                )
        
        # Phase 2: Validate - Store validated sources to Redis immediately
        from governance.validator import SourceValidator
        validator = SourceValidator(policies)
        validated_sources = validator.validate_all_sources(all_sources)
        
        # Relevance Scoring: Batch score sources (efficient for demos!)
        relevant_sources = []
        relevance_threshold = 0.6
        sources_to_score = validated_sources[:min(20, plan["max_sources"])]  # Limit to 20 for demo
        
        if sources_to_score:
            try:
                # Batch score up to 20 sources in ONE LLM call
                batch_prompt = f"""Rate relevance (0.0-1.0) for each paper below.
Research Goal: {research_goal}

Papers to rate:
"""
                for i, source in enumerate(sources_to_score):
                    title = source.get('title', 'Unknown')[:150]
                    batch_prompt += f"{i}. {title}\n"
                
                batch_prompt += f"""
Return ONLY comma-separated scores in order (e.g., "0.85,0.72,0.91,0.45,..."):"""
                
                scores_text = self.llm_client.generate_completion(batch_prompt, temperature=0.0, max_tokens=200)
                scores = [float(s.strip()) for s in scores_text.split(',') if s.strip()]
                
                # Apply scores to sources
                for i, source in enumerate(sources_to_score):
                    if i < len(scores):
                        score = max(0.0, min(1.0, scores[i]))  # Clamp 0-1
                        source['relevance_score'] = score
                        
                        if score >= relevance_threshold:
                            relevant_sources.append(source)
                        else:
                            self.audit_logger.log_decision(
                                job_id, "RELEVANCE_FILTER",
                                f"Filtered: {source.get('title', 'Unknown')[:60]}",
                                f"Relevance score: {score:.2f} < {relevance_threshold}",
                                tool_used="RelevanceScorer"
                            )
                    else:
                        # If we didn't get enough scores, keep remaining sources
                        relevant_sources.append(source)
                        
            except Exception as e:
                # If batch scoring fails, keep all sources (safe fallback for demo)
                self.audit_logger.log_decision(
                    job_id, "RELEVANCE_FILTER",
                    "Batch scoring failed, keeping all sources",
                    f"Error: {str(e)}",
                    tool_used="RelevanceScorer"
                )
                relevant_sources = sources_to_score
        
        # Limit to max_sources needed
        validated_sources = relevant_sources[:plan["max_sources"]]
        
        self.audit_logger.log_decision(
            job_id, "RELEVANCE_FILTER",
            f"Relevance filtering complete",
            f"Kept {len(validated_sources)} highly relevant sources",
            tool_used="RelevanceScorer"
        )
        
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

