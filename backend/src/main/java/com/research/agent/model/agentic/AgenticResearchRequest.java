package com.research.agent.model.agentic;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AgenticResearchRequest {
    
    @JsonProperty("research_goal")
    private String researchGoal;
    
    @JsonProperty("scope_parameters")
    private AgenticScopeParameters scopeParameters;

    public String getResearchGoal() {
        return researchGoal;
    }

    public void setResearchGoal(String researchGoal) {
        this.researchGoal = researchGoal;
    }

    public AgenticScopeParameters getScopeParameters() {
        return scopeParameters;
    }

    public void setScopeParameters(AgenticScopeParameters scopeParameters) {
        this.scopeParameters = scopeParameters;
    }
}
