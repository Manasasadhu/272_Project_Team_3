package com.research.agent.tools;

import com.research.agent.tools.controllers.ToolsController;
import com.research.agent.tools.services.ToolsService;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(ToolsController.class)
public class ToolsControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ToolsService toolsService;

    @Test
    public void healthEndpointReturns200() throws Exception {
        when(toolsService.checkGrobidReachable()).thenReturn(true);
        when(toolsService.checkOpenAlexReachable()).thenReturn(true);
        mockMvc.perform(get("/api/tools/health")).andExpect(status().isOk());
    }
}
