# ComfyUI Workflow Builder - Web UI

A modern web-based interface for the ComfyUI Workflow Builder v2.0 system.

## Overview

This web UI provides an intuitive interface for generating ComfyUI workflows using natural language. It connects to the ComfyUI Workflow Builder v2.0 backend and provides real-time visualization of the workflow generation process.

## Features

- **Natural Language Input**: Describe your workflow in plain English
- **Real-Time Progress**: Watch the agent pipeline in action
- **Workflow Visualization**: See your workflow visually before downloading
- **JSON Editor**: View and edit the generated workflow JSON
- **Export Options**: Download workflows in multiple formats
- **History Management**: Access previously generated workflows
- **Settings Panel**: Configure models, paths, and preferences

## Architecture

```
comfyui-builder-ui/
├── frontend/          # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API services
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utility functions
│   ├── public/           # Static assets
│   └── package.json
│
├── backend/           # FastAPI backend
│   ├── api/          # API routes
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   ├── websocket/    # WebSocket handlers
│   └── main.py       # Application entry
│
└── docs/             # Documentation
    ├── API.md        # API documentation
    ├── SETUP.md      # Setup instructions
    └── USAGE.md      # Usage guide
```

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Query** - Data fetching
- **Zustand** - State management
- **Monaco Editor** - JSON editing
- **React Flow** - Workflow visualization

### Backend
- **FastAPI** - Python web framework
- **WebSocket** - Real-time updates
- **Pydantic** - Data validation
- **Python 3.10+** - Runtime

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- ComfyUI Workflow Builder v2.0 installed

### Installation

1. **Clone the repository**
```bash
cd /home/user/comfyui-builder-ui
```

2. **Install frontend dependencies**
```bash
cd frontend
npm install
```

3. **Install backend dependencies**
```bash
cd ../backend
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

### Running the Application

**Development Mode:**

Terminal 1 - Backend:
```bash
cd backend
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Access the UI at: http://localhost:5173

**Production Mode:**
```bash
cd frontend
npm run build
cd ../backend
python main.py --production
```

## Usage

1. **Enter Workflow Description**: In the main input area, describe your desired workflow in natural language
2. **Configure Options**: Set model type, resolution, and other preferences
3. **Generate**: Click "Generate Workflow"
4. **Monitor Progress**: Watch the agent pipeline execute in real-time
5. **Review & Edit**: View the generated workflow visually and in JSON
6. **Export**: Download your workflow JSON file

## Example Workflow Requests

```
Create a Flux workflow with LoRA support and 2-pass upscaling

Build a SDXL workflow with ADetailer for face enhancement and Ultimate SD Upscale

Generate a Pony model workflow with wildcards, multi-pass rendering, and controlnet support
```

## API Endpoints

- `POST /api/workflows/generate` - Generate a new workflow
- `GET /api/workflows/{id}` - Get workflow by ID
- `GET /api/workflows/history` - Get workflow history
- `WS /ws/progress` - Real-time progress updates

See [docs/API.md](docs/API.md) for complete API documentation.

## Development

### Frontend Development
```bash
cd frontend
npm run dev        # Start dev server
npm run build      # Build for production
npm run lint       # Run ESLint
npm run type-check # Run TypeScript checks
```

### Backend Development
```bash
cd backend
python main.py --dev    # Start with auto-reload
pytest                  # Run tests
black .                 # Format code
mypy .                  # Type checking
```

## Configuration

Configuration is done through environment variables:

```env
# Backend
BUILDER_PATH=/home/user/comfywfbuilder2.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173

# Frontend
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

**Backend won't start:**
- Ensure ComfyUI Workflow Builder v2.0 is installed
- Check Python version (3.10+ required)
- Verify all dependencies are installed

**Frontend won't connect:**
- Check backend is running on correct port
- Verify CORS settings in backend
- Check browser console for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [github.com/gdahlberg55/comfywfbuilder2.0]
- Documentation: See docs/ folder

---

**Version**: 1.0.0
**Status**: Alpha
**Last Updated**: October 2025
