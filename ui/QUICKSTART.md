# Quick Start Guide

Get up and running with ComfyUI Workflow Builder UI in 5 minutes!

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- ComfyUI Workflow Builder v2.0 at `/home/user/comfywfbuilder2.0`

## Installation

```bash
cd /home/user/comfyui-builder-ui

# Run setup script
./setup.sh
```

The setup script will:
1. Check prerequisites
2. Install backend dependencies
3. Install frontend dependencies
4. Create configuration files

## Configuration

Edit `backend/.env`:

```bash
nano backend/.env
```

Update the `BUILDER_PATH` if different:
```env
BUILDER_PATH=/home/user/comfywfbuilder2.0
```

## Running

### Option 1: Start Script (Recommended)

```bash
./start.sh
```

This starts both backend and frontend automatically.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access

Open your browser to:
- **UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs

## First Workflow

1. Enter a description:
   ```
   Create a Flux workflow with LoRA support and upscaling
   ```

2. Click "Generate Workflow"

3. Watch the progress in real-time

4. Download your workflow JSON

5. Import into ComfyUI!

## Next Steps

- Read [docs/USAGE.md](docs/USAGE.md) for detailed usage guide
- Explore [docs/API.md](docs/API.md) for API documentation
- Check [docs/SETUP.md](docs/SETUP.md) for advanced setup

## Troubleshooting

**Backend won't start:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules
npm install
```

**Can't connect to API:**
- Check backend is running
- Verify `backend/.env` has correct settings
- Check `frontend/.env` has correct API_URL

## Support

For issues, check:
- Backend logs: `backend/logs/api.log`
- Browser console (F12)
- [docs/SETUP.md](docs/SETUP.md) for detailed troubleshooting
