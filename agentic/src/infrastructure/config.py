"""Configuration management"""
import os
from typing import Optional

class Config:
    """Application configuration"""
    
    # LLM Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "models/gemini-2.5-flash")
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # ChromaDB Configuration (Optional)
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Agent Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "50"))
    CONTEXT_WINDOW_SIZE: int = int(os.getenv("CONTEXT_WINDOW_SIZE", "8000"))
    
    # Java Backend Tools Service Configuration
    JAVA_TOOLS_URL: str = os.getenv("JAVA_TOOLS_URL", "http://localhost:9000")
    JAVA_TOOLS_SEARCH_URL: str = os.getenv("JAVA_TOOLS_SEARCH_URL", os.getenv("JAVA_TOOLS_URL", "http://localhost:9000") + "/api/tools/search")
    JAVA_TOOLS_EXTRACT_URL: str = os.getenv("JAVA_TOOLS_EXTRACT_URL", os.getenv("JAVA_TOOLS_URL", "http://localhost:9000") + "/api/tools/extract")
    JAVA_TOOLS_SEARCH_TIMEOUT: float = float(os.getenv("JAVA_TOOLS_SEARCH_TIMEOUT", "30.0"))
    JAVA_TOOLS_EXTRACT_TIMEOUT: float = float(os.getenv("JAVA_TOOLS_EXTRACT_TIMEOUT", "60.0"))
    
    # Instana Configuration (Optional)
    INSTANA_AGENT_KEY: Optional[str] = os.getenv("INSTANA_AGENT_KEY", None)
    INSTANA_SERVICE_NAME: str = os.getenv("INSTANA_SERVICE_NAME", "agentic-research-service")
    INSTANA_ENABLED: bool = os.getenv("INSTANA_ENABLED", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return True

config = Config()

