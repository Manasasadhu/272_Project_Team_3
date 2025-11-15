"""Tool registry"""
from typing import Dict
from tools.base_tool import BaseTool
from tools.search_tool import SearchTool
from tools.extraction_tool import ExtractionTool

class ToolRegistry:
    """Tool registration and factory"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        self.register("SearchTool", SearchTool())
        self.register("ExtractionTool", ExtractionTool())
    
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

