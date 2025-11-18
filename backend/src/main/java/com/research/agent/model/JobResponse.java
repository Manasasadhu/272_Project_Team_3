package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

public class JobResponse {

    @JsonProperty("job_id")
    private String jobId;

    @JsonProperty("status")
    private String status;

    @JsonProperty("autonomous_analysis")
    private AutonomousAnalysis autonomousAnalysis;

    @JsonProperty("execution_plan")
    private ExecutionPlan executionPlan;

    // Synthesis response fields from agentic service
    @JsonProperty("synthesis")
    private Map<String, Object> synthesis;

    @JsonProperty("execution_summary")
    private Map<String, Object> executionSummary;

    @JsonProperty("audit_trail_summary")
    private Map<String, Object> auditTrailSummary;

    // Getters and Setters
    public String getJobId() {
        return jobId;
    }

    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public AutonomousAnalysis getAutonomousAnalysis() {
        return autonomousAnalysis;
    }

    public void setAutonomousAnalysis(AutonomousAnalysis autonomousAnalysis) {
        this.autonomousAnalysis = autonomousAnalysis;
    }

    public ExecutionPlan getExecutionPlan() {
        return executionPlan;
    }

    public void setExecutionPlan(ExecutionPlan executionPlan) {
        this.executionPlan = executionPlan;
    }

    public Map<String, Object> getSynthesis() {
        return synthesis;
    }

    public void setSynthesis(Map<String, Object> synthesis) {
        this.synthesis = synthesis;
    }

    public Map<String, Object> getExecutionSummary() {
        return executionSummary;
    }

    public void setExecutionSummary(Map<String, Object> executionSummary) {
        this.executionSummary = executionSummary;
    }

    public Map<String, Object> getAuditTrailSummary() {
        return auditTrailSummary;
    }

    public void setAuditTrailSummary(Map<String, Object> auditTrailSummary) {
        this.auditTrailSummary = auditTrailSummary;
    }
}
