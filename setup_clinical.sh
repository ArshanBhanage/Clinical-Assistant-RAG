#!/bin/bash

# Quick setup script for Clinical AI Assistant with Clinical folder data
# Run this after adding your OpenRouter API key to backend/.env

echo "=========================================="
echo "Clinical AI Assistant - Quick Setup"
echo "Using Clinical/ folder data"
echo "=========================================="
echo ""

# Check if OpenRouter API key is set
if ! grep -q "OPENROUTER_API_KEY=sk-or" backend/.env 2>/dev/null; then
    echo "⚠️  Please add your OpenRouter API key to backend/.env first!"
    echo ""
    echo "Edit backend/.env and replace:"
    echo "  OPENROUTER_API_KEY=your_openrouter_api_key_here"
    echo ""
    echo "With your actual key from https://openrouter.ai/"
    echo ""
    exit 1
fi

# Setup backend
echo "Step 1/4: Setting up Python environment..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo ""
echo "Step 2/4: Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Step 3/4: Processing data with Landing AI..."
echo "  - Parsing 20 PDFs from Clinical folder"
echo "  - Processing 4 CSV files with clinical trial data"
echo "  - This may take 5-10 minutes..."
echo ""

python data_ingestion.py

if [ $? -ne 0 ]; then
    echo "❌ Error during data ingestion"
    exit 1
fi

echo ""
echo "Step 4/4: Building RAG indexes..."
echo "  - Generating embeddings"
echo "  - Creating FAISS indexes"
echo ""

python rag_pipeline.py

if [ $? -ne 0 ]; then
    echo "❌ Error building indexes"
    exit 1
fi

cd ..

# Setup frontend
echo ""
echo "Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

cd ..

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Your Clinical data is ready:"
echo "  • COVID: 5 PDFs + clinical trial CSV"
echo "  • Diabetes: 5 PDFs + clinical trial CSV"
echo "  • Heart Attack: 5 PDFs + clinical trial CSV"
echo "  • Knee Injuries: 5 PDFs + clinical trial CSV"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
