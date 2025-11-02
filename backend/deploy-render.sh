#!/bin/bash
# Render deployment script with automatic data ingestion

set -e  # Exit on error

echo "🚀 Clinical AI Assistant - Render Deployment"
echo "=============================================="
echo ""

# Check environment variables
echo "📋 Checking environment variables..."
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ ERROR: OPENROUTER_API_KEY not set"
    exit 1
fi

if [ -z "$VISION_AGENT_API_KEY" ]; then
    echo "❌ ERROR: VISION_AGENT_API_KEY not set"
    exit 1
fi

echo "✅ Environment variables OK"
echo ""

# Set paths
INDEX_DIR="${INDEX_DIR:-/var/data/indexes}"
DATA_DIR="${DATA_DIR:-/var/data/Clinical}"

echo "📁 Index directory: $INDEX_DIR"
echo "📁 Data directory: $DATA_DIR"
echo ""

# Check if indexes already exist
if [ -d "$INDEX_DIR" ] && [ "$(ls -A $INDEX_DIR 2>/dev/null)" ]; then
    echo "✅ Indexes found! Skipping ingestion..."
    ls -lh $INDEX_DIR/
else
    echo "📥 No indexes found. Running data ingestion..."
    echo ""
    
    # Check if data exists
    if [ ! -d "$DATA_DIR" ] || [ ! "$(ls -A $DATA_DIR 2>/dev/null)" ]; then
        echo "⚠️  WARNING: No data found in $DATA_DIR"
        echo "📋 You need to upload Clinical data folder first:"
        echo "   - Use Render Shell (paid) or SCP"
        echo "   - Upload to: $DATA_DIR"
        echo ""
        echo "🔧 For now, starting server without indexes..."
        echo "   (Server will return errors until data is uploaded and indexed)"
        echo ""
    else
        echo "✅ Data found! Running ingestion..."
        echo "⏳ This will take 15-25 minutes (Landing AI processing)"
        echo ""
        
        # Create index directory if needed
        mkdir -p "$INDEX_DIR"
        
        # Run data ingestion
        python data_ingestion.py
        
        echo ""
        echo "✅ Ingestion complete!"
        echo "📊 Indexes created:"
        ls -lh $INDEX_DIR/
    fi
fi

echo ""
echo "🌐 Starting FastAPI server..."
echo "=============================================="
echo ""

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
