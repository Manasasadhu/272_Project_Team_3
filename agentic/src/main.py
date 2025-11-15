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
from infrastructure.logging_setup import logger

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
    
    # Use existing record_api_metric (handles logging + metrics + Instana)
    from infrastructure.logging_setup import record_api_metric
    record_api_metric(f"{request.method} {request.url.path}", duration, response.status_code)
    
    return response

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("=== Agentic Server Starting ===")
    logger.info(f"Redis: {config.REDIS_HOST}:{config.REDIS_PORT}")
    logger.info(f"LLM Model: {config.LLM_MODEL}")
    logger.info(f"Instana: {'Enabled' if instana_enabled else 'Disabled'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("=== Agentic Server Shutting Down ===")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

