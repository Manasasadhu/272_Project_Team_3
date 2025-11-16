package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class DetailedAnalysis {

    @JsonProperty("main_findings")
    private String mainFindings;

    @JsonProperty("key_takeaways")
    private String keyTakeaways;

    // Getters and Setters
    public String getMainFindings() {
        return mainFindings;
    }

    public void setMainFindings(String mainFindings) {
        this.mainFindings = mainFindings;
    }

    public String getKeyTakeaways() {
        return keyTakeaways;
    }

    public void setKeyTakeaways(String keyTakeaways) {
        this.keyTakeaways = keyTakeaways;
    }
}
