
package com.research.agent.controller;

import com.research.agent.model.JobResponse;
import com.research.agent.model.JobStatus;
import com.research.agent.model.JobResult;
import com.research.agent.model.ResearchRequest;
import com.research.agent.service.ResearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/agent")
@CrossOrigin(origins = "*", maxAge = 3600)
public class ResearchAgentController {

    private final ResearchService researchService;

    @Autowired
    public ResearchAgentController(ResearchService researchService) {
        this.researchService = researchService;
    }

    @PostMapping("/execute")
    public ResponseEntity<JobResponse> execute(@RequestBody ResearchRequest researchRequest) {
        // Basic validation according to API spec: research_goal required, 10-500 chars
        if (researchRequest == null || researchRequest.getResearchGoal() == null) {
            return ResponseEntity.badRequest().build();
        }
        String goal = researchRequest.getResearchGoal().trim();
        if (goal.length() < 10 || goal.length() > 500) {
            return ResponseEntity.badRequest().build();
        }

        JobResponse resp = researchService.execute(researchRequest);
        // Return 202 Accepted since processing is asynchronous
        return ResponseEntity.accepted().body(resp);
    }

    @GetMapping("/status/{job_id}")
    public ResponseEntity<JobStatus> getStatus(@PathVariable("job_id") String jobId) {
        JobStatus status = researchService.getStatus(jobId);
        if (status == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(status);
    }

    @GetMapping("/results/{job_id}")
    public ResponseEntity<JobResult> getResults(@PathVariable("job_id") String jobId) {
        JobResult result = researchService.getResults(jobId);
        if (result == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(result);
    }
}
