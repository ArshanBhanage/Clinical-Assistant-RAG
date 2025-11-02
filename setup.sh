#!/bin/bash

# Setup script for Clinical AI Assistant
# Run this after placing your PDF files and configuring .env

echo "=========================================="
echo "Clinical AI Assistant - Setup Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "Error: Please run this script from the clinical-ai-assistant root directory"
    exit 1
fi

# Step 1: Setup Backend
echo "Step 1/5: Setting up Python virtual environment..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "Step 2/5: Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Check for .env file
echo ""
echo "Step 3/5: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create it with your API keys."
    echo "   Copy from .env.example if available"
    exit 1
fi

# Check for API keys
if ! grep -q "OPENROUTER_API_KEY=your_openrouter_api_key_here" .env; then
    echo "✅ OpenRouter API key configured"
else
    echo "⚠️  Warning: Please update your OpenRouter API key in backend/.env"
fi

# Check for PDF files
echo ""
echo "Step 4/5: Checking for PDF files..."
pdf_count=0
for domain in covid diabetes_heart knee_injuries; do
    domain_pdfs=$(find "data/$domain/pdfs" -name "*.pdf" 2>/dev/null | wc -l)
    echo "  - $domain: $domain_pdfs PDF files found"
    pdf_count=$((pdf_count + domain_pdfs))
done

if [ $pdf_count -eq 0 ]; then
    echo "⚠️  Warning: No PDF files found. Please add PDF files to data/*/pdfs/ folders"
    echo "   Each domain should have at least 5 IEEE papers"
else
    echo "✅ Found $pdf_count total PDF files"
fi

echo ""
echo "Step 5/5: Ingesting data and building indexes..."
echo "This may take several minutes depending on the number of PDFs..."
echo ""

python data_ingestion.py
if [ $? -ne 0 ]; then
    echo "❌ Error during data ingestion"
    exit 1
fi

echo ""
python rag_pipeline.py
if [ $? -ne 0 ]; then
    echo "❌ Error building RAG indexes"
    exit 1
fi

cd ..

# Step 6: Setup Frontend
echo ""
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "✅ Frontend dependencies already installed"
fi

cd ..

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
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
