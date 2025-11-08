"""Logging configuration"""
import logging
import sys
import os
from typing import Dict, Any

def setup_logging():
    """Setup structured logging"""
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
    logger.info(f"API Metric - Endpoint: {endpoint}, Response Time: {response_time}s, Status: {status_code}")

def record_memory_metric(memory_usage: float):
    """Record memory usage metrics"""
    logger.info(f"Memory Usage Metric: {memory_usage}")

def record_llm_metric(model: str, tokens: int, duration: float):
    """Record LLM-related metrics"""
    logger.info(f"LLM Metric - Model: {model}, Tokens: {tokens}, Duration: {duration}s")

