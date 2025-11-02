#!/bin/bash
# Script to prepare indexes for deployment upload

echo "📦 Preparing indexes for deployment..."

cd "$(dirname "$0")"

INDEXES_DIR="backend/indexes"
OUTPUT_ZIP="clinical-ai-indexes.zip"

# Check if indexes exist
if [ ! -d "$INDEXES_DIR" ]; then
    echo "❌ Error: Indexes directory not found at $INDEXES_DIR"
    exit 1
fi

# Check if required files exist
REQUIRED_FILES=(
    "covid_index.faiss"
    "covid_metadata.pkl"
    "diabetes_index.faiss"
    "diabetes_metadata.pkl"
    "heart_attack_index.faiss"
    "heart_attack_metadata.pkl"
    "knee_injuries_index.faiss"
    "knee_injuries_metadata.pkl"
    "all_documents.pkl"
)

echo "🔍 Checking required files..."
MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$INDEXES_DIR/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "❌ Missing required files:"
    printf '   - %s\n' "${MISSING_FILES[@]}"
    exit 1
fi

echo "✅ All required files found!"

# Create zip file
echo "📦 Creating zip archive..."
cd backend
zip -r "../$OUTPUT_ZIP" indexes/ -x "*.DS_Store" -x "__pycache__/*"
cd ..

# Get file size
SIZE=$(du -sh "$OUTPUT_ZIP" | cut -f1)

echo ""
echo "✅ Success! Indexes packaged for deployment."
echo ""
echo "📄 File: $OUTPUT_ZIP"
echo "📊 Size: $SIZE"
echo ""
echo "📤 Upload Instructions:"
echo ""
echo "For Railway:"
echo "  1. Deploy your backend to Railway"
echo "  2. Create a volume: railway volume create indexes"
echo "  3. Attach volume: railway volume attach indexes /app/indexes"
echo "  4. Upload via Railway dashboard or CLI"
echo ""
echo "For Render:"
echo "  1. Create your web service on Render"
echo "  2. Add a disk with mount path: /opt/render/project/src/indexes"
echo "  3. Upload this zip via Render dashboard"
echo "  4. Unzip in the shell: unzip $OUTPUT_ZIP -d /opt/render/project/src/"
echo ""
echo "For Docker:"
echo "  1. Extract: unzip $OUTPUT_ZIP"
echo "  2. The docker-compose.yml will mount it automatically"
echo ""
