#!/bin/bash

# ComfyUI Workflow Builder UI - Start Script
# Starts both backend and frontend in development mode

set -e

echo "Starting ComfyUI Workflow Builder UI..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to be ready..."
sleep 3

# Start frontend
echo "Starting frontend dev server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "Services Started!"
echo "================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for processes
wait
