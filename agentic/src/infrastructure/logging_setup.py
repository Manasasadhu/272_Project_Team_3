"""Logging configuration with Instana metrics monitoring"""
import logging
import sys
import os
import instana
from typing import Dict, Any

def setup_logging():
    """Setup structured logging with Instana integration"""
    # Initialize Instana monitoring for metrics
    instana.logger.init(log_level=logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_file = "server.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

# Metrics recording functions
def record_api_metric(endpoint: str, response_time: float, status_code: int):
    """Record API endpoint metrics"""
    instana.agent.get().custom_metrics.gauge(
        name=f"agentic.api.response_time",
        value=response_time,
        tags={"endpoint": endpoint, "status": status_code}
    )

def record_memory_metric(memory_usage: float):
    """Record memory usage metrics"""
    instana.agent.get().custom_metrics.gauge(
        name="agentic.memory.usage",
        value=memory_usage
    )

def record_llm_metric(model: str, tokens: int, duration: float):
    """Record LLM-related metrics"""
    instana.agent.get().custom_metrics.gauge(
        name="agentic.llm.usage",
        value=tokens,
        tags={"model": model}
    )
    instana.agent.get().custom_metrics.gauge(
        name="agentic.llm.duration",
        value=duration,
        tags={"model": model}
    )

