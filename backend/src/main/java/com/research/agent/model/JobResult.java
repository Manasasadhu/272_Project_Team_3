package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class JobResult {

    @JsonProperty("job_id")
    private String jobId;

    @JsonProperty("status")
    private String status;

    @JsonProperty("sources")
    private List<Source> sources;

    @JsonProperty("detailed_analysis")
    private DetailedAnalysis detailedAnalysis;

    @JsonProperty("executive_summary")
    private ExecutiveSummary executiveSummary;

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

    public List<Source> getSources() {
        return sources;
    }

    public void setSources(List<Source> sources) {
        this.sources = sources;
    }

    public DetailedAnalysis getDetailedAnalysis() {
        return detailedAnalysis;
    }

    public void setDetailedAnalysis(DetailedAnalysis detailedAnalysis) {
        this.detailedAnalysis = detailedAnalysis;
    }

    public ExecutiveSummary getExecutiveSummary() {
        return executiveSummary;
    }

    public void setExecutiveSummary(ExecutiveSummary executiveSummary) {
        this.executiveSummary = executiveSummary;
    }
}
