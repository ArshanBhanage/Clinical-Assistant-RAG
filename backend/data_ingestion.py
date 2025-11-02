"""
Data ingestion module using Landing AI's Agentic Document Extraction (ADE)
"""
import os
import json
import pickle
import requests
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path

from config import VISION_AGENT_API_KEY, DOMAINS


class LandingAIADE:
    """Wrapper for Landing AI Agentic Document Extraction API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"
    
    def parse(self, document_path: str, include_marginalia: bool = True, 
              include_metadata_in_markdown: bool = True) -> Dict[str, Any]:
        """
        Parse a PDF document using Landing AI ADE
        
        Args:
            document_path: Path to the PDF file
            include_marginalia: Whether to include headers, footers, etc.
            include_metadata_in_markdown: Whether to include metadata in markdown
            
        Returns:
            Dict containing markdown, chunks, and metadata
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        with open(document_path, 'rb') as pdf_file:
            files = {
                'pdf': (os.path.basename(document_path), pdf_file, 'application/pdf')
            }
            
            data = {
                'include_marginalia': str(include_marginalia).lower(),
                'include_metadata_in_markdown': str(include_metadata_in_markdown).lower(),
                'enable_rotation_detection': 'false'
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "markdown": result.get("data", {}).get("markdown", ""),
                    "chunks": result.get("data", {}).get("chunks", []),
                    "document_url": document_path,
                    "errors": result.get("errors", [])
                }
            else:
                raise Exception(f"ADE API Error: {response.status_code} - {response.text}")


class DataIngestion:
    """Handles ingestion of PDFs and structured data"""
    
    def __init__(self):
        self.ade = LandingAIADE(VISION_AGENT_API_KEY)
        self.all_documents = {}
    
    def process_pdf_folder(self, domain: str, pdf_folder: str) -> List[Dict[str, Any]]:
        """
        Process all PDFs in a folder for a given domain
        
        Args:
            domain: Clinical domain (covid, diabetes_heart, knee_injuries)
            pdf_folder: Path to folder containing PDFs
            
        Returns:
            List of processed documents with chunks
        """
        documents = []
        pdf_folder_path = Path(pdf_folder)
        
        if not pdf_folder_path.exists():
            print(f"Warning: PDF folder {pdf_folder} does not exist. Creating it...")
            pdf_folder_path.mkdir(parents=True, exist_ok=True)
            return documents
        
        pdf_files = list(pdf_folder_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"Warning: No PDF files found in {pdf_folder}")
            return documents
        
        print(f"\nProcessing {len(pdf_files)} PDFs for domain: {domain}")
        
        for pdf_file in pdf_files:
            try:
                print(f"  Processing: {pdf_file.name}...")
                result = self.ade.parse(str(pdf_file))
                
                # Extract chunks with metadata
                for chunk in result["chunks"]:
                    if chunk.get("text"):
                        documents.append({
                            "text": chunk["text"],
                            "source": pdf_file.name,
                            "domain": domain,
                            "page": chunk.get("grounding", [{}])[0].get("page", 0) if chunk.get("grounding") else 0,
                            "chunk_type": chunk.get("chunk_type", "text"),
                            "chunk_id": chunk.get("chunk_id", ""),
                            "grounding": chunk.get("grounding", [])
                        })
                
                print(f"    Extracted {len([c for c in result['chunks'] if c.get('text')])} chunks")
                
            except Exception as e:
                print(f"    Error processing {pdf_file.name}: {str(e)}")
        
        return documents
    
    def process_csv_files(self, domain: str, csv_files: List[str]) -> List[Dict[str, Any]]:
        """
        Process CSV/JSON files containing semi-structured clinical data
        
        Args:
            domain: Clinical domain
            csv_files: List of CSV/JSON file paths
            
        Returns:
            List of documents extracted from structured data
        """
        documents = []
        
        for file_path in csv_files:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                print(f"Warning: File {file_path} does not exist")
                continue
            
            try:
                # Read CSV or JSON
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.json'):
                    df = pd.read_json(file_path)
                else:
                    print(f"Unsupported file format: {file_path}")
                    continue
                
                # Convert each row to a text document
                for idx, row in df.iterrows():
                    # Create a textual representation of the row
                    text_parts = []
                    for col in df.columns:
                        value = row[col]
                        if pd.notna(value):
                            text_parts.append(f"{col}: {value}")
                    
                    text = " | ".join(text_parts)
                    
                    documents.append({
                        "text": text,
                        "source": file_path_obj.name,
                        "domain": domain,
                        "page": 0,
                        "chunk_type": "structured_data",
                        "chunk_id": f"row_{idx}",
                        "grounding": []
                    })
                
                print(f"Processed {len(df)} rows from {file_path_obj.name}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        return documents
    
    def ingest_all_domains(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Ingest data for all clinical domains
        
        Returns:
            Dictionary mapping domain to list of documents
        """
        all_docs = {}
        
        for domain_key, domain_config in DOMAINS.items():
            print(f"\n{'='*60}")
            print(f"Ingesting data for domain: {domain_config['name']}")
            print(f"{'='*60}")
            
            documents = []
            
            # Process PDFs
            pdf_folder = domain_config["pdf_folder"]
            pdf_docs = self.process_pdf_folder(domain_key, pdf_folder)
            documents.extend(pdf_docs)
            
            # Process CSV/JSON files
            csv_files = domain_config.get("csv_files", [])
            if csv_files:
                csv_docs = self.process_csv_files(domain_key, csv_files)
                documents.extend(csv_docs)
            
            all_docs[domain_key] = documents
            print(f"\nTotal documents for {domain_key}: {len(documents)}")
        
        self.all_documents = all_docs
        return all_docs
    
    def save_documents(self, output_path: str = "indexes/all_documents.pkl"):
        """Save processed documents to disk"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            pickle.dump(self.all_documents, f)
        print(f"\nSaved all documents to {output_path}")
    
    def load_documents(self, input_path: str = "indexes/all_documents.pkl") -> Dict[str, List[Dict[str, Any]]]:
        """Load processed documents from disk"""
        with open(input_path, 'rb') as f:
            self.all_documents = pickle.load(f)
        return self.all_documents


if __name__ == "__main__":
    # Test data ingestion
    ingestion = DataIngestion()
    all_docs = ingestion.ingest_all_domains()
    ingestion.save_documents()
    
    # Print summary
    print("\n" + "="*60)
    print("INGESTION SUMMARY")
    print("="*60)
    for domain, docs in all_docs.items():
        print(f"{domain}: {len(docs)} documents")
