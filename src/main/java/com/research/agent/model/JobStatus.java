package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class JobStatus {

    @JsonProperty("job_id")
    private String jobId;

    @JsonProperty("status")
    private String status;

    @JsonProperty("current_phase")
    private String currentPhase;

    @JsonProperty("sources_identified_count")
    private int sourcesIdentifiedCount;

    @JsonProperty("sources_processed_count")
    private int sourcesProcessedCount;

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

    public String getCurrentPhase() {
        return currentPhase;
    }

    public void setCurrentPhase(String currentPhase) {
        this.currentPhase = currentPhase;
    }

    public int getSourcesIdentifiedCount() {
        return sourcesIdentifiedCount;
    }

    public void setSourcesIdentifiedCount(int sourcesIdentifiedCount) {
        this.sourcesIdentifiedCount = sourcesIdentifiedCount;
    }

    public int getSourcesProcessedCount() {
        return sourcesProcessedCount;
    }

    public void setSourcesProcessedCount(int sourcesProcessedCount) {
        this.sourcesProcessedCount = sourcesProcessedCount;
    }
}
