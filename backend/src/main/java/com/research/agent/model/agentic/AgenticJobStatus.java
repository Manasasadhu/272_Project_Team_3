package com.research.agent.model.agentic;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;

public class AgenticJobStatus {
    
    @JsonProperty("job_id")
    private String jobId;
    
    @JsonProperty("status")
    private String status;
    
    @JsonProperty("current_phase")
    private Map<String, Object> currentPhase;
    
    @JsonProperty("progress_percentage")
    private Integer progressPercentage;

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

    public Map<String, Object> getCurrentPhase() {
        return currentPhase;
    }

    public void setCurrentPhase(Map<String, Object> currentPhase) {
        this.currentPhase = currentPhase;
    }

    public Integer getProgressPercentage() {
        return progressPercentage;
    }

    public void setProgressPercentage(Integer progressPercentage) {
        this.progressPercentage = progressPercentage;
    }
}
