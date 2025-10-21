"""
Workflow Generator Service
Orchestrates the workflow generation process using agents
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from models.workflow import WorkflowRequest, AgentStatus, AgentProgress


class WorkflowGenerator:
    """Generates ComfyUI workflows using the agent pipeline"""

    def __init__(self, workflow_id: str, ws_manager):
        self.workflow_id = workflow_id
        self.ws_manager = ws_manager
        self.builder_path = os.getenv("BUILDER_PATH", "/home/user/comfywfbuilder2.0")

    async def send_progress(self, agent_name: str, status: str, message: str = ""):
        """Send progress update via WebSocket"""
        await self.ws_manager.broadcast(
            {
                "type": "agent_progress",
                "workflow_id": self.workflow_id,
                "agent": agent_name,
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }
        )

    async def generate(self, request: WorkflowRequest) -> Dict[str, Any]:
        """
        Generate workflow using the agent pipeline

        This is a simplified version that creates a basic workflow structure.
        In production, this would integrate with the actual Claude Code agents.
        """

        # Mode 1: Workflow Generation Pipeline
        generation_agents = [
            "parameter-extractor",
            "asset-finder",
            "prompt-crafter",
            "workflow-architect",
            "node-curator",
            "graph-engineer",
        ]

        # Mode 2: Workflow Organization Pipeline
        organization_agents = [
            "graph-analyzer",
            "layout-strategist",
            "reroute-engineer",
            "layout-refiner",
            "group-coordinator",
            "nomenclature-specialist",
            "workflow-validator",
            "workflow-serializer",
        ]

        # Execute Mode 1
        await self.send_progress(
            "orchestrator", "running", "Starting Mode 1: Workflow Generation"
        )

        for agent in generation_agents:
            await self.send_progress(agent, "running", f"Executing {agent}...")
            await asyncio.sleep(0.5)  # Simulate work
            await self.send_progress(agent, "completed", f"{agent} completed")

        # Execute Mode 2
        await self.send_progress(
            "orchestrator", "running", "Starting Mode 2: Workflow Organization"
        )

        for agent in organization_agents:
            await self.send_progress(agent, "running", f"Executing {agent}...")
            await asyncio.sleep(0.5)  # Simulate work
            await self.send_progress(agent, "completed", f"{agent} completed")

        # Generate workflow JSON
        # This is a simplified example - in production, this would use the actual
        # workflow generation modules and Claude Code agents
        workflow_json = self.create_sample_workflow(request)

        await self.send_progress(
            "orchestrator", "completed", "Workflow generation complete!"
        )

        return workflow_json

    def create_sample_workflow(self, request: WorkflowRequest) -> Dict[str, Any]:
        """
        Create a sample workflow JSON structure
        In production, this would be replaced with actual workflow generation
        """
        return {
            "last_node_id": 10,
            "last_link_id": 15,
            "nodes": [
                {
                    "id": 1,
                    "type": "CheckpointLoaderSimple",
                    "pos": [50, 100],
                    "size": [315, 98],
                    "flags": {},
                    "order": 0,
                    "mode": 0,
                    "outputs": [
                        {"name": "MODEL", "type": "MODEL", "links": [1], "slot_index": 0},
                        {"name": "CLIP", "type": "CLIP", "links": [2, 3], "slot_index": 1},
                        {"name": "VAE", "type": "VAE", "links": [4], "slot_index": 2},
                    ],
                    "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
                    "widgets_values": [f"{request.model_type.value}_model.safetensors"],
                },
                {
                    "id": 2,
                    "type": "CLIPTextEncode",
                    "pos": [420, 80],
                    "size": [422.84503173828125, 164.6060791015625],
                    "flags": {},
                    "order": 1,
                    "mode": 0,
                    "inputs": [{"name": "clip", "type": "CLIP", "link": 2}],
                    "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [5]}],
                    "properties": {"Node name for S&R": "CLIPTextEncode"},
                    "widgets_values": [request.description or "a beautiful landscape"],
                },
                {
                    "id": 3,
                    "type": "EmptyLatentImage",
                    "pos": [50, 250],
                    "size": [315, 106],
                    "flags": {},
                    "order": 2,
                    "mode": 0,
                    "outputs": [{"name": "LATENT", "type": "LATENT", "links": [6]}],
                    "properties": {"Node name for S&R": "EmptyLatentImage"},
                    "widgets_values": [request.width, request.height, 1],
                },
            ],
            "links": [
                [1, 1, 0, 4, 0, "MODEL"],
                [2, 1, 1, 2, 0, "CLIP"],
                [3, 1, 1, 3, 0, "CLIP"],
                [4, 1, 2, 5, 1, "VAE"],
                [5, 2, 0, 4, 1, "CONDITIONING"],
                [6, 3, 0, 4, 3, "LATENT"],
            ],
            "groups": [],
            "config": {},
            "extra": {
                "generated_by": "ComfyUI Workflow Builder v2.0",
                "generated_at": datetime.now().isoformat(),
                "workflow_id": self.workflow_id,
            },
            "version": 0.4,
        }
