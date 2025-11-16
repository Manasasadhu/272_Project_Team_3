"""Main FastAPI application with Instana monitoring"""
import os
import time
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Set Instana env vars BEFORE importing anything
# This is required for Instana's auto-instrumentation to work
from infrastructure.config import config
instana_enabled = False
if config.INSTANA_ENABLED and config.INSTANA_AGENT_KEY:
    os.environ["INSTANA_AGENT_KEY"] = config.INSTANA_AGENT_KEY
    os.environ["INSTANA_SERVICE_NAME"] = config.INSTANA_SERVICE_NAME
    # For SaaS direct connection (serverless mode)
    os.environ["INSTANA_ENDPOINT_URL"] = "https://ingress-pumpkin-saas.instana.io"
    os.environ["INSTANA_ENDPOINT_PORT"] = "443"
    try:
        import instana  # Auto-instrumentation activates on import
        instana_enabled = True
    except Exception as e:
        # Instana not installed or failed - continue without it
        instana_enabled = False

# Now import FastAPI and other modules (after Instana is initialized)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from infrastructure.logging_setup import logger, set_prometheus_metrics

# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY

# Define metrics (using default REGISTRY)
request_count = Counter(
    'agentic_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'agentic_http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

llm_calls = Counter(
    'agentic_llm_calls_total',
    'Total LLM API calls',
    ['model', 'status']
)

llm_tokens = Counter(
    'agentic_llm_tokens_total',
    'Total LLM tokens used',
    ['model']
)

# Register LLM metrics with logging setup so it can record them
set_prometheus_metrics(llm_calls, llm_tokens)

active_jobs = Gauge(
    'agentic_active_jobs',
    'Number of active research jobs'
)

# Redis and ChromaDB performance metrics
redis_latency = Histogram(
    'agentic_redis_operation_duration_seconds',
    'Redis operation latency',
    ['operation']
)

redis_memory = Gauge(
    'agentic_redis_memory_bytes',
    'Redis memory usage in bytes'
)

chromadb_query_latency = Histogram(
    'agentic_chromadb_query_duration_seconds',
    'ChromaDB query latency',
    ['operation']
)

# Latency by endpoint (for better endpoint-specific tracking)
endpoint_latency = Histogram(
    'agentic_http_endpoint_latency_seconds',
    'HTTP endpoint latency distribution',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

if instana_enabled:
    logger.info(f"Instana initialized: {config.INSTANA_SERVICE_NAME}")
else:
    logger.info("Instana disabled or not available")

# Validate config (warn but don't fail)
try:
    config.validate()
except ValueError as e:
    logger.warning(f"Configuration warning: {e}")

# Create FastAPI app
app = FastAPI(
    title="Goal-Oriented Knowledge Discovery Agent",
    description="Autonomous agentic server for knowledge discovery",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Track API metrics - logs to console/file + sends to Instana"""
    start_time = time.time()
    
    # Add custom span tags if Instana is enabled
    if instana_enabled:
        try:
            from instana.singletons import tracer
            span = tracer.active_span
            if span:
                span.set_tag("research.endpoint", request.url.path)
                span.set_tag("research.method", request.method)
        except:
            pass
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Record Prometheus metrics
    try:
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        # Record endpoint-specific latency distribution
        endpoint_latency.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
    except Exception as e:
        logger.error(f"Error recording Prometheus metrics: {e}")
    
    # Use existing record_api_metric (handles logging + metrics + Instana)
    from infrastructure.logging_setup import record_api_metric
    record_api_metric(f"{request.method} {request.url.path}", duration, response.status_code)
    
    return response

# Include routes
app.include_router(router)

# Prometheus metrics endpoint
@app.get("/metrics", response_class=None)
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, REGISTRY
    from fastapi.responses import Response
    
    return Response(
        content=generate_latest(REGISTRY),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("=== Agentic Server Starting ===")
    logger.info(f"Redis: {config.REDIS_HOST}:{config.REDIS_PORT}")
    logger.info(f"LLM Model: {config.LLM_MODEL}")
    logger.info(f"Instana: {'Enabled' if instana_enabled else 'Disabled'}")
    
    # Start background task for monitoring Redis and ChromaDB
    import asyncio
    asyncio.create_task(monitor_infrastructure_health())

async def monitor_infrastructure_health():
    """Background task to monitor Redis and ChromaDB health"""
    import asyncio
    while True:
        try:
            # Monitor Redis
            try:
                from infrastructure.redis_storage import RedisStorage
                storage = RedisStorage()
                start = time.time()
                storage.client.ping()
                latency = time.time() - start
                redis_latency.labels(operation='ping').observe(latency)
                
                # Get Redis memory info
                info = storage.client.info('memory')
                redis_memory.set(info.get('used_memory', 0))
            except Exception as e:
                logger.warning(f"Redis health check failed: {e}")
            
            # Monitor ChromaDB (via a simple query)
            try:
                import httpx
                start = time.time()
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"http://{config.CHROMA_HOST}:{config.CHROMA_PORT}/api/v1/version",
                        timeout=5.0
                    )
                latency = time.time() - start
                chromadb_query_latency.labels(operation='health_check').observe(latency)
            except Exception as e:
                logger.warning(f"ChromaDB health check failed: {e}")
            
            # Check every 30 seconds
            await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Infrastructure health monitoring error: {e}")
            await asyncio.sleep(30)

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("=== Agentic Server Shutting Down ===")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

