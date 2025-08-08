import os
from pathlib import Path
from dotenv import load_dotenv

# --- Load environment variables from .env file ---
load_dotenv()

# --- Core Project Paths ---
# Define the root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Define paths to data directories
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Define absolute paths to all data artifacts
RAW_KB_PATH = PROCESSED_DATA_DIR / "knowledge_base_raw.json"
FINAL_KB_CHUNKS_PATH = PROCESSED_DATA_DIR / "knowledge_base_final_chunks.json"
FAISS_INDEX_PATH = PROCESSED_DATA_DIR / "faiss_index.bin"
CITATIONS_PATH = PROCESSED_DATA_DIR / "citations.json"


# --- Model and RAG Pipeline Parameters ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GENERATIVE_MODEL_NAME = "gemini-1.5-flash-latest"
SEARCH_RESULT_COUNT_K = 3
MIN_SIMILARITY_SCORE = 0.4
# The key in the JSON chunk that contains the text to be embedded.
EMBEDDING_CONTENT_KEY = "content_for_embedding"


# --- Secrets Management ---
# Load secrets from the environment. The application will import these variables.
FOT_GOOGLE_API_KEY = os.environ.get("FOT_GOOGLE_API_KEY")
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "default_password") # Added a default for safety