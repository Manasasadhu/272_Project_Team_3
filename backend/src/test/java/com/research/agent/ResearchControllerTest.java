package com.research.agent;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.research.agent.controller.ResearchAgentController;
import com.research.agent.model.ResearchRequest;
import com.research.agent.service.ResearchService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Map;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(ResearchAgentController.class)
public class ResearchControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ResearchService researchService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testExecute() throws Exception {
        ResearchRequest researchRequest = new ResearchRequest();
        researchRequest.setResearchGoal("What are recent advances in transformer architectures?");

        com.research.agent.model.JobResponse jr = new com.research.agent.model.JobResponse();
        jr.setJobId("job-123");
        when(researchService.execute(any(ResearchRequest.class))).thenReturn(jr);

        mockMvc.perform(post("/api/agent/execute")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(researchRequest)))
            .andExpect(status().isAccepted());
    }

    @Test
    public void testGetStatus() throws Exception {
        com.research.agent.model.JobStatus js = new com.research.agent.model.JobStatus();
        js.setJobId("123");
        js.setStatus("IN_PROGRESS");
        when(researchService.getStatus("123")).thenReturn(js);

        mockMvc.perform(get("/api/agent/status/123"))
                .andExpect(status().isOk());
    }

    @Test
    public void testGetResults() throws Exception {
        com.research.agent.model.JobResult jr2 = new com.research.agent.model.JobResult();
        jr2.setJobId("123");
        jr2.setStatus("COMPLETED");
        when(researchService.getResults("123")).thenReturn(jr2);

        mockMvc.perform(get("/api/agent/results/123"))
                .andExpect(status().isOk());
    }
}
