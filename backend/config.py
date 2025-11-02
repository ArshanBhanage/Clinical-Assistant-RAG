"""
Configuration settings for the Clinical AI Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
VISION_AGENT_API_KEY = os.getenv("VISION_AGENT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

# Paths - Support both local and deployment environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
INDEX_DIR = os.getenv("INDEX_DIR", os.path.join(BASE_DIR, "indexes"))

# For deployment: Check if /app/indexes exists (common deployment path)
if os.path.exists("/app/indexes") and not os.path.exists(INDEX_DIR):
    INDEX_DIR = "/app/indexes"

# Clinical domains - Using Clinical folder structure
DOMAINS = {
    "covid": {
        "name": "COVID Clinical Research",
        "data_path": f"{DATA_DIR}/Clinical/Covid",
        "pdf_folder": f"{DATA_DIR}/Clinical/Covid",
        "csv_files": [f"{DATA_DIR}/Clinical/ctg-studies_covid.csv"],
        "index_path": f"{INDEX_DIR}/covid_index.faiss",
        "metadata_path": f"{INDEX_DIR}/covid_metadata.pkl"
    },
    "diabetes": {
        "name": "Diabetes",
        "data_path": f"{DATA_DIR}/Clinical/Diabetes",
        "pdf_folder": f"{DATA_DIR}/Clinical/Diabetes",
        "csv_files": [f"{DATA_DIR}/Clinical/ctg-studies_diabetes.csv"],
        "index_path": f"{INDEX_DIR}/diabetes_index.faiss",
        "metadata_path": f"{INDEX_DIR}/diabetes_metadata.pkl"
    },
    "heart_attack": {
        "name": "Heart Attack",
        "data_path": f"{DATA_DIR}/Clinical/Heart_attack",
        "pdf_folder": f"{DATA_DIR}/Clinical/Heart_attack",
        "csv_files": [f"{DATA_DIR}/Clinical/ctg-studies_Hearattack.csv"],
        "index_path": f"{INDEX_DIR}/heart_attack_index.faiss",
        "metadata_path": f"{INDEX_DIR}/heart_attack_metadata.pkl"
    },
    "knee_injuries": {
        "name": "Knee Injuries",
        "data_path": f"{DATA_DIR}/Clinical/KneeInjuries",
        "pdf_folder": f"{DATA_DIR}/Clinical/KneeInjuries",
        "csv_files": [f"{DATA_DIR}/Clinical/ctg-studies_KneeInjuries.csv"],
        "index_path": f"{INDEX_DIR}/knee_injuries_index.faiss",
        "metadata_path": f"{INDEX_DIR}/knee_injuries_metadata.pkl"
    }
}

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval settings
TOP_K_RESULTS = 5
MIN_SIMILARITY_SCORE = 0.3

# OpenRouter settings
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
