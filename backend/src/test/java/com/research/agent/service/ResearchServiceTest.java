package com.research.agent.service;

import com.research.agent.model.JobResponse;
import com.research.agent.model.JobStatus;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

public class ResearchServiceTest {

	@Test
	public void testExecuteAndStatus() {
		ResearchServiceImpl service = new ResearchServiceImpl();
		// Arrange
		var req = new com.research.agent.model.ResearchRequest();
		req.setResearchGoal("What are recent advances in transformer architectures?");

		// Act
		JobResponse resp = service.execute(req);
		assertNotNull(resp.getJobId());

		// Immediately after execute, status should be INITIALIZED
		JobStatus status = service.getStatus(resp.getJobId());
		assertNotNull(status);
		assertEquals("INITIALIZED", status.getStatus());
	}

	@Test
	@Timeout(value = 15)
	public void testWorkflowCompletes() {
		ResearchServiceImpl service = new ResearchServiceImpl();
		var req = new com.research.agent.model.ResearchRequest();
		req.setResearchGoal("What are recent advances in transformer architectures?");
		JobResponse resp = service.execute(req);
		assertNotNull(resp.getJobId());

		// Wait for completion (service's internal sleeps are approx 6s). Give 12s max.
		long start = System.currentTimeMillis();
		while (System.currentTimeMillis() - start < Duration.ofSeconds(12).toMillis()) {
			JobStatus st = service.getStatus(resp.getJobId());
			if (st != null && "COMPLETED".equals(st.getStatus())) {
				break;
			}
			try { Thread.sleep(200); } catch (InterruptedException ie) { Thread.currentThread().interrupt(); break; }
		}

		JobStatus finalStatus = service.getStatus(resp.getJobId());
		assertNotNull(finalStatus);
		assertEquals("COMPLETED", finalStatus.getStatus());
	}
}
