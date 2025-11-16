package com.research.agent.service;

import com.research.agent.model.JobResponse;
import com.research.agent.model.JobStatus;
import com.research.agent.model.JobResult;
import com.research.agent.model.ResearchRequest;

public interface ResearchService {

    JobResponse execute(ResearchRequest researchRequest);

    JobStatus getStatus(String jobId);

    JobResult getResults(String jobId);
}
