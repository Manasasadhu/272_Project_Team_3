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
import static org.mockito.Mockito.verify;
import org.mockito.ArgumentCaptor;
import static org.assertj.core.api.Assertions.assertThat;

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

    @Test
    public void extractPassesExtractionParametersThrough() throws Exception {
        Map<String, Object> fake = Map.of("extracted_content", Map.of("key_findings", Map.of()), "metadata", Map.of("extraction_success", true));
        when(toolsService.extract(org.mockito.ArgumentMatchers.anyMap())).thenReturn(fake);
        String req = "{\"source\":\"https://example.com/a.pdf\", \"extraction_parameters\": {\"required_elements\": [\"key_findings\", \"methodology\"]}}";
        mockMvc.perform(post("/api/tools/extract").contentType(APPLICATION_JSON_VALUE).content(req)).andExpect(status().isOk()).andExpect(content().json("{" + "\"metadata\":{\"extraction_success\":true}" + "}"));
        ArgumentCaptor<Map<String, Object>> captor = ArgumentCaptor.forClass(Map.class);
        verify(toolsService).extract(captor.capture());
        Map<String, Object> captured = captor.getValue();
        assertThat(captured).containsKey("extraction_parameters");
        Object ext = captured.get("extraction_parameters");
        assertThat(ext).isNotNull();
        assertThat(ext.toString()).contains("key_findings");
    }
}
