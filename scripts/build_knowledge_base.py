import json
import sys
import faiss
import numpy as np
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.fot_recommender.config import PROCESSED_DATA_DIR, RAW_KB_PATH # noqa: E402
from src.fot_recommender.semantic_chunker import chunk_by_concept # noqa: E402
from src.fot_recommender.rag_pipeline import (  # noqa: E402
    initialize_embedding_model,
    create_embeddings,
)


def build():
    """
    Builds the entire knowledge base artifact set needed by the application:
    1.  The processed, semantically chunked JSON file.
    2.  The Facebook AI Similarity Search (FAISS) vector index file (`faiss_index.bin`).
    """
    print("--- Building Final Knowledge Base and FAISS Index ---")

    # --- Create Final Chunks ---
    final_chunks_path = PROCESSED_DATA_DIR / "knowledge_base_final_chunks.json"
    print(f"Loading raw knowledge base from: {RAW_KB_PATH}")
    with open(RAW_KB_PATH, "r", encoding="utf-8") as f:
        raw_kb = json.load(f)

    final_chunks = chunk_by_concept(raw_kb)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(final_chunks_path, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=4)
    print(f"✅ Saved {len(final_chunks)} semantic chunks to {final_chunks_path}")

    # --- Create and Save FAISS Index ---
    faiss_index_path = PROCESSED_DATA_DIR / "faiss_index.bin"
    print("\n--- Creating FAISS Index ---")

    model = initialize_embedding_model()
    embeddings = create_embeddings(final_chunks, model)

    # Explicitly set dtype for FAISS
    embeddings = np.asarray(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)  # type: ignore

    faiss.write_index(index, str(faiss_index_path))
    print(f"✅ Saved FAISS index with {index.ntotal} vectors to {faiss_index_path}")

    print("\n🎉 Success! All artifacts are built and ready for the application.")


if __name__ == "__main__":
    build()
