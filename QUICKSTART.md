# Quick Start Guide - Clinical AI Assistant

## 🚀 Get Started in 5 Minutes

### Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] OpenRouter API key (get free at https://openrouter.ai/)
- [ ] PDF papers ready (5 per domain recommended)

### Step-by-Step Setup

#### 1️⃣ Get Your OpenRouter API Key (2 minutes)

1. Visit https://openrouter.ai/
2. Sign up with your email
3. Go to Settings → API Keys
4. Create a new key
5. Copy your key (starts with `sk-or-...`)

#### 2️⃣ Configure the Backend (1 minute)

```bash
# Navigate to the backend folder
cd "clinical-ai-assistant/backend"

# Edit the .env file
# Replace 'your_openrouter_api_key_here' with your actual key
nano .env  # or use any text editor
```

Your `.env` should look like:
```bash
VISION_AGENT_API_KEY=ajBsZzJjdzE2ajhnY3VrdndoZGdiOmV6TFNYUDMyZU9YWEFhZ3VPWVVhN2JSeFpSdWQ0QU16
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

#### 3️⃣ Add Your PDF Files (2 minutes)

Place your IEEE papers in these folders:

```bash
backend/data/covid/pdfs/
  ├── covid_paper_1.pdf
  ├── covid_paper_2.pdf
  ├── covid_paper_3.pdf
  ├── covid_paper_4.pdf
  └── covid_paper_5.pdf

backend/data/diabetes_heart/pdfs/
  ├── diabetes_paper_1.pdf
  ├── diabetes_paper_2.pdf
  └── ... (5 papers)

backend/data/knee_injuries/pdfs/
  ├── knee_paper_1.pdf
  ├── knee_paper_2.pdf
  └── ... (5 papers)
```

**Note**: Sample CSV data is already included for testing!

#### 4️⃣ Run the Setup Script (3-10 minutes)

```bash
# From the clinical-ai-assistant root directory
chmod +x setup.sh
./setup.sh
```

This script will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Parse PDFs with Landing AI
- ✅ Build FAISS vector indexes
- ✅ Install frontend dependencies

**Expected output**: You should see progress bars and success messages.

#### 5️⃣ Start the Application

**Option A: Use the quick start script**
```bash
chmod +x start.sh
./start.sh
```

**Option B: Start manually (recommended for development)**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

#### 6️⃣ Open the App

🌐 Open your browser to: **http://localhost:3000**

## 🎯 First Test Query

Try these example questions:

**COVID Domain:**
- "What are the symptoms of COVID-19?"
- "How is COVID-19 transmitted?"
- "What treatments are available for COVID?"

**Diabetes/Heart:**
- "How is diabetes managed?"
- "What are the risk factors for heart attacks?"
- "What is the relationship between diabetes and cardiovascular disease?"

**Knee Injuries:**
- "What are common types of knee injuries?"
- "How are ACL tears treated?"
- "What is the recovery time for meniscus surgery?"

## ✅ Verification Steps

### Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "indexes": {
    "covid": {"loaded": true, "num_vectors": 150},
    "diabetes_heart": {"loaded": true, "num_vectors": 120},
    "knee_injuries": {"loaded": true, "num_vectors": 100}
  }
}
```

### Check Frontend
- Navigate to http://localhost:3000
- You should see the Clinical AI Assistant interface
- Try submitting a test query

### Test API Documentation
Visit: http://localhost:8000/docs

You can test API endpoints directly from the Swagger UI.

## 🐛 Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'landingai_ade'"
**Fix:**
```bash
cd backend
source venv/bin/activate
pip install landingai-ade
```

### Issue: "RAG pipeline not initialized"
**Fix:** You need to build the indexes first:
```bash
cd backend
source venv/bin/activate
python data_ingestion.py
python rag_pipeline.py
```

### Issue: "Error generating response: 401 Unauthorized"
**Fix:** Your OpenRouter API key is invalid or not set:
1. Check `backend/.env`
2. Make sure `OPENROUTER_API_KEY` is correct
3. Restart the backend server

### Issue: "No PDF files found"
**Fix:** Add PDF files to the correct folders:
- `backend/data/covid/pdfs/*.pdf`
- `backend/data/diabetes_heart/pdfs/*.pdf`
- `backend/data/knee_injuries/pdfs/*.pdf`

### Issue: Frontend shows "Failed to fetch"
**Fix:**
1. Make sure backend is running on port 8000
2. Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Try restarting both servers

### Issue: "Cannot find module 'next'"
**Fix:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📊 Using the Visualizations

After getting a response:

1. **Select Graph Type**:
   - Word Cloud: See most common terms
   - Term Frequency: Bar chart of top words
   - Source Distribution: Where answers came from
   - Similarity Scores: How relevant each source is

2. **Click "Generate Graph"**

3. **View the visualization** below

## 💡 Tips for Best Results

1. **Be Specific**: Instead of "Tell me about COVID", ask "What are the main symptoms of COVID-19?"

2. **Use Domain Selection**: Narrow your search by selecting a specific domain

3. **Check Sources**: Always review the source citations to verify information

4. **Rate Responses**: Use 👍/👎 to help improve the system (future feature)

5. **Try Different Visualizations**: Each graph type reveals different insights

## 🎨 Customization

### Change the LLM Model
Edit `backend/config.py`:
```python
OPENROUTER_MODEL = "openai/gpt-4"  # Use a more powerful model
```

See available models: https://openrouter.ai/models

### Adjust Retrieval Settings
Edit `backend/config.py`:
```python
TOP_K_RESULTS = 10  # Retrieve more documents
MIN_SIMILARITY_SCORE = 0.5  # Higher threshold
```

### Add More Data
1. Add new PDFs to `backend/data/*/pdfs/`
2. Re-run:
   ```bash
   python data_ingestion.py
   python rag_pipeline.py
   ```

## 📞 Need Help?

1. **Check the main README.md** for detailed documentation
2. **Review logs**: Backend terminal shows detailed error messages
3. **Test with sample data**: The system includes sample CSV files
4. **Verify API keys**: Most issues are due to incorrect API keys

## 🎉 Success!

If you can:
- ✅ Submit a query
- ✅ Get a response with sources
- ✅ Generate a visualization
- ✅ Rate the response

**You're all set!** Start exploring your clinical datasets.

---

**Next Steps:**
- Add more PDF papers for better coverage
- Experiment with different queries
- Try all visualization types
- Explore the API documentation at http://localhost:8000/docs

Happy querying! 🏥🤖
