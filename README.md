# 🏥 Clinical AI Assistant - RAG System

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

A Retrieval-Augmented Generation (RAG) system that answers clinical questions using **only local datasets**. Built with Landing AI's Agentic Document Extraction, FAISS vector search, and OpenRouter LLM.

## 🎯 Mission

Bridge the gap between data scarcity and clinical intelligence by providing an AI assistant capable of answering clinicians' questions in real-time, supported by credible, machine-readable evidence from:
- **20 IEEE 2024 peer-reviewed medical research papers**
- **30,000+ clinical trial records from ClinicalTrials.gov**

## ✨ Features

- 🔍 **RAG Architecture**: Retrieves relevant context before generating answers
- 📚 **Multi-Domain Support**: COVID-19, Diabetes, Heart Attack, Knee Injuries
- 📄 **PDF Processing**: Landing AI's Agentic Document Extraction with page-level grounding
- 🗂️ **Structured Data**: Ingests clinical trial CSV data from ClinicalTrials.gov
- 🎨 **Modern UI**: Next.js frontend with Tailwind CSS
- 📊 **Evidence Display**: Shows top 5 sources with document excerpts
- 👍👎 **Feedback System**: Rate responses for continuous improvement
- 📈 **Visualizations**: Word cloud, term frequency, source distribution
- 🔒 **100% Local**: All retrieval happens locally, no internet data

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Landing AI API Key](https://va.landing.ai/)
- [OpenRouter API Key](https://openrouter.ai/)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/ArshanBhanage/Clinical-Assistant-RAG.git
cd Clinical-Assistant-RAG

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd ../frontend
npm install

# 4. Configure API keys
cd ../backend
echo "VISION_AGENT_API_KEY=your_landing_ai_key" > .env
echo "OPENROUTER_API_KEY=your_openrouter_key" >> .env
echo "OPENROUTER_MODEL=nvidia/nemotron-nano-12b-v2-vl:free" >> .env
```

### Add Your Data

Place files in:
```
backend/data/Clinical/
├── Covid/*.pdf (5 PDFs)
├── Diabetes/*.pdf (5 PDFs)
├── Heart_attack/*.pdf (5 PDFs)
├── KneeInjuries/*.pdf (5 PDFs)
├── ctg-studies_covid.csv
├── ctg-studies_diabetes.csv
├── ctg-studies_heart_attack.csv
└── ctg-studies_knee_injuries.csv
```

### Run the System

```bash
# Terminal 1 - Ingest data (one-time)
cd backend
source venv/bin/activate
python data_ingestion.py     # Parse PDFs & CSVs
python rag_pipeline.py        # Build FAISS indexes

# Terminal 2 - Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 3 - Start frontend
cd frontend
npm run dev
```

**Access**: http://localhost:3000

## 📊 Dataset Statistics

| Domain | Research Papers | Clinical Trials | Total Documents |
|--------|----------------|-----------------|-----------------|
| COVID-19 | 5 PDFs | 4,773 trials | 5,106 |
| Diabetes | 5 PDFs | 22,860 trials | 23,313 |
| Heart Attack | 5 PDFs | 3,713 trials | 3,999 |
| Knee Injuries | 5 PDFs | 1,265 trials | 1,669 |
| **Total** | **20 PDFs** | **32,611 trials** | **34,087** |

## 🏗️ Architecture

```
User Query → Next.js UI → FastAPI Backend → RAG Pipeline
                                              ├─ Query Embedding (sentence-transformers)
                                              ├─ FAISS Vector Search (top-k retrieval)
                                              ├─ Context Assembly (retrieved docs)
                                              └─ LLM Generation (OpenRouter)
                                                    ↓
                                              Response + Evidence
```

### Data Sources
- **PDFs**: Parsed with Landing AI ADE (layout-aware, page grounding)
- **CSVs**: Clinical trial metadata (NCT IDs, interventions, outcomes)

### Tech Stack
- **Backend**: Python, FastAPI, FAISS, sentence-transformers
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **LLM**: NVIDIA Nemotron via OpenRouter (temperature=0.3 for accuracy)
- **Vector DB**: FAISS IndexFlatIP (cosine similarity)
- **Embedding**: all-MiniLM-L6-v2 (384 dimensions)

## 🎨 UI Showcase

### Query Interface
- Domain selector (COVID, Diabetes, Heart Attack, Knee Injuries, All)
- Natural language text input
- Real-time search with loading animations

### Response Display
- AI answer with confidence badge (High/Medium/Low)
- **Top 5 Evidence Cards**:
  - Document name & page number
  - Similarity match percentage
  - Text excerpt (500 chars)
  - Chunk type indicator
- Thumbs up/down feedback buttons
- Visualization options (word cloud, term frequency, etc.)

## 🔧 API Endpoints

### POST /query
```json
{
  "query": "What are the symptoms of COVID-19?",
  "domain": "covid"
}
```

**Response**:
```json
{
  "response": "Based on research papers and clinical trials...",
  "sources": [
    {
      "source": "COVID_Detection_Deep_Learning.pdf",
      "page": 3,
      "text": "Common symptoms include fever, cough, fatigue...",
      "similarity": 0.89,
      "chunk_type": "paragraph"
    }
  ],
  "confidence": "high"
}
```

### POST /generate-graph
```json
{
  "query": "COVID symptoms",
  "domain": "covid",
  "viz_type": "wordcloud"
}
```

## 📁 Project Structure

```
clinical-ai-assistant/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── rag_pipeline.py         # RAG implementation
│   ├── data_ingestion.py       # PDF/CSV processing
│   ├── visualizer.py           # Graph generation
│   ├── config.py               # Configuration
│   ├── requirements.txt
│   ├── .env                    # API keys (gitignored)
│   ├── data/Clinical/          # Your data (gitignored)
│   └── indexes/                # FAISS indexes (gitignored)
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main UI
│   │   └── layout.tsx
│   ├── package.json
│   └── tailwind.config.ts
├── .gitignore
└── README.md
```

## 🧠 How It Works

### 1. PDF Parsing (Landing AI)
```python
response = requests.post(
    "https://api.va.landing.ai/v1/tools/agentic-document-analysis",
    files={"file": pdf},
    headers={"Authorization": f"Bearer {LANDING_AI_KEY}"}
)
# Extracts text with page numbers and bounding boxes
```

### 2. Vector Indexing
```python
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatIP(384)
index.add(embeddings)
```

### 3. RAG Query
```python
# 1. Embed query
query_vec = model.encode([question])

# 2. Search FAISS
scores, indices = index.search(query_vec, k=5)

# 3. Retrieve context
context = [documents[i] for i in indices[0]]

# 4. Generate with LLM
prompt = f"Context: {context}\n\nQuestion: {question}"
response = openrouter.generate(prompt, temperature=0.3)
```

## 🎯 Configuration

### Key Settings (`config.py`)
```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_RESULTS = 5
MIN_SIMILARITY_SCORE = 0.7
OPENROUTER_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"
TEMPERATURE = 0.3  # Low for factual accuracy
```

## 📈 Performance

- **Ingestion**: ~5-10 min for 20 PDFs + 4 CSVs
- **Indexing**: ~2-3 min for 34K documents
- **Query**: 200-500ms (retrieval + generation)
- **Index Size**: ~150MB
- **Memory**: ~2GB RAM

## 🧪 Testing

```bash
# Test ingestion
python backend/data_ingestion.py

# Test RAG
python backend/rag_pipeline.py

# Test API
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "COVID symptoms", "domain": "covid"}'
```

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- **Landing AI** - Agentic Document Extraction
- **OpenRouter** - LLM API access
- **ClinicalTrials.gov** - Clinical trial data
- **Meta AI** - FAISS vector search
- **UKP Lab** - Sentence Transformers

## 📧 Contact

**Arshan Bhanage**  
GitHub: [@ArshanBhanage](https://github.com/ArshanBhanage)  
Project: [Clinical-Assistant-RAG](https://github.com/ArshanBhanage/Clinical-Assistant-RAG)

---

**⚠️ Disclaimer**: Research prototype for educational purposes. Not a replacement for professional medical advice. Always consult licensed healthcare professionals.

## 🎓 Academic Context

Developed for Advanced Data Mining course demonstrating:
- Retrieval-Augmented Generation (RAG)
- Vector database implementation
- Multi-modal data ingestion (PDFs + CSVs)
- Real-world NLP in healthcare
- Production ML system design
