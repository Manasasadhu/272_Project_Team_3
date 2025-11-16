package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class GovernanceApplied {

    @JsonProperty("policies_checked")
    private List<String> policiesChecked;

    // Getters and Setters
    public List<String> getPoliciesChecked() {
        return policiesChecked;
    }

    public void setPoliciesChecked(List<String> policiesChecked) {
        this.policiesChecked = policiesChecked;
    }
}
