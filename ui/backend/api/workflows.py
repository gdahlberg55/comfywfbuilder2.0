"""
Workflows API endpoints
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from models.workflow import (
    WorkflowRequest,
    WorkflowResponse,
    WorkflowHistory,
    WorkflowStatus,
)
from services.workflow_generator import WorkflowGenerator
from websocket.progress import manager as ws_manager

router = APIRouter()

# In-memory storage (replace with database in production)
workflows_db: dict = {}


@router.post("/generate", response_model=WorkflowResponse)
async def generate_workflow(
    request: WorkflowRequest, background_tasks: BackgroundTasks
):
    """
    Generate a new ComfyUI workflow from natural language description

    This endpoint initiates the workflow generation process using the
    orchestrator and specialized agents.
    """
    # Create workflow ID
    workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create initial response
    workflow_response = WorkflowResponse(
        id=workflow_id,
        status=WorkflowStatus.PENDING,
        created_at=datetime.now(),
        metadata={
            "description": request.description,
            "model_type": request.model_type,
            "dimensions": f"{request.width}x{request.height}",
        },
    )

    # Store in database
    workflows_db[workflow_id] = workflow_response

    # Start generation in background
    background_tasks.add_task(
        generate_workflow_task, workflow_id, request, ws_manager
    )

    return workflow_response


async def generate_workflow_task(
    workflow_id: str, request: WorkflowRequest, ws_manager
):
    """Background task to generate workflow"""
    try:
        # Update status
        workflows_db[workflow_id].status = WorkflowStatus.PROCESSING

        # Send initial progress
        await ws_manager.broadcast(
            {
                "type": "status",
                "workflow_id": workflow_id,
                "status": "processing",
                "message": "Starting workflow generation...",
            }
        )

        # Initialize generator
        generator = WorkflowGenerator(workflow_id, ws_manager)

        # Generate workflow
        workflow_json = await generator.generate(request)

        # Update response
        workflows_db[workflow_id].workflow_json = workflow_json
        workflows_db[workflow_id].status = WorkflowStatus.COMPLETED
        workflows_db[workflow_id].completed_at = datetime.now()

        # Send completion message
        await ws_manager.broadcast(
            {
                "type": "complete",
                "workflow_id": workflow_id,
                "status": "completed",
                "message": "Workflow generated successfully!",
            }
        )

    except Exception as e:
        # Handle error
        workflows_db[workflow_id].status = WorkflowStatus.FAILED
        workflows_db[workflow_id].error = str(e)

        await ws_manager.broadcast(
            {
                "type": "error",
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
            }
        )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get workflow by ID"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflows_db[workflow_id]


@router.get("/{workflow_id}/download")
async def download_workflow(workflow_id: str):
    """Download workflow JSON file"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow = workflows_db[workflow_id]
    if not workflow.workflow_json:
        raise HTTPException(status_code=400, detail="Workflow not yet generated")

    # Save to temp file
    temp_file = f"/tmp/{workflow_id}.json"
    with open(temp_file, "w") as f:
        json.dump(workflow.workflow_json, f, indent=2)

    return FileResponse(
        temp_file,
        media_type="application/json",
        filename=f"{workflow_id}.json",
    )


@router.get("/", response_model=List[WorkflowHistory])
async def get_workflow_history(limit: int = 20, offset: int = 0):
    """Get workflow generation history"""
    # Convert workflows to history items
    history = []
    for wf_id, wf in workflows_db.items():
        history.append(
            WorkflowHistory(
                id=wf.id,
                description=wf.metadata.get("description", ""),
                model_type=wf.metadata.get("model_type", "flux"),
                status=wf.status,
                created_at=wf.created_at,
                preview_url=None,  # TODO: Generate previews
            )
        )

    # Sort by created_at descending
    history.sort(key=lambda x: x.created_at, reverse=True)

    # Apply pagination
    return history[offset : offset + limit]


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete workflow by ID"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")

    del workflows_db[workflow_id]
    return {"message": "Workflow deleted successfully"}
