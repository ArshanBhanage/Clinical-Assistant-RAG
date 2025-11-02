"""
RAG Pipeline: Retrieval and Generation using FAISS and OpenRouter
"""
import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import requests
import logging
from datetime import datetime

from config import (
    EMBEDDING_MODEL, 
    TOP_K_RESULTS, 
    MIN_SIMILARITY_SCORE,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    DOMAINS
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline using FAISS and OpenRouter"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.indexes = {}
        self.metadata = {}
        self.dimension = 384  # MiniLM embedding dimension
    
    def build_index(self, documents: List[Dict[str, Any]], domain: str):
        """
        Build FAISS index for a specific domain
        
        Args:
            documents: List of document dictionaries with text and metadata
            domain: Clinical domain identifier
        """
        if not documents:
            print(f"Warning: No documents to index for domain {domain}")
            return
        
        print(f"\nBuilding index for {domain}...")
        print(f"  Total documents: {len(documents)}")
        
        # Extract texts
        texts = [doc["text"] for doc in documents]
        
        # Generate embeddings
        print(f"  Generating embeddings...")
        embeddings = self.embedding_model.encode(
            texts, 
            convert_to_numpy=True,
            show_progress_bar=True
        ).astype('float32')
        
        # Normalize for cosine similarity (using IndexFlatIP for inner product)
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        index = faiss.IndexFlatIP(self.dimension)
        index.add(embeddings)
        
        # Store index and metadata
        self.indexes[domain] = index
        self.metadata[domain] = documents
        
        print(f"  Index built with {index.ntotal} vectors")
    
    def build_all_indexes(self, all_documents: Dict[str, List[Dict[str, Any]]]):
        """Build indexes for all domains"""
        for domain, documents in all_documents.items():
            self.build_index(documents, domain)
    
    def save_indexes(self):
        """Save all indexes and metadata to disk"""
        for domain in self.indexes.keys():
            domain_config = DOMAINS[domain]
            
            # Save FAISS index
            index_path = domain_config["index_path"]
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            faiss.write_index(self.indexes[domain], index_path)
            
            # Save metadata
            metadata_path = domain_config["metadata_path"]
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata[domain], f)
            
            print(f"Saved index for {domain} to {index_path}")
    
    def load_indexes(self):
        """Load all indexes and metadata from disk"""
        for domain, domain_config in DOMAINS.items():
            index_path = domain_config["index_path"]
            metadata_path = domain_config["metadata_path"]
            
            if os.path.exists(index_path) and os.path.exists(metadata_path):
                # Load FAISS index
                self.indexes[domain] = faiss.read_index(index_path)
                
                # Load metadata
                with open(metadata_path, 'rb') as f:
                    self.metadata[domain] = pickle.load(f)
                
                print(f"Loaded index for {domain}: {self.indexes[domain].ntotal} vectors")
            else:
                print(f"Warning: Index files not found for {domain}")
    
    def retrieve(self, query: str, domain: Optional[str] = None, k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            domain: Specific domain to search (None for all domains)
            k: Number of top results to retrieve
            
        Returns:
            List of relevant documents with scores
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            [query], 
            convert_to_numpy=True
        ).astype('float32')
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        all_results = []
        
        # Search in specified domain or all domains
        domains_to_search = [domain] if domain else list(self.indexes.keys())
        
        for search_domain in domains_to_search:
            if search_domain not in self.indexes:
                continue
            
            index = self.indexes[search_domain]
            metadata = self.metadata[search_domain]
            
            # Search
            scores, indices = index.search(query_embedding, k)
            
            # Collect results
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(metadata) and score >= MIN_SIMILARITY_SCORE:
                    result = metadata[idx].copy()
                    result["similarity_score"] = float(score)
                    all_results.append(result)
        
        # Sort by score and return top k
        all_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return all_results[:k]
    
    def generate_response(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate response using OpenRouter LLM
        
        Args:
            query: User query
            retrieved_docs: List of retrieved documents
            
        Returns:
            Dictionary with response and metadata
        """
        if not retrieved_docs:
            return {
                "response": "I couldn't find sufficient information in the provided datasets to answer your question. Please try rephrasing your query or ask about a different topic within the clinical domains (COVID, Diabetes/Heart Attack, or Knee Injuries).",
                "sources": [],
                "confidence": "low"
            }
        
        # Build context from retrieved documents
        context_blocks = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs[:5]):  # Top 5 for evidence
            source_info = f"[Source {i+1}: {doc['source']}, Page {doc['page']}]"
            context_blocks.append(f"{source_info}\n{doc['text']}\n")
            
            sources.append({
                "source": doc["source"],
                "page": doc["page"],
                "chunk_type": doc["chunk_type"],
                "similarity": doc["similarity_score"],
                "text": doc["text"][:500]  # Include first 500 chars of text as evidence
            })
        
        context = "\n".join(context_blocks)
        
        # Create prompt
        prompt = f"""You are a Clinical AI Assistant that provides accurate medical information based ONLY on the provided context. You must follow these rules strictly:

1. ONLY use information from the context below to answer the question
2. If the context doesn't contain enough information, explicitly state that
3. Cite sources using the [Source X] format provided in the context
4. Do not use any external knowledge or information from the internet
5. Be precise and clinical in your language
6. If you're uncertain, say so clearly

Context:
{context}

Question: {query}

Answer (cite sources and be concise):"""
        
        # Call OpenRouter API
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://clinical-ai-assistant.local",
                "X-Title": "Clinical AI Assistant"
            }
            
            payload = {
                "model": OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful medical AI assistant that only uses provided context to answer questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            # Log OpenRouter request
            logger.info(f"🚀 OpenRouter API Call:")
            logger.info(f"   Model: {OPENROUTER_MODEL}")
            logger.info(f"   Query: {query[:100]}...")
            logger.info(f"   Context docs: {len(retrieved_docs)}")
            logger.info(f"   Prompt length: {len(prompt)} chars")
            
            start_time = datetime.now()
            
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                
                # Log successful response
                logger.info(f"✅ OpenRouter Response:")
                logger.info(f"   Status: 200 OK")
                logger.info(f"   Response time: {elapsed:.2f}s")
                logger.info(f"   Response length: {len(answer)} chars")
                
                # Log usage if available
                if "usage" in result:
                    usage = result["usage"]
                    logger.info(f"   Token usage: {usage.get('total_tokens', 'N/A')} "
                              f"(prompt: {usage.get('prompt_tokens', 'N/A')}, "
                              f"completion: {usage.get('completion_tokens', 'N/A')})")
                
                # Log cost if available
                if "cost" in result:
                    logger.info(f"   Cost: ${result['cost']:.6f}")
                
                return {
                    "response": answer,
                    "sources": sources,
                    "confidence": "high" if len(retrieved_docs) >= 3 else "medium"
                }
            else:
                # Log error response
                logger.error(f"❌ OpenRouter Error:")
                logger.error(f"   Status: {response.status_code}")
                logger.error(f"   Response time: {elapsed:.2f}s")
                logger.error(f"   Error: {response.text[:200]}")
                
                return {
                    "response": f"Error generating response: {response.status_code}",
                    "sources": sources,
                    "confidence": "error"
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"❌ OpenRouter Timeout:")
            logger.error(f"   Request exceeded 30 seconds")
            return {
                "response": "Error: Request timed out. Please try again.",
                "sources": sources,
                "confidence": "error"
            }
        except Exception as e:
            logger.error(f"❌ OpenRouter Exception:")
            logger.error(f"   Error: {str(e)}")
            logger.exception("Full traceback:")
            return {
                "response": f"Error calling LLM: {str(e)}",
                "sources": sources,
                "confidence": "error"
            }
    
    def query(self, query_text: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve and generate
        
        Args:
            query_text: User's natural language query
            domain: Optional domain to restrict search
            
        Returns:
            Response dictionary with answer and sources
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query_text, domain)
        
        # Generate response
        response = self.generate_response(query_text, retrieved_docs)
        
        return response


if __name__ == "__main__":
    # Test RAG pipeline
    from data_ingestion import DataIngestion
    
    # Load or create documents
    ingestion = DataIngestion()
    
    if os.path.exists("indexes/all_documents.pkl"):
        all_docs = ingestion.load_documents()
    else:
        all_docs = ingestion.ingest_all_domains()
        ingestion.save_documents()
    
    # Build RAG pipeline
    rag = RAGPipeline()
    rag.build_all_indexes(all_docs)
    rag.save_indexes()
    
    # Test query
    test_query = "What are the symptoms of COVID-19?"
    print(f"\n{'='*60}")
    print(f"Test Query: {test_query}")
    print(f"{'='*60}")
    
    result = rag.query(test_query)
    print(f"\nResponse: {result['response']}")
    print(f"\nConfidence: {result['confidence']}")
    print(f"\nSources: {len(result['sources'])}")
