"""Tool registry"""
import logging
import httpx
from typing import Dict
from tools.base_tool import BaseTool
from tools.search_tool import SearchTool
from tools.extraction_tool import ExtractionTool
from infrastructure.config import config

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Tool registration and factory with health checking"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        self.register("search_papers", SearchTool())
        self.register("extract_paper", ExtractionTool())
    
    def register(self, name: str, tool: BaseTool):
        """Register a tool"""
        self.tools[name] = tool
    
    def get_tool(self, name: str) -> BaseTool:
        """Get tool by name"""
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name]
    
    def list_tools(self) -> list:
        """List all registered tools"""
        return list(self.tools.keys())
    
    def check_java_backend_health(self) -> Dict[str, bool]:
        """
        Check Java backend service health
        
        Returns:
            Dict with health status including search, extract, and overall connectivity
        """
        health_status = {
            "backend_reachable": False,
            "search_available": False,
            "extract_available": False
        }
        
        try:
            health_endpoint = f"{config.JAVA_TOOLS_URL}/api/tools/health"
            logger.debug(f"Checking Java backend health: {health_endpoint}")
            
            with httpx.Client() as client:
                response = client.get(health_endpoint, timeout=5.0)
                response.raise_for_status()
                
                data = response.json()
                health_status["backend_reachable"] = True
                health_status["search_available"] = True  # Both endpoints available if backend is up
                health_status["extract_available"] = True
                
                logger.info(f"Java backend health check passed: {data}")
                
        except httpx.TimeoutException:
            logger.warning(f"Java backend health check timeout at {config.JAVA_TOOLS_URL}")
        except httpx.ConnectError:
            logger.warning(f"Cannot connect to Java backend at {config.JAVA_TOOLS_URL}")
        except Exception as e:
            logger.warning(f"Java backend health check failed: {str(e)}")
        
        return health_status
    
    def get_tools_info(self) -> Dict:
        """
        Get comprehensive information about registered tools
        
        Returns:
            Dict with tool names, descriptions, and backend status
        """
        backend_health = self.check_java_backend_health()
        
        return {
            "registered_tools": self.list_tools(),
            "backend_config": {
                "url": config.JAVA_TOOLS_URL,
                "search_timeout": config.JAVA_TOOLS_SEARCH_TIMEOUT,
                "extract_timeout": config.JAVA_TOOLS_EXTRACT_TIMEOUT
            },
            "backend_health": backend_health,
            "tools": {
                "search_papers": {
                    "name": "search_papers",
                    "description": "Search for academic papers using OpenAlex API",
                    "expected_params": ["query", "max_results"],
                    "available": backend_health.get("search_available", False)
                },
                "extract_paper": {
                    "name": "extract_paper",
                    "description": "Extract structured content from papers (ArXiv, DOI, PDF)",
                    "expected_params": ["source_url"],
                    "available": backend_health.get("extract_available", False)
                }
            }
        }
