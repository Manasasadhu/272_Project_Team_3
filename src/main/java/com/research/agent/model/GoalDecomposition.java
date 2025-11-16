package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class GoalDecomposition {

    @JsonProperty("primary_objectives")
    private List<String> primaryObjectives;

    @JsonProperty("sub_goals")
    private List<String> subGoals;

    // Getters and Setters
    public List<String> getPrimaryObjectives() {
        return primaryObjectives;
    }

    public void setPrimaryObjectives(List<String> primaryObjectives) {
        this.primaryObjectives = primaryObjectives;
    }

    public List<String> getSubGoals() {
        return subGoals;
    }

    public void setSubGoals(List<String> subGoals) {
        this.subGoals = subGoals;
    }
}
