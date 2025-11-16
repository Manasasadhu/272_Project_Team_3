package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class JobResponse {

    @JsonProperty("job_id")
    private String jobId;

    @JsonProperty("status")
    private String status;

    @JsonProperty("autonomous_analysis")
    private AutonomousAnalysis autonomousAnalysis = new AutonomousAnalysis();

    @JsonProperty("execution_plan")
    private ExecutionPlan executionPlan = new ExecutionPlan();

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
}
