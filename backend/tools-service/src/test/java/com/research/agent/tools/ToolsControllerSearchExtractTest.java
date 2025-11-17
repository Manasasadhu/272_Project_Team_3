package com.research.agent.tools;

import com.research.agent.tools.controllers.ToolsController;
import com.research.agent.tools.services.ToolsService;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;
import java.util.Map;

@WebMvcTest(ToolsController.class)
public class ToolsControllerSearchExtractTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ToolsService toolsService;

    @Test
    public void searchReturns200() throws Exception {
        when(toolsService.search(Map.of("query","ml"))).thenReturn(Map.of("results", Map.of()));
        mockMvc.perform(post("/api/tools/search").contentType(APPLICATION_JSON_VALUE).content("{\"query\":\"ml\"}"))
            .andExpect(status().isOk());
    }

    @Test
    public void extractReturns200() throws Exception {
        when(toolsService.extract(Map.of("source","https://example.com/a.pdf"))).thenReturn(Map.of("source","https://example.com/a.pdf"));
        mockMvc.perform(post("/api/tools/extract").contentType(APPLICATION_JSON_VALUE).content("{\"source\":\"https://example.com/a.pdf\"}"))
            .andExpect(status().isOk());
    }
}
