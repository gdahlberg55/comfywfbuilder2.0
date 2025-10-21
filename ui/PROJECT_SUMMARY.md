# ComfyUI Workflow Builder - Web UI

## Project Overview

A complete web-based user interface for the ComfyUI Workflow Builder v2.0 system. This UI provides an intuitive way to generate professional ComfyUI workflows using natural language, with real-time progress tracking and visual feedback.

## What's Been Created

### Complete Full-Stack Application

✅ **Backend (Python/FastAPI)**
- RESTful API with FastAPI framework
- WebSocket support for real-time updates
- Workflow generation orchestration
- Agent pipeline management
- Complete API documentation (Swagger/ReDoc)

✅ **Frontend (React/TypeScript)**
- Modern React 18 application with TypeScript
- Tailwind CSS for styling
- Real-time progress tracking
- JSON editor with Monaco
- Workflow history management
- Responsive design

✅ **Documentation**
- Comprehensive setup guide
- API documentation
- Usage guide
- Quick start guide

✅ **Automation**
- Setup script (setup.sh)
- Start script (start.sh)
- Development-ready configuration

## Project Structure

```
comfyui-builder-ui/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   ├── workflows.py       # Workflow endpoints
│   │   ├── agents.py          # Agent endpoints
│   │   └── models_api.py      # Model endpoints
│   ├── services/              # Business logic
│   │   └── workflow_generator.py
│   ├── models/                # Data models
│   │   └── workflow.py
│   ├── websocket/             # WebSocket handlers
│   │   └── progress.py
│   ├── main.py                # Application entry
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   │   ├── Header.tsx
│   │   │   ├── WorkflowForm.tsx
│   │   │   ├── ProgressPanel.tsx
│   │   │   ├── WorkflowViewer.tsx
│   │   │   └── HistoryPanel.tsx
│   │   ├── pages/            # Page components
│   │   │   └── WorkflowBuilder.tsx
│   │   ├── services/         # API services
│   │   │   ├── api.ts
│   │   │   └── websocket.ts
│   │   ├── store/            # State management
│   │   │   └── workflowStore.ts
│   │   ├── types/            # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx           # Main app component
│   │   └── main.tsx          # Entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   └── tailwind.config.js    # Tailwind configuration
│
├── docs/                       # Documentation
│   ├── SETUP.md              # Setup instructions
│   ├── USAGE.md              # Usage guide
│   └── API.md                # API reference
│
├── setup.sh                   # Automated setup script
├── start.sh                   # Start script
├── QUICKSTART.md             # Quick start guide
├── README.md                 # Project overview
└── LICENSE                   # MIT License
```

## Features

### Core Features
- ✅ Natural language workflow generation
- ✅ Real-time agent pipeline visualization
- ✅ 14-step agent progress tracking
- ✅ JSON editor with syntax highlighting
- ✅ Workflow download functionality
- ✅ Workflow history management
- ✅ Multiple model type support (Flux, SDXL, Pony, SD1.5)
- ✅ Customizable resolution presets
- ✅ Advanced options (upscaling, ADetailer, etc.)

### Technical Features
- ✅ RESTful API with OpenAPI documentation
- ✅ WebSocket for real-time updates
- ✅ TypeScript for type safety
- ✅ React Query for data fetching
- ✅ Zustand for state management
- ✅ Tailwind CSS for styling
- ✅ Monaco Editor for JSON editing
- ✅ CORS configuration
- ✅ Error handling and validation

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **WebSockets** - Real-time communication
- **Pydantic** - Data validation
- **Python 3.10+** - Runtime

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Query** - Data fetching
- **Zustand** - State management
- **Monaco Editor** - Code editing
- **Lucide React** - Icons
- **Axios** - HTTP client

## Installation & Usage

### Quick Start

```bash
cd /home/user/comfyui-builder-ui

# Run setup
./setup.sh

# Configure backend
nano backend/.env

# Start application
./start.sh
```

### Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Access

- **UI**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## API Endpoints

### Workflows
- `POST /api/workflows/generate` - Generate workflow
- `GET /api/workflows/{id}` - Get workflow
- `GET /api/workflows/` - Get history
- `GET /api/workflows/{id}/download` - Download workflow
- `DELETE /api/workflows/{id}` - Delete workflow

### Agents
- `GET /api/agents/list` - List all agents
- `GET /api/agents/pipeline` - Get pipeline info

### Models
- `GET /api/models/types` - Get model types
- `GET /api/models/loras` - Get LoRAs
- `GET /api/models/resolutions` - Get resolutions

### WebSocket
- `WS /ws/progress` - Real-time progress updates

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate

# Run with auto-reload
python main.py

# Run tests (when available)
pytest

# Format code
black .
```

### Frontend Development
```bash
cd frontend

# Dev server
npm run dev

# Build
npm run build

# Type check
npm run type-check

# Lint
npm run lint
```

## Integration with ComfyUI Workflow Builder v2.0

This UI is designed to work with the existing ComfyUI Workflow Builder v2.0 system:

1. **Connects to Builder**: Backend integrates with Python modules from the builder
2. **Uses Agents**: Leverages the 24 specialized agents
3. **Follows Standards**: Adheres to all workflow standards and protocols
4. **Frontend Format**: Generates workflows in proper ComfyUI frontend format
5. **Workspace Integration**: Saves to builder's workspace directory

## Configuration

### Backend (.env)
```env
API_PORT=8000
BUILDER_PATH=/home/user/comfywfbuilder2.0
WORKSPACE_PATH=/home/user/comfywfbuilder2.0/workspace
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/progress
```

## Future Enhancements

Potential improvements:
- [ ] Visual workflow preview (node graph)
- [ ] Drag-and-drop workflow editing
- [ ] User authentication and sessions
- [ ] Workflow templates library
- [ ] Advanced search and filtering
- [ ] Export to multiple formats
- [ ] Integration with ComfyUI server
- [ ] Workflow comparison tool
- [ ] Batch workflow generation
- [ ] Model/LoRA browser integration

## Files Created

**Total**: 32 files

**Backend**: 9 files
- API routes (3)
- Services (1)
- Models (1)
- WebSocket (1)
- Configuration (3)

**Frontend**: 17 files
- Components (5)
- Pages (1)
- Services (2)
- Store (1)
- Types (1)
- Configuration (7)

**Documentation**: 6 files
- Setup guide
- Usage guide
- API documentation
- Quick start
- README
- Project summary

## License

MIT License - See LICENSE file

## Support

For issues:
1. Check logs in `backend/logs/`
2. Review browser console (F12)
3. Consult documentation in `docs/`
4. Check GitHub issues

## Notes

- This is a development-ready implementation
- Production deployment would require additional security
- Some features are simplified for MVP (e.g., in-memory storage)
- Visual workflow preview is planned for future release

## Credits

Built for the ComfyUI Workflow Builder v2.0 system
Designed to enhance the workflow generation experience with a modern web interface.

---

**Status**: ✅ Complete and Ready for Use
**Version**: 1.0.0
**Created**: October 2025
