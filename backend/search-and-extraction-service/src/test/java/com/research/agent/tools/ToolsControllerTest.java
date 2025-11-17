package com.research.agent.tools;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(ToolsController.class)
public class ToolsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private RestTemplate restTemplate;

    private static final String OPENALEX_WORKS_URL = "https://api.openalex.org/works";
    private static final String GROBIG_BASE = "http://localhost:8070";

    @BeforeEach
    public void setup() {
        // Base health mocks
        when(restTemplate.getForEntity(any(String.class), eq(String.class)))
                .thenReturn(new ResponseEntity<>("{}", HttpStatus.OK));
        when(restTemplate.getForEntity(any(String.class), eq(String.class)))
                .thenReturn(new ResponseEntity<>("OK", HttpStatus.OK));
    }

    @Test
    public void testSearch() throws Exception {
        Map<String, Object> request = Map.of(
                "query", "artificial intelligence trends",
                "max_results", 20
        );

        // Mock OpenAlex response
        Map<String, Object> meta = new HashMap<>();
        meta.put("query_time_ms", 100);
        Map<String, Object> hit = Map.of("title", "Test paper", "abstract", "An abstract", "score", 1.0);
        Map<String, Object> body = Map.of("meta", meta, "results", Collections.singletonList(hit));
        when(restTemplate.getForEntity(any(String.class), eq(Map.class))).thenReturn(new ResponseEntity<>(body, HttpStatus.OK));

        mockMvc.perform(post("/api/tools/search")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.results").isArray());
    }

    @Test
    public void testExtract() throws Exception {
        Map<String, Object> request = Map.of(
                "source_url", "https://arxiv.org/abs/2401.12345"
        );

        // Mock arXiv XML response
        String xml = "<feed><entry><title>Arxiv Title</title><summary>arxiv abstract here.</summary></entry></feed>";
        when(restTemplate.getForEntity(any(String.class), eq(String.class))).thenReturn(new ResponseEntity<>(xml, HttpStatus.OK));

        mockMvc.perform(post("/api/tools/extract")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.extracted_content.title").value("Arxiv Title"))
                .andExpect(jsonPath("$.extracted_content.abstract").value("arxiv abstract here."));
    }

    @Test
    public void testHealth() throws Exception {
        mockMvc.perform(get("/api/tools/health")).andExpect(status().isOk())
                .andExpect(jsonPath("$.service").value("ok"))
                .andExpect(jsonPath("$.openalex").value(true));
    }
}
