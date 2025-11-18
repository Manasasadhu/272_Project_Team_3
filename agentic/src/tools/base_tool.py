"""Base tool interface"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class ToolResult:
    """Tool execution result"""
    def __init__(self, success: bool, data: Any = None, error: str = None, metadata: Dict = None):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}

class BaseTool(ABC):
    """Abstract base tool"""
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> ToolResult:
        """Execute tool with parameters"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get tool name"""
        pass

