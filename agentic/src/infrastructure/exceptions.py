"""Custom exceptions"""

class AgentExecutionError(Exception):
    """Base exception for agent execution errors"""
    pass

class ToolExecutionError(Exception):
    """Exception for tool execution failures"""
    pass

class GovernanceViolationError(Exception):
    """Exception for governance policy violations"""
    pass

class StorageError(Exception):
    """Exception for storage operations"""
    pass

