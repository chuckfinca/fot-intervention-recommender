import json
import sys
from pathlib import Path

# This allows the script to find and import modules from your 'src' directory
# by adding the project's root folder to the list of paths Python searches.
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.fot_recommender.config import RAW_KB_PATH, PROCESSED_DATA_DIR  # noqa: E402
from src.fot_recommender.semantic_chunker import chunk_by_concept  # noqa: E402


def build():
    """
    This script performs the knowledge base build process.
    1. Loads the raw, manually curated knowledge base.
    2. Uses the semantic chunker to group entries by concept.
    3. Saves the final, consolidated chunks to the file that the main
       RAG pipeline expects ('knowledge_base_final_chunks.json').
    """
    print("--- Building Final Knowledge Base ---")

    # Define the path for the output file
    final_chunks_path = PROCESSED_DATA_DIR / "knowledge_base_final_chunks.json"

    # 1. Load the raw knowledge base file
    print(f"Loading raw knowledge base from: {RAW_KB_PATH}")
    try:
        with open(RAW_KB_PATH, "r", encoding="utf-8") as f:
            raw_kb = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Raw knowledge base file not found at {RAW_KB_PATH}. Halting.")
        return

    print(f"Loaded {len(raw_kb)} raw entries.")

    # 2. Process and chunk the knowledge base using the existing chunker
    print("Applying semantic chunking to consolidate related content...")
    final_chunks = chunk_by_concept(raw_kb)
    print(f"Created {len(final_chunks)} final semantic chunks.")

    # 3. Save the final chunked file
    print(f"Saving final chunked knowledge base to: {final_chunks_path}")

    # Ensure the 'processed' directory exists before trying to write to it
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(final_chunks_path, "w", encoding="utf-8") as f:
        # We use indent=4 to make the final JSON file human-readable,
        # which is extremely helpful for debugging and verification.
        json.dump(final_chunks, f, indent=4)

    print("\n✅ Success! The final knowledge base is built and ready.")
    print("You can now run the main application.")


if __name__ == "__main__":
    build()
