"""Logging configuration with metrics"""
import logging
import sys
import os
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime
import json
import requests
import threading

# Loki configuration
LOKI_URL = os.getenv("LOKI_URL", "http://loki:3100/loki/api/v1/push")

class LokiHandler(logging.Handler):
    """Send logs to Loki"""
    def __init__(self, url: str, labels: dict):
        super().__init__()
        self.url = url
        self.labels = labels
        self.batch = []
        self.batch_lock = threading.Lock()
        self.last_flush = datetime.now()
        
    def emit(self, record: logging.LogRecord):
        """Send log to Loki"""
        try:
            log_entry = self.format(record)
            timestamp_ns = int(record.created * 1e9)
            
            # Batch logs to reduce requests
            with self.batch_lock:
                self.batch.append((timestamp_ns, log_entry))
                
                # Send when batch reaches 5 OR every 10 seconds
                should_flush = len(self.batch) >= 5
                time_since_flush = (datetime.now() - self.last_flush).total_seconds()
                if time_since_flush > 10:
                    should_flush = True
                
                if should_flush and self.batch:
                    self._send_batch()
        except Exception as e:
            pass  # Silently fail
    
    def _send_batch(self):
        """Send batched logs to Loki"""
        if not self.batch:
            return
            
        try:
            # Format for Loki
            values = [[str(ts), msg] for ts, msg in self.batch]
            
            payload = {
                "streams": [
                    {
                        "stream": self.labels,  # Send as dict
                        "values": values
                    }
                ]
            }
            
            response = requests.post(self.url, json=payload, timeout=2)
            self.batch.clear()
            self.last_flush = datetime.now()
        except Exception as e:
            pass  # Silently fail to not block logging
    
    def flush(self):
        """Flush remaining logs on shutdown"""
        with self.batch_lock:
            if self.batch:
                self._send_batch()

def setup_logging():
    """Setup structured logging"""
    log_file = "server.log"
    
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file)
    ]
    
    # Add Loki handler if available
    try:
        loki_handler = LokiHandler(
            LOKI_URL,
            {
                "job": "agentic-server",
                "service": "research-api",
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        )
        loki_handler.setLevel(logging.INFO)
        handlers.append(loki_handler)
    except Exception as e:
        pass  # Loki not available, continue without it
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
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

# Global Prometheus metric objects (will be set by main.py)
_prometheus_llm_calls = None
_prometheus_llm_tokens = None

def set_prometheus_metrics(llm_calls, llm_tokens):
    """Set Prometheus metric objects for LLM tracking"""
    global _prometheus_llm_calls, _prometheus_llm_tokens
    _prometheus_llm_calls = llm_calls
    _prometheus_llm_tokens = llm_tokens

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
    
    # Record Prometheus metrics if available
    if _prometheus_llm_calls and _prometheus_llm_tokens:
        try:
            status = "success" if tokens > 0 else "error"
            _prometheus_llm_calls.labels(model=model, status=status).inc()
            _prometheus_llm_tokens.labels(model=model).inc(tokens)
        except Exception as e:
            logger.debug(f"Failed to record Prometheus LLM metrics: {e}")
    
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

