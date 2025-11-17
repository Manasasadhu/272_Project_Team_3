package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Phase {

    @JsonProperty("phase")
    private String phase;

    @JsonProperty("description")
    private String description;

    // Getters and Setters
    public String getPhase() {
        return phase;
    }

    public void setPhase(String phase) {
        this.phase = phase;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
