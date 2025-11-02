"""
FastAPI backend for Clinical AI Assistant
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging
from datetime import datetime

from rag_pipeline import RAGPipeline
from visualizer import Visualizer
from config import DOMAINS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Clinical AI Assistant API",
    description="RAG-based clinical question answering system",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",  # Allow all Vercel domains
        "https://*.railway.app"   # Allow Railway domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline and visualizer
rag_pipeline = RAGPipeline()
visualizer = Visualizer()

# Load indexes on startup
@app.on_event("startup")
async def startup_event():
    """Load indexes when server starts"""
    try:
        rag_pipeline.load_indexes()
        print("RAG pipeline initialized successfully")
    except Exception as e:
        print(f"Warning: Could not load indexes: {e}")
        print("Please run data_ingestion.py and rag_pipeline.py first to build indexes")


# Pydantic models
class QueryRequest(BaseModel):
    query: str
    domain: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    confidence: str
    retrieved_docs: List[Dict[str, Any]]


class FeedbackRequest(BaseModel):
    query: str
    response: str
    rating: str  # "up" or "down"


class GraphRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    viz_type: str = "wordcloud"  # wordcloud, term_frequency, sources, similarity


# API endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Clinical AI Assistant API is running",
        "domains": list(DOMAINS.keys())
    }


@app.get("/domains")
async def get_domains():
    """Get available clinical domains"""
    return {
        "domains": [
            {
                "id": domain_id,
                "name": config["name"]
            }
            for domain_id, config in DOMAINS.items()
        ]
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a clinical query and return RAG response
    
    Args:
        request: QueryRequest with query text and optional domain
        
    Returns:
        QueryResponse with answer, sources, and confidence
    """
    start_time = datetime.now()
    
    try:
        # Log incoming request
        logger.info(f"📥 New query received:")
        logger.info(f"   Query: {request.query[:100]}...")
        logger.info(f"   Domain: {request.domain or 'All domains'}")
        
        if not request.query.strip():
            logger.warning(f"❌ Empty query rejected")
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Check if indexes are loaded
        if not rag_pipeline.indexes:
            logger.error(f"❌ RAG pipeline not initialized")
            raise HTTPException(
                status_code=503,
                detail="RAG pipeline not initialized. Please build indexes first."
            )
        
        # Validate domain if provided
        if request.domain and request.domain not in DOMAINS:
            logger.warning(f"❌ Invalid domain: {request.domain}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain. Valid domains: {list(DOMAINS.keys())}"
            )
        
        # Retrieve relevant documents
        logger.info(f"🔍 Retrieving documents...")
        retrieved_docs = rag_pipeline.retrieve(request.query, request.domain)
        logger.info(f"   Found {len(retrieved_docs)} relevant documents")
        
        # Generate response (OpenRouter call happens here - logged in rag_pipeline.py)
        logger.info(f"💬 Generating response...")
        result = rag_pipeline.generate_response(request.query, retrieved_docs)
        
        # Log completion
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Query completed:")
        logger.info(f"   Total time: {elapsed:.2f}s")
        logger.info(f"   Confidence: {result['confidence']}")
        logger.info(f"   Sources: {len(result['sources'])}")
        
        # Return complete response
        return QueryResponse(
            response=result["response"],
            sources=result["sources"],
            confidence=result["confidence"],
            retrieved_docs=retrieved_docs
        )
        
    except HTTPException:
        raise
    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ Query failed after {elapsed:.2f}s: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback (thumbs up/down)
    
    Note: This is a placeholder for future feedback collection
    """
    try:
        # Log feedback (in production, save to database)
        print(f"Feedback received: {request.rating} for query: '{request.query}'")
        
        return {
            "status": "success",
            "message": "Feedback recorded (will be extended in future)"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording feedback: {str(e)}")


@app.post("/generate-graph")
async def generate_graph(request: GraphRequest):
    """
    Generate visualization from query results
    
    Args:
        request: GraphRequest with query, domain, and visualization type
        
    Returns:
        Base64 encoded image
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Check if indexes are loaded
        if not rag_pipeline.indexes:
            raise HTTPException(
                status_code=503,
                detail="RAG pipeline not initialized. Please build indexes first."
            )
        
        # Retrieve relevant documents
        retrieved_docs = rag_pipeline.retrieve(request.query, request.domain, k=10)
        
        if not retrieved_docs:
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found for visualization"
            )
        
        # Generate visualization
        img_base64 = visualizer.generate_combined_visualization(
            retrieved_docs,
            request.viz_type
        )
        
        return {
            "image": img_base64,
            "viz_type": request.viz_type,
            "num_documents": len(retrieved_docs)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graph: {str(e)}")


@app.get("/health")
async def health_check():
    """Detailed health check"""
    index_status = {}
    
    for domain in DOMAINS.keys():
        if domain in rag_pipeline.indexes:
            index_status[domain] = {
                "loaded": True,
                "num_vectors": rag_pipeline.indexes[domain].ntotal
            }
        else:
            index_status[domain] = {
                "loaded": False,
                "num_vectors": 0
            }
    
    return {
        "status": "healthy",
        "indexes": index_status,
        "total_domains": len(DOMAINS)
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("Starting Clinical AI Assistant API")
    print("="*60)
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
