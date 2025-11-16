package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ExecutionPlan {

    @JsonProperty("phases")
    private List<Phase> phases;

    @JsonProperty("estimated_sources")
    private int estimatedSources;

    @JsonProperty("estimated_duration_minutes")
    private int estimatedDurationMinutes;

    // Getters and Setters
    public List<Phase> getPhases() {
        return phases;
    }

    public void setPhases(List<Phase> phases) {
        this.phases = phases;
    }

    public int getEstimatedSources() {
        return estimatedSources;
    }

    public void setEstimatedSources(int estimatedSources) {
        this.estimatedSources = estimatedSources;
    }

    public int getEstimatedDurationMinutes() {
        return estimatedDurationMinutes;
    }

    public void setEstimatedDurationMinutes(int estimatedDurationMinutes) {
        this.estimatedDurationMinutes = estimatedDurationMinutes;
    }
}
