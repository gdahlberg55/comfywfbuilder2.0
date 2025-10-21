#!/bin/bash

# ComfyUI Workflow Builder UI - Setup Script
# This script sets up both backend and frontend

set -e

echo "================================"
echo "ComfyUI Workflow Builder UI Setup"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${YELLOW}Warning: Node.js version is less than 18${NC}"
fi

echo -e "${GREEN}✓ Node.js $(node -v)${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo -e "${GREEN}✓ Python $(python3 --version)${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ npm $(npm -v)${NC}"

echo ""
echo "================================"
echo "Setting up Backend"
echo "================================"
echo ""

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your configuration${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

cd ..

echo ""
echo "================================"
echo "Setting up Frontend"
echo "================================"
echo ""

cd frontend

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete${NC}"

cd ..

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure backend environment:"
echo "   ${YELLOW}nano backend/.env${NC}"
echo ""
echo "2. Start the backend server:"
echo "   ${GREEN}cd backend && source venv/bin/activate && python main.py${NC}"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   ${GREEN}cd frontend && npm run dev${NC}"
echo ""
echo "4. Open your browser to:"
echo "   ${GREEN}http://localhost:5173${NC}"
echo ""
echo "For more information, see docs/SETUP.md"
echo ""
