from pathlib import Path

# Define the root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Define paths to data files
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# The single source of truth for our knowledge base
RAW_KB_PATH = PROCESSED_DATA_DIR / "knowledge_base_raw.json"