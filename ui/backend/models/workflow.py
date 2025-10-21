"""
Data models for workflows
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ModelType(str, Enum):
    """Supported model types"""

    FLUX = "flux"
    SDXL = "sdxl"
    PONY = "pony"
    SD15 = "sd1.5"


class WorkflowStatus(str, Enum):
    """Workflow generation status"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(str, Enum):
    """Agent execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowRequest(BaseModel):
    """Request model for workflow generation"""

    description: str = Field(..., description="Natural language workflow description")
    model_type: Optional[ModelType] = Field(
        ModelType.FLUX, description="AI model type to use"
    )
    width: Optional[int] = Field(1024, description="Image width")
    height: Optional[int] = Field(1024, description="Image height")
    steps: Optional[int] = Field(30, description="Number of sampling steps")
    include_upscale: Optional[bool] = Field(True, description="Include upscaling pass")
    include_adetailer: Optional[bool] = Field(False, description="Include ADetailer")
    lora_models: Optional[List[str]] = Field(default=[], description="LoRA models to use")
    custom_options: Optional[Dict[str, Any]] = Field(
        default={}, description="Custom workflow options"
    )


class AgentProgress(BaseModel):
    """Progress information for an agent"""

    name: str
    status: AgentStatus
    message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class WorkflowResponse(BaseModel):
    """Response model for workflow generation"""

    id: str
    status: WorkflowStatus
    workflow_json: Optional[Dict[str, Any]] = None
    agent_progress: List[AgentProgress] = []
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class WorkflowHistory(BaseModel):
    """Workflow history item"""

    id: str
    description: str
    model_type: ModelType
    status: WorkflowStatus
    created_at: datetime
    preview_url: Optional[str] = None
