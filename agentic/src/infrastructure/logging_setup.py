"""Logging configuration with metrics"""
import logging
import sys
import os
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime

def setup_logging():
    """Setup structured logging"""
    log_file = "server.log"
    
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

# Simple in-memory metrics store
class MetricsCollector:
    """Lightweight metrics collector"""
    def __init__(self):
        self.api_calls = defaultdict(int)
        self.api_durations = defaultdict(list)
        self.llm_calls = 0
        self.llm_tokens = 0
        self.errors = defaultdict(int)
        
    def record_api(self, endpoint: str, duration: float, status: int):
        """Record API call"""
        self.api_calls[endpoint] += 1
        self.api_durations[endpoint].append(duration)
        if status >= 400:
            self.errors[endpoint] += 1
    
    def record_llm(self, tokens: int):
        """Record LLM usage"""
        self.llm_calls += 1
        self.llm_tokens += tokens
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            "total_api_calls": sum(self.api_calls.values()),
            "total_llm_calls": self.llm_calls,
            "total_llm_tokens": self.llm_tokens,
            "total_errors": sum(self.errors.values()),
            "endpoints": dict(self.api_calls)
        }

# Global metrics collector
metrics = MetricsCollector()

def record_api_metric(endpoint: str, response_time: float, status_code: int):
    """Record API endpoint metrics - logs to console/file + tracks metrics"""
    # Log (console + file)
    logger.info(f"API: {endpoint} | {status_code} | {response_time:.3f}s")
    
    # Track in-memory
    metrics.record_api(endpoint, response_time, status_code)
    
    # Note: Instana auto-instrumentation already captures all HTTP metrics
    # No need to manually send - it's already in the dashboard!

def record_memory_metric(memory_usage_mb: float):
    """Record memory usage metrics"""
    logger.info(f"Memory: {memory_usage_mb:.2f} MB")
    
    # Note: Instana agent already monitors system memory
    # This log is for local debugging

def record_llm_metric(model: str, tokens: int, duration: float):
    """Record LLM-related metrics"""
    logger.info(f"LLM: {model} | {tokens} tokens | {duration:.3f}s")
    
    # Track in-memory
    metrics.record_llm(tokens)
    
    # Add custom tags to current trace (visible in Instana trace details)
    try:
        from instana.singletons import tracer
        span = tracer.active_span
        if span:
            span.set_tag("llm.model", model)
            span.set_tag("llm.tokens", tokens)
            span.set_tag("llm.duration_seconds", duration)
    except:
        pass

def get_metrics_summary() -> Dict[str, Any]:
    """Get current metrics summary"""
    return metrics.get_summary()

