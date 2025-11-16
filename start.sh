#!/bin/bash

echo "🌳 Starting The Village Project..."
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ Node.js and npm are required but not installed."
    exit 1
fi

echo "✅ Dependencies check passed"
echo ""

# Start backend in background
echo "🚀 Starting Backend (Flask)..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Start Flask in background
python app.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

cd ..

# Start frontend
echo ""
echo "🎨 Starting Frontend (React)..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

echo "✅ Frontend starting..."
echo ""
echo "================================================"
echo "🌳 The Village Project is Running!"
echo "================================================"
echo "Backend:  http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"
echo ""

# Start frontend (this will block)
npm run dev

# Cleanup on exit
echo ""
echo "🛑 Shutting down..."
kill $BACKEND_PID 2>/dev/null
echo "✅ All services stopped"

