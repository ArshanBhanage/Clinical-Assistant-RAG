"""
Retry ingestion for only the failed PDFs with new Landing AI API key
"""
import os
import pickle
from pathlib import Path
from data_ingestion import DataIngestion, LandingAIADE
from config import VISION_AGENT_API_KEY, DOMAINS

# PDFs that failed in the previous run
# FAILED_PDFS = {
#     "covid": ["COVID_Detection_using_Deep_Learning.pdf"],
#     "diabetes": [
#         "Artificial_Intelligence_and_Machine_Learning_for_Improving_Glycemic_Control_in_Diabetes_Best_Practices_Pitfalls_and_Opportunities.pdf",
#         "Knowledge-Infused_LLM-Powered_Conversational_Health_Agent_A_Case_Study_for_Diabetes_Patients.pdf",
#         "Improving_Self-Management_of_Type_2_Diabetes_Evaluating_the_Effectiveness_of_a_Mobile_App-Based_Patient_Education_Approach.pdf",
#         "Deep_Learning-Based_Genetic_Detection_and_Pathogenesis_of_Diabetes.pdf"
#     ],
#     "heart_attack": [
#         "Machine_Learning_Approaches_for_Predicting_Heart_Attacks.pdf",
#         "Machine_Learning_Model_for_Heart_Disease_Detection_A_Comparative_Analysis_of_SVM_vs_KNN.pdf"
#     ]
# }

FAILED_PDFS = {
    "covid": ["Extraction_of_Features_from_Lung_Image_for_the_Detection_of_Covid-19.pdf"],
    "diabetes": ["Deep_Learning-Based_Genetic_Detection_and_Pathogenesis_of_Diabetes.pdf"],
    "heart_attack": ["IOT_Based_Heart_Rate_Monitoring_System_Design_for_Heart_Attack_Detection.pdf"]
}

def retry_failed_pdfs():
    """Retry processing only the failed PDFs"""
    print("="*60)
    print("RETRYING FAILED PDFs WITH NEW API KEY")
    print("="*60)
    print(f"Using API key: {VISION_AGENT_API_KEY[:20]}...")
    print()
    
    # Load existing documents
    try:
        with open("indexes/all_documents.pkl", 'rb') as f:
            existing_docs = pickle.load(f)
        print(f"✓ Loaded existing documents")
        print()
    except Exception as e:
        print(f"Error loading existing documents: {e}")
        print("Please run data_ingestion.py first.")
        return
    
    # Initialize ADE parser
    ade = LandingAIADE(VISION_AGENT_API_KEY)
    
    total_new_chunks = 0
    
    for domain_key, pdf_list in FAILED_PDFS.items():
        if domain_key not in DOMAINS:
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing failed PDFs for: {DOMAINS[domain_key]['name']}")
        print(f"{'='*60}")
        
        pdf_folder = Path(DOMAINS[domain_key]["pdf_folder"])
        
        for pdf_name in pdf_list:
            pdf_path = pdf_folder / pdf_name
            
            if not pdf_path.exists():
                print(f"⚠ Warning: {pdf_name} not found")
                continue
            
            try:
                print(f"\n  Processing: {pdf_name}...")
                result = ade.parse(str(pdf_path))
                
                # Add chunks to existing documents
                new_docs = []
                for chunk in result["chunks"]:
                    if chunk.get("text"):
                        new_docs.append({
                            "text": chunk["text"],
                            "source": pdf_name,
                            "domain": domain_key,
                            "page": chunk.get("grounding", [{}])[0].get("page", 0) if chunk.get("grounding") else 0,
                            "chunk_type": chunk.get("chunk_type", "text"),
                            "chunk_id": chunk.get("chunk_id", ""),
                            "grounding": chunk.get("grounding", [])
                        })
                
                existing_docs[domain_key].extend(new_docs)
                total_new_chunks += len(new_docs)
                print(f"    ✓ Extracted {len(new_docs)} chunks")
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
    
    # Save updated documents
    if total_new_chunks > 0:
        with open("indexes/all_documents.pkl", 'wb') as f:
            pickle.dump(existing_docs, f)
        print(f"\n✓ Saved updated documents to indexes/all_documents.pkl")
    else:
        print("\n⚠ No new chunks were added")
    
    print("\n" + "="*60)
    print("UPDATED SUMMARY")
    print("="*60)
    for domain, docs in existing_docs.items():
        print(f"{domain}: {len(docs)} documents")
    print(f"\nTotal new chunks added: {total_new_chunks}")
    print("="*60)
    print()
    print("Next step: Run 'python rag_pipeline.py' to build indexes")

if __name__ == "__main__":
    retry_failed_pdfs()
