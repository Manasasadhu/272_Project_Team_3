"""API request/response schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# Request Schemas
class TemporalBoundary(BaseModel):
    publication_window_years: int = Field(default=3, ge=1, le=10)

class QualityThreshold(BaseModel):
    impact_level: Literal["cutting_edge", "high_impact", "established", "baseline"] = "high_impact"

class ScopeParameters(BaseModel):
    temporal_boundary: Optional[TemporalBoundary] = None
    quality_threshold: Optional[QualityThreshold] = None
    discovery_depth: Literal["rapid", "focused", "comprehensive", "exhaustive"] = "comprehensive"
    source_diversity_requirement: bool = True

class ExecuteAgentRequest(BaseModel):
    research_goal: str = Field(..., min_length=10, max_length=500)
    scope_parameters: Optional[ScopeParameters] = None

# Response Schemas
class AutonomousAnalysis(BaseModel):
    goal_decomposition: dict
    execution_strategy: dict
    governance_applied: dict

class PhasePlan(BaseModel):
    phase: str
    description: str

class ExecutionPlan(BaseModel):
    phases: List[PhasePlan]
    estimated_sources: int
    estimated_duration_minutes: Optional[int] = None

class AgentExecutionResponse(BaseModel):
    job_id: str
    status: str
    autonomous_analysis: AutonomousAnalysis
    execution_plan: ExecutionPlan

class PhaseStatus(BaseModel):
    phase_name: str
    phase_description: str
    progress_percentage: int
    intelligent_actions_taken: List[str]

class AutonomousDecision(BaseModel):
    timestamp: str
    decision_type: str
    reasoning: str
    action_taken: str

class QualityMetrics(BaseModel):
    sources_discovered: int
    sources_validated: int
    sources_accepted: int
    sources_rejected: int
    average_quality_score: float

class IntermediateInsights(BaseModel):
    emerging_themes: List[str]
    gaps_identified: List[str]

class AgentStatusResponse(BaseModel):
    job_id: str
    status: str
    current_phase: PhaseStatus
    autonomous_decisions: List[AutonomousDecision]
    quality_metrics: QualityMetrics
    intermediate_insights: Optional[IntermediateInsights] = None
    estimated_completion: Optional[str] = None

class SynthesisResponse(BaseModel):
    job_id: str
    status: str
    synthesis: dict
    execution_summary: dict
    audit_trail_summary: dict

