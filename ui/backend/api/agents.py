"""
Agents API endpoints
"""

from typing import List, Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/list")
async def list_agents():
    """List all available agents"""
    agents = [
        {
            "name": "parameter-extractor",
            "description": "Extracts parameters from user requests",
            "category": "generation",
        },
        {
            "name": "asset-finder",
            "description": "Searches for models, LoRAs, custom nodes",
            "category": "generation",
        },
        {
            "name": "prompt-crafter",
            "description": "Optimizes prompts with triggers",
            "category": "generation",
        },
        {
            "name": "workflow-architect",
            "description": "Designs workflow structure",
            "category": "generation",
        },
        {
            "name": "node-curator",
            "description": "Selects appropriate ComfyUI nodes",
            "category": "generation",
        },
        {
            "name": "graph-engineer",
            "description": "Wires node connections",
            "category": "generation",
        },
        {
            "name": "graph-analyzer",
            "description": "Analyzes workflow topology",
            "category": "organization",
        },
        {
            "name": "layout-strategist",
            "description": "Plans optimal layout with data buses",
            "category": "organization",
        },
        {
            "name": "reroute-engineer",
            "description": "Implements orthogonal routing",
            "category": "organization",
        },
        {
            "name": "layout-refiner",
            "description": "Resolves collisions via AABB",
            "category": "organization",
        },
        {
            "name": "group-coordinator",
            "description": "Creates semantic groups",
            "category": "organization",
        },
        {
            "name": "nomenclature-specialist",
            "description": "Applies descriptive naming",
            "category": "organization",
        },
        {
            "name": "workflow-validator",
            "description": "Technical validation",
            "category": "validation",
        },
        {
            "name": "workflow-serializer",
            "description": "JSON format conversion",
            "category": "serialization",
        },
        {
            "name": "learning-agent",
            "description": "Pattern recognition and improvement",
            "category": "support",
        },
        {
            "name": "logger",
            "description": "Session and audit logging",
            "category": "support",
        },
        {
            "name": "memory-monitor",
            "description": "Resource usage tracking",
            "category": "support",
        },
        {
            "name": "node-verification",
            "description": "Schema validation",
            "category": "validation",
        },
    ]
    return {"agents": agents, "total": len(agents)}


@router.get("/pipeline")
async def get_pipeline_info():
    """Get information about the agent pipeline"""
    return {
        "mode_1": {
            "name": "Workflow Generation",
            "description": "Natural Language → JSON",
            "agents": [
                "parameter-extractor",
                "asset-finder",
                "prompt-crafter",
                "workflow-architect",
                "node-curator",
                "graph-engineer",
            ],
        },
        "mode_2": {
            "name": "Workflow Organization",
            "description": "JSON → Organized JSON",
            "agents": [
                "graph-analyzer",
                "layout-strategist",
                "reroute-engineer",
                "layout-refiner",
                "group-coordinator",
                "nomenclature-specialist",
                "workflow-validator",
                "workflow-serializer",
            ],
        },
    }
