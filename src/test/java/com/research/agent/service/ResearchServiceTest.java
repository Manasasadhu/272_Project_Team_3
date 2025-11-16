//package com.research.agent.service;
//
//import com.research.agent.model.ResearchRequest;
//import com.research.agent.repository.ResearchRepository;
//import org.junit.jupiter.api.Test;
//import org.junit.jupiter.api.extension.ExtendWith;
//import org.mockito.InjectMocks;
//import org.mockito.Mock;
//import org.mockito.junit.jupiter.MockitoExtension;
//
//import java.util.Map;
//
//import static org.junit.jupiter.api.Assertions.assertEquals;
//import static org.junit.jupiter.api.Assertions.assertNotNull;
//
//@ExtendWith(MockitoExtension.class)
//public class ResearchServiceTest {
//
//    @InjectMocks
//    private ResearchService researchService;
//
//    @Mock
//    private ResearchRepository researchRepository;
//
//    @Test
//    public void testStartResearch() {
//        ResearchRequest researchRequest = new ResearchRequest();
//        researchRequest.setResearchGoal("What are recent advances in transformer architectures?");
//        String researchId = researchService.startResearch(researchRequest);
//        assertNotNull(researchId);
//    }
//
//    @Test
//    public void testGetStatus() {
//        Map<String, Object> status = researchService.getStatus("123");
//        assertEquals("IN_PROGRESS", status.get("status"));
//    }
//
//    @Test
//    public void testGetResults() {
//        Map<String, Object> results = researchService.getResults("123");
//        assertEquals("COMPLETED", results.get("status"));
//    }
//}
