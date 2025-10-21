# Setup Guide

Complete setup instructions for the ComfyUI Workflow Builder Web UI.

## Prerequisites

### Required Software
- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **npm** or **yarn** package manager
- **pip** Python package manager

### System Requirements
- **ComfyUI Workflow Builder v2.0** must be installed at `/home/user/comfywfbuilder2.0`
- Minimum 4GB RAM
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation Steps

### 1. Clone or Copy the UI Project

```bash
cd /home/user
# The UI should already be in /home/user/comfyui-builder-ui
cd comfyui-builder-ui
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Important .env Configuration:**
```env
# Backend Configuration
API_PORT=8000
API_HOST=0.0.0.0

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# ComfyUI Workflow Builder Path
BUILDER_PATH=/home/user/comfywfbuilder2.0

# Workspace Path
WORKSPACE_PATH=/home/user/comfywfbuilder2.0/workspace
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

### 4. Verify Installation

Check that all dependencies are installed:

```bash
# Backend
cd backend
python -c "import fastapi; print('FastAPI OK')"

# Frontend
cd ../frontend
npm list react
```

## Running the Application

### Development Mode

**Terminal 1 - Backend Server:**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python main.py
```

You should see:
```
Starting ComfyUI Workflow Builder API on 0.0.0.0:8000
Builder Path: /home/user/comfywfbuilder2.0
Docs: http://localhost:8000/api/docs
```

**Terminal 2 - Frontend Dev Server:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Access the Application

Open your browser and navigate to:
- **UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs
- **API Health**: http://localhost:8000/api/health

## Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`.

### Serve with Production Server

```bash
cd backend
pip install gunicorn

# Start with Gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Using Docker (Optional)

A Dockerfile will be provided in future updates for containerized deployment.

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`
```bash
pip install -r requirements.txt
```

**Problem:** `BUILDER_PATH not found`
- Verify the path in `.env` file
- Ensure ComfyUI Workflow Builder v2.0 is installed

**Problem:** `Address already in use`
```bash
# Change port in .env
API_PORT=8001
```

### Frontend Issues

**Problem:** `Cannot find module 'react'`
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem:** `Failed to fetch from API`
- Check backend is running
- Verify API_URL in frontend/.env
- Check CORS settings in backend/.env

**Problem:** WebSocket connection failed
- Ensure backend supports WebSocket
- Check firewall settings
- Verify WS_URL in frontend

### Common Issues

**Problem:** Workflows not generating
- Check ComfyUI Workflow Builder v2.0 is installed
- Verify Python modules in code_modules/
- Check backend logs for errors

**Problem:** Slow performance
- Increase workers in production
- Check system resources
- Enable caching

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `API_PORT` | Backend server port | `8000` |
| `API_HOST` | Backend server host | `0.0.0.0` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:5173` |
| `BUILDER_PATH` | Path to ComfyUI Builder | `/home/user/comfywfbuilder2.0` |
| `WORKSPACE_PATH` | Workspace directory | `{BUILDER_PATH}/workspace` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Frontend (.env)

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/progress
```

## Next Steps

1. Read [USAGE.md](USAGE.md) for usage instructions
2. Check [API.md](API.md) for API documentation
3. Review example workflows in the UI

## Support

For issues:
- Check logs in `backend/logs/`
- Review browser console for frontend errors
- Consult [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
