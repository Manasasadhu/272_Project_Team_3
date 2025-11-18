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
                tool_used="search_papers"
            )
            
            result = self.executor.execute_tool("search_papers", {"query": query, "max_results": 20})
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
                        tool_used="search_papers"
                    )
                    result = self.executor.execute_tool("search_papers", {"query": query, "max_results": 20})
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
        relevance_threshold = 0.50  # Lowered from 0.65 to allow more papers through extraction phase
        sources_to_score = validated_sources  # Score ALL validated sources, not just first 20!
        
        if sources_to_score:
            try:
                # IMPROVED: Use multi-factor semantic heuristics instead of LLM
                # No Gemini blocking, highly interpretable, provably effective
                # Factors: keyword overlap (40%), recency (30%), citations (20%), venue (10%)
                
                from governance.relevance_scorer import RelevanceScorer
                from infrastructure.logging_setup import logger
                
                scorer = RelevanceScorer(logger=logger)
                scores = scorer.batch_score(sources_to_score, research_goal, verbose=True)
                
                logger.info(f"=== RELEVANCE SCORING (HEURISTIC-BASED) ===")
                logger.info(f"Research Goal: {research_goal}")
                logger.info(f"Papers scored: {len(sources_to_score)}")
                logger.info(f"Scoring factors: 40% keyword_overlap, 30% recency, 20% citations, 10% venue")
                logger.info(f"Threshold: {relevance_threshold}")
                
                # Now apply scores to actual sources
                for i, source in enumerate(sources_to_score):
                    if i < len(scores):
                        score = scores[i]
                        source['relevance_score'] = score
                        
                        # Calculate score breakdown for audit
                        keyword_component = source.get('title', '')
                        
                        if score >= relevance_threshold:
                            relevant_sources.append(source)
                            self.audit_logger.log_decision(
                                job_id, "RELEVANCE_FILTER",
                                f"Accepted: {source.get('title', 'Unknown')[:60]}",
                                f"Heuristic score: {score:.3f} >= {relevance_threshold} (keyword overlap, recency, citations, venue)",
                                tool_used="RelevanceScorer"
                            )
                        else:
                            self.audit_logger.log_decision(
                                job_id, "RELEVANCE_FILTER",
                                f"Filtered: {source.get('title', 'Unknown')[:60]}",
                                f"Heuristic score: {score:.3f} < {relevance_threshold}",
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
        
        # IMPROVED: Query expansion when too few papers pass relevance filter
        # This helps find more specific/relevant papers when initial search is too broad
        min_target_sources = 5
        if len(relevant_sources) < min_target_sources:
            self.audit_logger.log_decision(
                job_id, "SEARCH_EXPANSION",
                f"Only {len(relevant_sources)} sources passed relevance filter",
                f"Initiating query expansion to find more specific papers",
                tool_used="QueryExpander"
            )
            
            # Generate more specific search queries using keywords from research goal
            expansion_queries = self._generate_expansion_queries(research_goal)
            
            for expansion_query in expansion_queries[:2]:  # Try up to 2 expansion queries
                try:
                    # Search with more specific query
                    result = self.executor.execute_tool("search_papers", {"query": expansion_query, "max_results": 10})
                    
                    if result.success:
                        new_sources = result.data.get("results", []) if isinstance(result.data, dict) else result.data
                        
                        # Score new sources with same heuristics
                        new_scores = scorer.batch_score(new_sources, research_goal)
                        
                        for i, source in enumerate(new_sources):
                            if i < len(new_scores) and new_scores[i] >= relevance_threshold:
                                # Avoid duplicates
                                source_title = source.get('title', '')
                                if not any(s.get('title', '') == source_title for s in relevant_sources):
                                    relevant_sources.append(source)
                        
                        if len(relevant_sources) >= min_target_sources:
                            break
                            
                except Exception as e:
                    logger.warning(f"Query expansion failed for '{expansion_query}': {str(e)}")
                    continue
        
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
                tool_used="extract_paper"
            )
            
            result = self.executor.execute_tool("extract_paper", {"source_url": source.get("url", "")})
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
                    tool_used="extract_paper"
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
    
    def _generate_expansion_queries(self, research_goal: str) -> List[str]:
        """Generate more specific search queries when initial search is too broad
        
        Extracts key technical terms and generates queries with combinations of them.
        """
        # Technical domain keywords and their variants
        keyword_map = {
            "transformer": ["attention mechanism", "BERT", "GPT", "T5"],
            "architecture": ["neural network design", "model structure", "encoder decoder"],
            "optimization": ["training efficiency", "inference speed", "computational efficiency"],
            "efficiency": ["parameter reduction", "pruning", "quantization", "distillation"],
            "improvement": ["advances", "enhancement", "breakthrough", "innovation"],
            "neural": ["deep learning", "machine learning", "representation learning"],
        }
        
        # Extract relevant keywords from goal
        goal_lower = research_goal.lower()
        expansion_queries = []
        
        for key, variants in keyword_map.items():
            if key in goal_lower:
                # Create queries combining the key term with its variants
                for variant in variants[:2]:  # Use first 2 variants
                    if variant not in goal_lower:
                        new_query = f"{key} {variant}"
                        if new_query not in expansion_queries:
                            expansion_queries.append(new_query)
        
        # If no expansions found, create generic technical queries
        if not expansion_queries:
            expansion_queries = [
                "transformer model architecture",
                "neural network optimization",
                "deep learning efficiency",
                "attention mechanism improvements"
            ]
        
        return expansion_queries[:4]  # Return up to 4 expansion queries