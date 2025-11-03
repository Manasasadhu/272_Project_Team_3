"""API routes"""
from fastapi import APIRouter, HTTPException
from api.schemas import (
    ExecuteAgentRequest, AgentExecutionResponse,
    AgentStatusResponse, SynthesisResponse
)
from services.agent_orchestrator import AgentOrchestrator
from infrastructure.redis_storage import RedisStorage
# ScopeParameters is in schemas, convert to dict for orchestrator
from models.agent_state import ExecutionStatus
from datetime import datetime, timedelta

router = APIRouter()
orchestrator = AgentOrchestrator()
storage = RedisStorage()

@router.post("/api/agent/execute", response_model=AgentExecutionResponse)
async def execute_agent(request: ExecuteAgentRequest):
    """Execute agent with research goal"""
    try:
        # Convert scope parameters to dict
        scope_params = None
        if request.scope_parameters:
            scope_params = {
                "temporal_boundary": request.scope_parameters.temporal_boundary.dict() if request.scope_parameters.temporal_boundary else None,
                "quality_threshold": request.scope_parameters.quality_threshold.dict() if request.scope_parameters.quality_threshold else None,
                "discovery_depth": request.scope_parameters.discovery_depth,
                "source_diversity_requirement": request.scope_parameters.source_diversity_requirement
            }
        
        # Execute
        response = await orchestrator.execute_research_goal(
            request.research_goal,
            scope_params
        )
        
        return AgentExecutionResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/agent/status/{job_id}", response_model=AgentStatusResponse)
async def get_status(job_id: str):
    """Get agent execution status"""
    try:
        state_dict = storage.get_agent_state(job_id)
        if not state_dict:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get data from Redis (source of truth)
        sources_found = storage.get_sources(job_id)
        extractions = storage.get_extractions(job_id)
        
        # Get audit log
        audit_entries = storage.get_audit_log(job_id)
        
        # Build response
        status = state_dict.get("status", "UNKNOWN")
        sources_found_count = len(sources_found)
        sources_validated_count = len(state_dict.get("sources_validated", []))
        extractions_count = len(extractions)
        
        # Calculate progress
        progress = 0
        if status == ExecutionStatus.SEARCHING:
            progress = 20
        elif status == ExecutionStatus.VALIDATING:
            progress = 40
        elif status == ExecutionStatus.EXTRACTING:
            progress = 60 + (extractions_count * 20 // max(sources_validated_count, 1))
        elif status == ExecutionStatus.SYNTHESIZING:
            progress = 90
        elif status == ExecutionStatus.COMPLETED:
            progress = 100
        
        # Get recent decisions
        recent_decisions = [
            {
                "timestamp": e.get("timestamp", ""),
                "decision_type": e.get("phase", ""),
                "reasoning": e.get("reasoning", ""),
                "action_taken": e.get("decision", "")
            }
            for e in audit_entries[-5:]  # Last 5 decisions
        ]
        
        return AgentStatusResponse(
            job_id=job_id,
            status=status,
            current_phase={
                "phase_name": state_dict.get("current_phase", "UNKNOWN"),
                "phase_description": f"Current phase: {status}",
                "progress_percentage": progress,
                "intelligent_actions_taken": [
                    f"Discovered {sources_found_count} sources",
                    f"Validated {sources_validated_count} sources",
                    f"Extracted {extractions_count} sources"
                ]
            },
            autonomous_decisions=recent_decisions,
            quality_metrics={
                "sources_discovered": sources_found_count,
                "sources_validated": sources_validated_count,
                "sources_accepted": sources_validated_count,
                "sources_rejected": sources_found_count - sources_validated_count,
                "average_quality_score": 0.85
            },
            intermediate_insights={
                "emerging_themes": ["Theme analysis in progress"],
                "gaps_identified": ["Gap analysis pending synthesis"]
            },
            estimated_completion=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/agent/results/{job_id}", response_model=SynthesisResponse)
async def get_results(job_id: str):
    """Get final synthesis results"""
    try:
        results = storage.get_results(job_id)
        if not results:
            raise HTTPException(status_code=404, detail="Results not found")
        
        audit_log = storage.get_audit_log(job_id)
        
        return SynthesisResponse(
            job_id=job_id,
            status="COMPLETED",
            synthesis=results.get("synthesis", {}),
            execution_summary=results.get("execution_summary", {}),
            audit_trail_summary={
                "total_decisions_logged": len(audit_log),
                "full_audit_log_available": True
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/agent/audit-log/{job_id}")
async def get_audit_log(job_id: str):
    """Get complete audit log"""
    try:
        audit_log = storage.get_audit_log(job_id)
        if not audit_log:
            raise HTTPException(status_code=404, detail="Audit log not found")
        return {"job_id": job_id, "entries": audit_log, "total": len(audit_log)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        storage.client.ping()
        return {"status": "healthy", "service": "agentic_server"}
    except:
        return {"status": "unhealthy", "service": "agentic_server"}

