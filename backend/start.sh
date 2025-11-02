#!/bin/bash
# Startup script for backend deployment

echo "🚀 Starting Clinical AI Assistant Backend..."

# Check if indexes exist
INDEXES_DIR="/app/indexes"
if [ ! -d "$INDEXES_DIR" ] || [ -z "$(ls -A $INDEXES_DIR)" ]; then
    echo "⚠️  WARNING: Indexes directory is empty or missing!"
    echo "📍 Looking for indexes in: $INDEXES_DIR"
    echo "ℹ️  Please upload pre-built indexes to this location."
    echo "   Required files:"
    echo "   - covid_index.faiss, covid_metadata.pkl"
    echo "   - diabetes_index.faiss, diabetes_metadata.pkl"
    echo "   - heart_attack_index.faiss, heart_attack_metadata.pkl"
    echo "   - knee_injuries_index.faiss, knee_injuries_metadata.pkl"
    echo "   - all_documents.pkl"
    
    # Check if indexes are in local path (development)
    if [ -d "./indexes" ]; then
        echo "✅ Found indexes in ./indexes (development mode)"
    else
        echo "❌ Cannot start without indexes!"
        exit 1
    fi
fi

echo "✅ Indexes found!"
echo "🔧 Starting FastAPI server..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
