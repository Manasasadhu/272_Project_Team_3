package com.research.agent.model.agentic;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class AgenticJobResult {
    
    @JsonProperty("job_id")
    private String jobId;
    
    @JsonProperty("status")
    private String status;
    
    @JsonProperty("sources")
    private List<AgenticSource> sources;
    
    @JsonProperty("detailed_analysis")
    private AgenticDetailedAnalysis detailedAnalysis;
    
    @JsonProperty("executive_summary")
    private AgenticExecutiveSummary executiveSummary;

    public String getJobId() {
        return jobId;
    }

    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public List<AgenticSource> getSources() {
        return sources;
    }

    public void setSources(List<AgenticSource> sources) {
        this.sources = sources;
    }

    public AgenticDetailedAnalysis getDetailedAnalysis() {
        return detailedAnalysis;
    }

    public void setDetailedAnalysis(AgenticDetailedAnalysis detailedAnalysis) {
        this.detailedAnalysis = detailedAnalysis;
    }

    public AgenticExecutiveSummary getExecutiveSummary() {
        return executiveSummary;
    }

    public void setExecutiveSummary(AgenticExecutiveSummary executiveSummary) {
        this.executiveSummary = executiveSummary;
    }

    public static class AgenticSource {
        @JsonProperty("source_id")
        private String sourceId;
        
        @JsonProperty("title")
        private String title;
        
        @JsonProperty("authors")
        private String authors;
        
        @JsonProperty("publication_year")
        private Integer publicationYear;
        
        @JsonProperty("summary")
        private String summary;

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

        public String getAuthors() {
            return authors;
        }

        public void setAuthors(String authors) {
            this.authors = authors;
        }

        public Integer getPublicationYear() {
            return publicationYear;
        }

        public void setPublicationYear(Integer publicationYear) {
            this.publicationYear = publicationYear;
        }

        public String getSummary() {
            return summary;
        }

        public void setSummary(String summary) {
            this.summary = summary;
        }
    }

    public static class AgenticDetailedAnalysis {
        @JsonProperty("main_findings")
        private String mainFindings;
        
        @JsonProperty("key_takeaways")
        private String keyTakeaways;

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

    public static class AgenticExecutiveSummary {
        @JsonProperty("highlights")
        private String highlights;
        
        @JsonProperty("consolidated_conclusions")
        private String consolidatedConclusions;

        public String getHighlights() {
            return highlights;
        }

        public void setHighlights(String highlights) {
            this.highlights = highlights;
        }

        public String getConsolidatedConclusions() {
            return consolidatedConclusions;
        }

        public void setConsolidatedConclusions(String consolidatedConclusions) {
            this.consolidatedConclusions = consolidatedConclusions;
        }
    }
}
