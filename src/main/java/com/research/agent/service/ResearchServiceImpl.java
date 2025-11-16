package com.research.agent.service;

import com.research.agent.model.*;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;

@Service
public class ResearchServiceImpl implements ResearchService {

    private final ConcurrentMap<String, JobResponse> jobResponses = new ConcurrentHashMap<>();
    private final ConcurrentMap<String, JobStatus> jobStatuses = new ConcurrentHashMap<>();
    private final ConcurrentMap<String, JobResult> jobResults = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newCachedThreadPool();

    @Override
    public JobResponse execute(ResearchRequest researchRequest) {
        String jobId = UUID.randomUUID().toString();

        JobResponse jobResponse = new JobResponse();
        jobResponse.setJobId(jobId);
        jobResponse.setStatus("INITIALIZED");

        AutonomousAnalysis autonomousAnalysis = new AutonomousAnalysis();
        // Basic placeholder analysis metadata
        autonomousAnalysis.setGoalDecomposition(new GoalDecomposition());
        autonomousAnalysis.setExecutionStrategy(new ExecutionStrategy());
        autonomousAnalysis.setGovernanceApplied(new GovernanceApplied());
        jobResponse.setAutonomousAnalysis(autonomousAnalysis);

        ExecutionPlan executionPlan = new ExecutionPlan();
        executionPlan.setEstimatedSources(30);
        executionPlan.setEstimatedDurationMinutes(2);
        jobResponse.setExecutionPlan(executionPlan);

        // persist initial status
        JobStatus initialStatus = new JobStatus();
        initialStatus.setJobId(jobId);
        initialStatus.setStatus("INITIALIZED");
        initialStatus.setCurrentPhase("Queued");
        initialStatus.setSourcesIdentifiedCount(0);
        initialStatus.setSourcesProcessedCount(0);

        jobResponses.put(jobId, jobResponse);
        jobStatuses.put(jobId, initialStatus);

        // Run asynchronous processing
        executor.submit(() -> runWorkflow(jobId));

        return jobResponse;
    }

    private void runWorkflow(String jobId) {
        JobStatus status = jobStatuses.get(jobId);
        try {
            status.setStatus("IN_PROGRESS");
            status.setCurrentPhase("Autonomous Exploration");
            jobStatuses.put(jobId, status);

            // Simulate search phase
            Thread.sleep(1000);
            status.setSourcesIdentifiedCount(25);
            jobStatuses.put(jobId, status);

            // Simulate extraction phase processing multiple sources
            status.setCurrentPhase("EXTRACTING");
            jobStatuses.put(jobId, status);
            for (int i = 1; i <= 9; i++) {
                Thread.sleep(500); // simulate per-source processing
                status.setSourcesProcessedCount(i);
                jobStatuses.put(jobId, status);
            }

            // Simulate analysis/synthesis
            status.setCurrentPhase("Meta-Analysis & Synthesis");
            jobStatuses.put(jobId, status);
            Thread.sleep(800);

            // Build final result (mocked)
            JobResult result = new JobResult();
            result.setJobId(jobId);
            result.setStatus("COMPLETED");

            ExecutiveSummary summary = new ExecutiveSummary();
            summary.setSummaryText("Mock executive summary generated at " + Instant.now().toString());
            result.setExecutiveSummary(summary);

            List<Source> sources = new ArrayList<>();
            for (int i = 0; i < 9; i++) {
                Source s = new Source();
                s.setUrl("https://example.org/paper/" + (i + 1));
                s.setTitle("Mock Paper " + (i + 1));
                sources.add(s);
            }
            result.setSources(sources);

            DetailedAnalysis detailed = new DetailedAnalysis();
            detailed.setSummary("Detailed mock analysis");
            result.setDetailedAnalysis(detailed);

            jobResults.put(jobId, result);

            status.setStatus("COMPLETED");
            jobStatuses.put(jobId, status);

        } catch (InterruptedException e) {
            status.setStatus("FAILED");
            jobStatuses.put(jobId, status);
            Thread.currentThread().interrupt();
        } catch (Exception e) {
            status.setStatus("FAILED");
            jobStatuses.put(jobId, status);
        }
    }

    @Override
    public JobStatus getStatus(String jobId) {
        return jobStatuses.get(jobId);
    }

    @Override
    public JobResult getResults(String jobId) {
        return jobResults.get(jobId);
    }
}
