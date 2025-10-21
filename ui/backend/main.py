"""
ComfyUI Workflow Builder - Web API
FastAPI backend server for the workflow builder UI
"""

import os
import sys
from pathlib import Path
from typing import Optional
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add builder path to Python path
BUILDER_PATH = os.getenv("BUILDER_PATH", "/home/user/comfywfbuilder2.0")
sys.path.insert(0, BUILDER_PATH)
sys.path.insert(0, os.path.join(BUILDER_PATH, "code_modules"))

# Import API routers
from api.workflows import router as workflows_router
from api.agents import router as agents_router
from api.models_api import router as models_router
from websocket.progress import manager as ws_manager

# Create FastAPI app
app = FastAPI(
    title="ComfyUI Workflow Builder API",
    description="API for generating ComfyUI workflows using natural language",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workflows_router, prefix="/api/workflows", tags=["workflows"])
app.include_router(agents_router, prefix="/api/agents", tags=["agents"])
app.include_router(models_router, prefix="/api/models", tags=["models"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "ComfyUI Workflow Builder API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "builder_path": BUILDER_PATH,
        "workspace_path": os.getenv("WORKSPACE_PATH"),
    }


@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    """WebSocket endpoint for real-time progress updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive client messages
            data = await websocket.receive_text()
            # Echo back for debugging
            await websocket.send_json({"type": "echo", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    print(f"Starting ComfyUI Workflow Builder API on {host}:{port}")
    print(f"Builder Path: {BUILDER_PATH}")
    print(f"Docs: http://localhost:{port}/api/docs")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
