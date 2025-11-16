package com.research.agent.model;

public class ResearchRequest {
    private String researchGoal;
    private ScopeParameters scopeParameters;

    public String getResearchGoal() {
        return researchGoal;
    }

    public void setResearchGoal(String researchGoal) {
        this.researchGoal = researchGoal;
    }

    public ScopeParameters getScopeParameters() {
        return scopeParameters;
    }

    public void setScopeParameters(ScopeParameters scopeParameters) {
        this.scopeParameters = scopeParameters;
    }
}
