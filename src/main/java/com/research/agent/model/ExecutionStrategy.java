package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ExecutionStrategy {

    @JsonProperty("search_approach")
    private String searchApproach;

    @JsonProperty("validation_rules")
    private List<String> validationRules;

    // Getters and Setters
    public String getSearchApproach() {
        return searchApproach;
    }

    public void setSearchApproach(String searchApproach) {
        this.searchApproach = searchApproach;
    }

    public List<String> getValidationRules() {
        return validationRules;
    }

    public void setValidationRules(List<String> validationRules) {
        this.validationRules = validationRules;
    }
}
