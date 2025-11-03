"""Tool executor"""
from typing import Dict, Any
from tools.base_tool import BaseTool, ToolResult
from tools.tool_registry import ToolRegistry
from infrastructure.exceptions import ToolExecutionError

class Executor:
    """Execute tools and manage results"""
    
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """Execute tool by name"""
        tool = self.tool_registry.get_tool(tool_name)
        return tool.execute(params)
    
    def handle_failure(self, result: ToolResult, context: str = "") -> bool:
        """Handle tool execution failure"""
        if not result.success:
            # Log failure but continue execution
            return False  # Indicates should continue
        return True

