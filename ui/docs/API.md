# API Documentation

Complete API reference for the ComfyUI Workflow Builder backend.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Authentication

Currently, the API does not require authentication. This may be added in future versions.

## Endpoints

### Health Check

#### GET /api/health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "builder_path": "/home/user/comfywfbuilder2.0",
  "workspace_path": "/home/user/comfywfbuilder2.0/workspace"
}
```

---

### Workflows

#### POST /api/workflows/generate

Generate a new workflow from a description.

**Request Body:**
```json
{
  "description": "Create a Flux workflow with LoRA support",
  "model_type": "flux",
  "width": 1024,
  "height": 1024,
  "steps": 30,
  "include_upscale": true,
  "include_adetailer": false,
  "lora_models": [],
  "custom_options": {}
}
```

**Response:**
```json
{
  "id": "wf_20251021_143022",
  "status": "pending",
  "workflow_json": null,
  "agent_progress": [],
  "created_at": "2025-10-21T14:30:22.123Z",
  "completed_at": null,
  "error": null,
  "metadata": {
    "description": "Create a Flux workflow with LoRA support",
    "model_type": "flux",
    "dimensions": "1024x1024"
  }
}
```

#### GET /api/workflows/{workflow_id}

Get workflow by ID.

**Parameters:**
- `workflow_id` (path): Workflow ID

**Response:**
```json
{
  "id": "wf_20251021_143022",
  "status": "completed",
  "workflow_json": { ... },
  "agent_progress": [ ... ],
  "created_at": "2025-10-21T14:30:22.123Z",
  "completed_at": "2025-10-21T14:31:45.456Z",
  "error": null,
  "metadata": { ... }
}
```

#### GET /api/workflows/

Get workflow history.

**Query Parameters:**
- `limit` (int, optional): Number of results (default: 20)
- `offset` (int, optional): Offset for pagination (default: 0)

**Response:**
```json
[
  {
    "id": "wf_20251021_143022",
    "description": "Create a Flux workflow",
    "model_type": "flux",
    "status": "completed",
    "created_at": "2025-10-21T14:30:22.123Z",
    "preview_url": null
  }
]
```

#### GET /api/workflows/{workflow_id}/download

Download workflow JSON file.

**Parameters:**
- `workflow_id` (path): Workflow ID

**Response:**
- Content-Type: `application/json`
- Downloads file: `{workflow_id}.json`

#### DELETE /api/workflows/{workflow_id}

Delete workflow by ID.

**Parameters:**
- `workflow_id` (path): Workflow ID

**Response:**
```json
{
  "message": "Workflow deleted successfully"
}
```

---

### Agents

#### GET /api/agents/list

List all available agents.

**Response:**
```json
{
  "agents": [
    {
      "name": "parameter-extractor",
      "description": "Extracts parameters from user requests",
      "category": "generation"
    }
  ],
  "total": 18
}
```

#### GET /api/agents/pipeline

Get agent pipeline information.

**Response:**
```json
{
  "mode_1": {
    "name": "Workflow Generation",
    "description": "Natural Language → JSON",
    "agents": [
      "parameter-extractor",
      "asset-finder",
      ...
    ]
  },
  "mode_2": {
    "name": "Workflow Organization",
    "description": "JSON → Organized JSON",
    "agents": [
      "graph-analyzer",
      "layout-strategist",
      ...
    ]
  }
}
```

---

### Models

#### GET /api/models/types

Get available model types.

**Response:**
```json
{
  "types": [
    {
      "id": "flux",
      "name": "Flux",
      "description": "Flux AI models with advanced features",
      "default_resolution": "1024x1024"
    }
  ]
}
```

#### GET /api/models/loras

Get available LoRA models.

**Response:**
```json
{
  "loras": [
    {
      "name": "detail_enhancer",
      "path": "detail_enhancer.safetensors"
    }
  ]
}
```

#### GET /api/models/resolutions

Get common resolution presets.

**Response:**
```json
{
  "resolutions": [
    {
      "width": 1024,
      "height": 1024,
      "name": "SDXL Square",
      "ratio": "1:1"
    }
  ]
}
```

---

## WebSocket

### WS /ws/progress

Real-time progress updates during workflow generation.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/progress')
```

**Message Types:**

#### Status Update
```json
{
  "type": "status",
  "workflow_id": "wf_20251021_143022",
  "status": "processing",
  "message": "Starting workflow generation..."
}
```

#### Agent Progress
```json
{
  "type": "agent_progress",
  "workflow_id": "wf_20251021_143022",
  "agent": "parameter-extractor",
  "status": "running",
  "message": "Extracting parameters...",
  "timestamp": "2025-10-21T14:30:25.123Z"
}
```

#### Completion
```json
{
  "type": "complete",
  "workflow_id": "wf_20251021_143022",
  "status": "completed",
  "message": "Workflow generated successfully!"
}
```

#### Error
```json
{
  "type": "error",
  "workflow_id": "wf_20251021_143022",
  "status": "failed",
  "error": "Failed to generate workflow: ..."
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Workflow not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. This may be added in future versions.

---

## Example Usage

### cURL

```bash
# Generate workflow
curl -X POST http://localhost:8000/api/workflows/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Create a Flux workflow",
    "model_type": "flux",
    "width": 1024,
    "height": 1024
  }'

# Get workflow
curl http://localhost:8000/api/workflows/wf_20251021_143022

# Download workflow
curl -O http://localhost:8000/api/workflows/wf_20251021_143022/download
```

### JavaScript/Fetch

```javascript
// Generate workflow
const response = await fetch('http://localhost:8000/api/workflows/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: 'Create a Flux workflow',
    model_type: 'flux',
    width: 1024,
    height: 1024
  })
})
const workflow = await response.json()

// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/progress')
ws.onmessage = (event) => {
  const message = JSON.parse(event.data)
  console.log('Progress:', message)
}
```

### Python

```python
import requests
import json

# Generate workflow
response = requests.post(
    'http://localhost:8000/api/workflows/generate',
    json={
        'description': 'Create a Flux workflow',
        'model_type': 'flux',
        'width': 1024,
        'height': 1024
    }
)
workflow = response.json()

# Get workflow
response = requests.get(f'http://localhost:8000/api/workflows/{workflow["id"]}')
result = response.json()
```

---

## Versioning

Current API version: **v1.0.0**

API versions will be maintained for backward compatibility.
