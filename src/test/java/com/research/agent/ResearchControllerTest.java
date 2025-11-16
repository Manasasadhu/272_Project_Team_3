//package com.research.agent;
//
//import com.fasterxml.jackson.databind.ObjectMapper;
//import com.research.agent.controller.ResearchAgentController;
//import com.research.agent.model.ResearchRequest;
//import com.research.agent.service.ResearchService;
//import org.junit.jupiter.api.Test;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
//import org.springframework.boot.test.mock.mockito.MockBean;
//import org.springframework.http.MediaType;
//import org.springframework.test.web.servlet.MockMvc;
//
//import java.util.Map;
//import java.util.UUID;
//
//import static org.mockito.ArgumentMatchers.any;
//import static org.mockito.Mockito.when;
//import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
//import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
//import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
//import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
//
//@WebMvcTest(ResearchAgentController.class)
//public class ResearchControllerTest {
//
//    @Autowired
//    private MockMvc mockMvc;
//
//    @MockBean
//    private ResearchService researchService;
//
//    @Autowired
//    private ObjectMapper objectMapper;
//
//    @Test
//    public void testExecute() throws Exception {
//        ResearchRequest researchRequest = new ResearchRequest();
//        researchRequest.setResearchGoal("What are recent advances in transformer architectures?");
//
//        String researchId = UUID.randomUUID().toString();
//        when(researchService.startResearch(any(ResearchRequest.class))).thenReturn(researchId);
//
//        mockMvc.perform(post("/api/agent/execute")
//                .contentType(MediaType.APPLICATION_JSON)
//                .content(objectMapper.writeValueAsString(researchRequest)))
//                .andExpect(status().isOk())
//                .andExpect(jsonPath("$.research_id").value(researchId));
//    }
//
//    @Test
//    public void testGetStatus() throws Exception {
//        String researchId = "123";
//        Map<String, Object> status = Map.of("status", "IN_PROGRESS");
//        when(researchService.getStatus(researchId)).thenReturn(status);
//
//        mockMvc.perform(get("/api/agent/status/" + researchId))
//                .andExpect(status().isOk())
//                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
//    }
//
//    @Test
//    public void testGetResults() throws Exception {
//        String researchId = "123";
//        Map<String, Object> results = Map.of("status", "COMPLETED");
//        when(researchService.getResults(researchId)).thenReturn(results);
//
//        mockMvc.perform(get("/api/agent/results/" + researchId))
//                .andExpect(status().isOk())
//                .andExpect(jsonPath("$.status").value("COMPLETED"));
//    }
//}
