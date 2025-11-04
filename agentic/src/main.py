"""Main FastAPI application with metrics monitoring"""
import os
import time
import psutil
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from infrastructure.config import config
from infrastructure.logging_setup import (
    logger, 
    record_api_metric,
    record_memory_metric
)

# Load environment variables
load_dotenv()

# Validate config (warn but don't fail)
try:
    config.validate()
except ValueError as e:
    logger.warning(f"Configuration warning: {e}. Server will start but some features may not work.")

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

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Agentic server starting up...")
    logger.info(f"Redis: {config.REDIS_HOST}:{config.REDIS_PORT}")
    logger.info(f"LLM Model: {config.LLM_MODEL}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Agentic server shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

