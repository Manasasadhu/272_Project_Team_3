package com.research.agent.tools.services;

import java.util.Map;

public interface ToolsService {
    boolean checkGrobidReachable();
    boolean checkOpenAlexReachable();
    Map<String, Object> search(Map<String, Object> request);
    Map<String, Object> extract(Map<String, Object> request);
}
