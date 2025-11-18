package com.research.agent.model.agentic;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AgenticJobResponse {
    
    @JsonProperty("job_id")
    private String jobId;
    
    @JsonProperty("status")
    private String status;

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
}
