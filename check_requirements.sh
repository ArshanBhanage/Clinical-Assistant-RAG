#!/bin/bash

# Check prerequisites for Clinical AI Assistant

echo "=========================================="
echo "Clinical AI Assistant - Prerequisites Check"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check Python
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    echo -e "${GREEN}✓${NC} Found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Not found"
    echo "  Please install Python 3.8 or higher"
    ERRORS=$((ERRORS + 1))
fi

# Check pip
echo -n "Checking pip... "
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d ' ' -f 2)
    echo -e "${GREEN}✓${NC} Found: $PIP_VERSION"
else
    echo -e "${RED}✗${NC} Not found"
    echo "  Please install pip3"
    ERRORS=$((ERRORS + 1))
fi

# Check Node.js
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Not found"
    echo "  Please install Node.js 18 or higher"
    ERRORS=$((ERRORS + 1))
fi

# Check npm
echo -n "Checking npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} Found: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} Not found"
    echo "  Please install npm"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=========================================="
echo "Configuration Check"
echo "=========================================="
echo ""

# Check backend .env
echo -n "Checking backend/.env... "
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} Found"
    
    # Check for API keys
    if grep -q "VISION_AGENT_API_KEY=ajBsZzJjdzE2ajhnY3VrdndoZGdiOmV6TFNYUDMyZU9YWEFhZ3VPWVVhN2JSeFpSdWQ0QU16" backend/.env; then
        echo "  Landing AI API key: ${GREEN}✓${NC} Configured"
    else
        echo "  Landing AI API key: ${RED}✗${NC} Missing or incorrect"
        ERRORS=$((ERRORS + 1))
    fi
    
    if grep -q "OPENROUTER_API_KEY=your_openrouter_api_key_here" backend/.env; then
        echo "  OpenRouter API key: ${YELLOW}⚠${NC}  Not configured (default value)"
        echo "    → Update with your actual API key from https://openrouter.ai/"
    else
        echo "  OpenRouter API key: ${GREEN}✓${NC} Configured"
    fi
else
    echo -e "${RED}✗${NC} Not found"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=========================================="
echo "Data Check"
echo "=========================================="
echo ""

# Check for PDF files
pdf_count=0
for domain in covid diabetes_heart knee_injuries; do
    echo -n "Checking $domain PDFs... "
    domain_pdfs=$(find "backend/data/$domain/pdfs" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$domain_pdfs" -gt 0 ]; then
        echo -e "${GREEN}✓${NC} Found $domain_pdfs PDF(s)"
    else
        echo -e "${YELLOW}⚠${NC}  No PDFs found"
        echo "  → Add PDF papers to backend/data/$domain/pdfs/"
    fi
    pdf_count=$((pdf_count + domain_pdfs))
done

if [ $pdf_count -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}Note:${NC} No PDFs found. Sample CSV data is included for testing,"
    echo "      but adding PDF papers is recommended for better results."
fi

# Check for CSV files
echo ""
echo -n "Checking sample CSV data... "
csv_count=0
for domain in covid diabetes_heart knee_injuries; do
    if [ -f "backend/data/$domain/sample_clinical_data.csv" ]; then
        csv_count=$((csv_count + 1))
    fi
done
if [ $csv_count -eq 3 ]; then
    echo -e "${GREEN}✓${NC} All domains have sample data"
else
    echo -e "${YELLOW}⚠${NC}  Some sample data missing"
fi

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All prerequisites met!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Add your PDF papers to backend/data/*/pdfs/ folders"
    echo "  2. Update OpenRouter API key in backend/.env"
    echo "  3. Run: ./setup.sh"
    echo ""
else
    echo -e "${RED}✗ $ERRORS issue(s) found${NC}"
    echo ""
    echo "Please resolve the issues above before continuing."
    echo ""
fi

exit $ERRORS
