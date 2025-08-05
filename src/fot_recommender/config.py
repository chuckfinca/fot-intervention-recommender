# src/fot_recommender/config.py

from pathlib import Path

# Define the root directory of the project
# This assumes your src folder is at the top level of your project
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Define paths to data and documentation files
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"

# Specific file paths
PDF_PATH = DATA_DIR / "source_pdfs" / "FOT_Toolkit_ToolSetC.pdf"
COMPLEXITY_MAP_PATH = DOCS_DIR / "document_complexity_map.csv"