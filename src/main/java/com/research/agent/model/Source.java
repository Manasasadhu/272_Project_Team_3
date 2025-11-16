package com.research.agent.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Source {

    @JsonProperty("source_id")
    private String sourceId;

    @JsonProperty("title")
    private String title;

    @JsonProperty("publication_year")
    private int publicationYear;

    @JsonProperty("authors")
    private String authors;

    @JsonProperty("summary")
    private String summary;

    // Getters and Setters
    public String getSourceId() {
        return sourceId;
    }

    public void setSourceId(String sourceId) {
        this.sourceId = sourceId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getPublicationYear() {
        return publicationYear;
    }

    public void setPublicationYear(int publicationYear) {
        this.publicationYear = publicationYear;
    }

    public String getAuthors() {
        return authors;
    }

    public void setAuthors(String authors) {
        this.authors = authors;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }
}
