package com.research.agent.service;

import com.research.agent.model.*;
import com.research.agent.model.agentic.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;

@Service
public class ResearchServiceImpl implements ResearchService {

    // Keep these for deprecated methods
    private final ConcurrentMap<String, JobStatus> jobStatuses = new ConcurrentHashMap<>();
    private final ConcurrentMap<String, JobResult> jobResults = new ConcurrentHashMap<>();

    @Autowired
    private RestTemplate restTemplate;

    @Value("${agentic.service.url}")
    private String agenticServiceUrl;

    @Value("${agentic.service.poll.interval.ms}")
    private long pollIntervalMs;

    @Value("${agentic.service.poll.max.attempts}")
    private int pollMaxAttempts;

    @Override
    public JobResponse execute(ResearchRequest researchRequest) {
        String agenticJobId = null;

        try {
            // Step 1: Build agentic request
            AgenticResearchRequest agenticRequest = new AgenticResearchRequest();
            agenticRequest.setResearchGoal(researchRequest.getResearchGoal());

            if (researchRequest.getScopeParameters() != null) {
                AgenticScopeParameters agenticParams = new AgenticScopeParameters();
                ScopeParameters params = researchRequest.getScopeParameters();
                
                // Map temporalBoundary to timeRange (calculate years from current year - startYear)
                if (params.getTemporalBoundary() != null) {
                    int currentYear = java.time.Year.now().getValue();
                    int years = currentYear - params.getTemporalBoundary().getStartYear();
                    agenticParams.setTimeRange(years > 0 ? years : 3); // Default to 3 if invalid
                }
                
                // Map discoveryDepth to researchDepth
                agenticParams.setResearchDepth(params.getDiscoveryDepth());
                
                // Map qualityThreshold to sourceQuality (use publicationTier as quality indicator)
                if (params.getQualityThreshold() != null) {
                    agenticParams.setSourceQuality(params.getQualityThreshold().getPublicationTier());
                }
                
                // Map sourceDiversityRequirement to sourceDiversity
                agenticParams.setSourceDiversity(params.isSourceDiversityRequirement());
                
                agenticRequest.setScopeParameters(agenticParams);
            }

            // Step 2: POST to agentic service /api/agent/execute
            String executeUrl = agenticServiceUrl + "/api/agent/execute";
            AgenticJobResponse agenticResponse = restTemplate.postForObject(
                executeUrl,
                agenticRequest,
                AgenticJobResponse.class
            );

            if (agenticResponse == null || agenticResponse.getJobId() == null) {
                throw new RuntimeException("Failed to get job ID from agentic service");
            }

            agenticJobId = agenticResponse.getJobId();

            // Step 3: Poll for status until completed
            String statusUrl = agenticServiceUrl + "/api/agent/status/" + agenticJobId;
            AgenticJobStatus agenticStatus = null;
            int attempts = 0;

            while (attempts < pollMaxAttempts) {
                Thread.sleep(pollIntervalMs);
                attempts++;

                agenticStatus = restTemplate.getForObject(statusUrl, AgenticJobStatus.class);

                if (agenticStatus != null) {
                    // Check if completed
                    if ("COMPLETED".equalsIgnoreCase(agenticStatus.getStatus()) ||
                        "completed".equalsIgnoreCase(agenticStatus.getStatus())) {
                        break;
                    }

                    if ("FAILED".equalsIgnoreCase(agenticStatus.getStatus()) ||
                        "failed".equalsIgnoreCase(agenticStatus.getStatus())) {
                        throw new RuntimeException("Agentic service job failed");
                    }
                }
            }

            if (attempts >= pollMaxAttempts) {
                throw new RuntimeException("Timeout waiting for agentic service to complete");
            }

            // Step 4: Get results from agentic service
            String resultsUrl = agenticServiceUrl + "/api/agent/results/" + agenticJobId;
            Map<String, Object> synthesisResponse = restTemplate.getForObject(resultsUrl, Map.class);

            if (synthesisResponse == null) {
                throw new RuntimeException("Failed to get results from agentic service");
            }

            // Step 5: Build JobResponse with synthesis data directly
            JobResponse jobResponse = new JobResponse();
            jobResponse.setJobId(agenticJobId);
            jobResponse.setStatus("COMPLETED");
            
            // Store the synthesis response in the job response
            jobResponse.setSynthesis((Map<String, Object>) synthesisResponse.get("synthesis"));
            jobResponse.setExecutionSummary((Map<String, Object>) synthesisResponse.get("execution_summary"));
            jobResponse.setAuditTrailSummary((Map<String, Object>) synthesisResponse.get("audit_trail_summary"));

            return jobResponse;

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Request interrupted: " + e.getMessage(), e);
        } catch (Exception e) {
            throw new RuntimeException("Error executing research: " + e.getMessage(), e);
        }
    }

    /**
     * @deprecated This method is no longer needed as execute() now returns results synchronously
     */
    @Deprecated
    @Override
    public JobStatus getStatus(String jobId) {
        return jobStatuses.get(jobId);
    }

    /**
     * @deprecated This method is no longer needed as execute() now returns results synchronously
     */
    @Deprecated
    @Override
    public JobResult getResults(String jobId) {
        return jobResults.get(jobId);
    }
}
