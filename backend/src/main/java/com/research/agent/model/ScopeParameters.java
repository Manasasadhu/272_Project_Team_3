package com.research.agent.model;

public class ScopeParameters {
    private TemporalBoundary temporalBoundary;
    private QualityThreshold qualityThreshold;
    private String discoveryDepth;
    private boolean sourceDiversityRequirement;

    public TemporalBoundary getTemporalBoundary() {
        return temporalBoundary;
    }

    public void setTemporalBoundary(TemporalBoundary temporalBoundary) {
        this.temporalBoundary = temporalBoundary;
    }

    public QualityThreshold getQualityThreshold() {
        return qualityThreshold;
    }

    public void setQualityThreshold(QualityThreshold qualityThreshold) {
        this.qualityThreshold = qualityThreshold;
    }

    public String getDiscoveryDepth() {
        return discoveryDepth;
    }

    public void setDiscoveryDepth(String discoveryDepth) {
        this.discoveryDepth = discoveryDepth;
    }

    public boolean isSourceDiversityRequirement() {
        return sourceDiversityRequirement;
    }

    public void setSourceDiversityRequirement(boolean sourceDiversityRequirement) {
        this.sourceDiversityRequirement = sourceDiversityRequirement;
    }
}
