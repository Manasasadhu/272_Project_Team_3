package com.research.agent.model.agentic;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AgenticScopeParameters {
    
    @JsonProperty("time_range")
    private Integer timeRange;
    
    @JsonProperty("research_depth")
    private String researchDepth;
    
    @JsonProperty("source_quality")
    private String sourceQuality;
    
    @JsonProperty("source_diversity")
    private Boolean sourceDiversity;

    public Integer getTimeRange() {
        return timeRange;
    }

    public void setTimeRange(Integer timeRange) {
        this.timeRange = timeRange;
    }

    public String getResearchDepth() {
        return researchDepth;
    }

    public void setResearchDepth(String researchDepth) {
        this.researchDepth = researchDepth;
    }

    public String getSourceQuality() {
        return sourceQuality;
    }

    public void setSourceQuality(String sourceQuality) {
        this.sourceQuality = sourceQuality;
    }

    public Boolean getSourceDiversity() {
        return sourceDiversity;
    }

    public void setSourceDiversity(Boolean sourceDiversity) {
        this.sourceDiversity = sourceDiversity;
    }
}
