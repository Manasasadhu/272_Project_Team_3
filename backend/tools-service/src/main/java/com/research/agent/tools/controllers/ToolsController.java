package com.research.agent.tools.controllers;

import com.research.agent.tools.services.ToolsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/tools")
public class ToolsController {
    private final ToolsService toolsService;

    @Autowired
    public ToolsController(ToolsService toolsService) {
        this.toolsService = toolsService;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(Map.of(
                "service", "tools",
                "grobid", toolsService.checkGrobidReachable(),
                "openalex", toolsService.checkOpenAlexReachable()
        ));
    }

    @GetMapping("/health/grobid")
    public ResponseEntity<Map<String, Object>> healthGrobid() {
        boolean up = toolsService.checkGrobidReachable();
        return ResponseEntity.ok(Map.of("service", "grobid", "up", up));
    }

    @GetMapping("/health/openalex")
    public ResponseEntity<Map<String, Object>> healthOpenAlex() {
        boolean up = toolsService.checkOpenAlexReachable();
        return ResponseEntity.ok(Map.of("service", "openalex", "up", up));
    }

    @PostMapping("/search")
    public ResponseEntity<Map<String, Object>> search(@RequestBody Map<String, Object> request) {
        Map<String, Object> response = toolsService.search(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/extract")
    public ResponseEntity<Map<String, Object>> extract(@RequestBody Map<String, Object> request) {
        Map<String, Object> response = toolsService.extract(request);
        return ResponseEntity.ok(response);
    }
}
