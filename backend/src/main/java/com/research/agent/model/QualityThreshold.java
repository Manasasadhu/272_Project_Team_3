package com.research.agent.model;

public class QualityThreshold {
    private String citationImpactFactor;
    private String publicationTier;

    public String getCitationImpactFactor() {
        return citationImpactFactor;
    }

    public void setCitationImpactFactor(String citationImpactFactor) {
        this.citationImpactFactor = citationImpactFactor;
    }

    public String getPublicationTier() {
        return publicationTier;
    }

    public void setPublicationTier(String publicationTier) {
        this.publicationTier = publicationTier;
    }
}
