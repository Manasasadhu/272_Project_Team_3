package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ExecutiveSummary {

    @JsonProperty("highlights")
    private String highlights;

    @JsonProperty("consolidated_conclusions")
    private String consolidatedConclusions;

    // Getters and Setters
    public String getHighlights() {
        return highlights;
    }

    public void setHighlights(String highlights) {
        this.highlights = highlights;
    }

    public String getConsolidatedConclusions() {
        return consolidatedConclusions;
    }

    public void setConsolidatedConclusions(String consolidatedConclusions) {
        this.consolidatedConclusions = consolidatedConclusions;
    }
}
