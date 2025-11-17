package com.research.agent.tools;

import com.research.agent.tools.services.ToolsServiceImpl;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class ToolsServiceImplTest {

    @Test
    public void testExtractFallbackFiltering() {
        ToolsServiceImpl svc = new ToolsServiceImpl();
        Map<String, Object> request = Map.of(
                "source", "not-a-real-source",
                "extraction_parameters", Map.of("required_elements", List.of("key_findings", "methodology"))
        );
        Map<String, Object> resp = svc.extract(request);
        assertNotNull(resp);
        Map<String, Object> extracted = (Map<String, Object>) resp.get("extracted_content");
        assertNotNull(extracted);
        // only requested elements should be present
        assertTrue(extracted.containsKey("key_findings"));
        assertTrue(extracted.containsKey("methodology"));
        assertFalse(extracted.containsKey("title"));
        assertFalse(extracted.containsKey("abstract"));
        assertFalse(extracted.containsKey("citations"));
    }

    @Test
    public void testExtractFallbackNoParamsReturnsAll() {
        ToolsServiceImpl svc = new ToolsServiceImpl();
        Map<String, Object> request = Map.of("source", "not-a-real-source");
        Map<String, Object> resp = svc.extract(request);
        assertNotNull(resp);
        Map<String, Object> extracted = (Map<String, Object>) resp.get("extracted_content");
        assertNotNull(extracted);
        assertTrue(extracted.containsKey("title"));
        assertTrue(extracted.containsKey("abstract"));
        assertTrue(extracted.containsKey("key_findings"));
        assertTrue(extracted.containsKey("methodology"));
        assertTrue(extracted.containsKey("citations"));
        assertTrue(extracted.containsKey("authors") || extracted.containsKey("citations"));
    }
}
