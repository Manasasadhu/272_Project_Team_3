package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AutonomousAnalysis {

    @JsonProperty("goal_decomposition")
    private GoalDecomposition goalDecomposition;

    @JsonProperty("execution_strategy")
    private ExecutionStrategy executionStrategy;

    @JsonProperty("governance_applied")
    private GovernanceApplied governanceApplied;

    // Getters and Setters
    public GoalDecomposition getGoalDecomposition() {
        return goalDecomposition;
    }

    public void setGoalDecomposition(GoalDecomposition goalDecomposition) {
        this.goalDecomposition = goalDecomposition;
    }

    public ExecutionStrategy getExecutionStrategy() {
        return executionStrategy;
    }

    public void setExecutionStrategy(ExecutionStrategy executionStrategy) {
        this.executionStrategy = executionStrategy;
    }

    public GovernanceApplied getGovernanceApplied() {
        return governanceApplied;
    }

    public void setGovernanceApplied(GovernanceApplied governanceApplied) {
        this.governanceApplied = governanceApplied;
    }
}
