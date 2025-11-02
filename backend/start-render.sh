#!/bin/bash
# Render deployment startup script for backend

echo "🚀 Starting Clinical AI Assistant Backend on Render"
echo "=================================================="

# Check if indexes exist
if [ -d "/app/indexes" ] && [ "$(ls -A /app/indexes)" ]; then
    echo "✅ Indexes found in /app/indexes"
    ls -lh /app/indexes/
elif [ -d "./indexes" ] && [ "$(ls -A ./indexes)" ]; then
    echo "✅ Indexes found in ./indexes"
    ls -lh ./indexes/
else
    echo "⚠️  WARNING: No indexes found!"
    echo "📋 Please upload indexes to /app/indexes/"
    echo ""
    echo "Required files:"
    echo "  - covid_index.faiss"
    echo "  - covid_metadata.pkl"
    echo "  - diabetes_index.faiss"
    echo "  - diabetes_metadata.pkl"
    echo "  - heart_attack_index.faiss"
    echo "  - heart_attack_metadata.pkl"
    echo "  - knee_injuries_index.faiss"
    echo "  - knee_injuries_metadata.pkl"
    echo "  - all_documents.pkl"
    echo ""
    echo "🔧 To upload indexes:"
    echo "1. Go to Render Dashboard → Your Service → Shell"
    echo "2. Navigate to /app/indexes"
    echo "3. Upload clinical-ai-indexes.zip"
    echo "4. Run: unzip clinical-ai-indexes.zip"
    echo ""
fi

# Start the FastAPI application
echo ""
echo "🌐 Starting server on port ${PORT:-8000}..."
echo "=================================================="
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
