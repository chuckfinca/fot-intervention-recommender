import json
import sys
import faiss
import numpy as np
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# We are intentionally ignoring the E402 warning here because the sys.path
# modification must happen before we can import from our local package.
from src.fot_recommender.config import (  # noqa: E402
    PROCESSED_DATA_DIR,
    RAW_KB_PATH,
    FINAL_KB_CHUNKS_PATH,
    FAISS_INDEX_PATH,
    EMBEDDING_MODEL_NAME,
)
from src.fot_recommender.semantic_chunker import chunk_by_concept  # noqa: E402
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
    print(f"Loading raw knowledge base from: {RAW_KB_PATH}")
    with open(RAW_KB_PATH, "r", encoding="utf-8") as f:
        raw_kb = json.load(f)

    final_chunks = chunk_by_concept(raw_kb)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FINAL_KB_CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, indent=4)
    print(f"✅ Saved {len(final_chunks)} semantic chunks to {FINAL_KB_CHUNKS_PATH}")

    # --- Create and Save FAISS Index ---
    print("\n--- Creating FAISS Index ---")

    # Initialize model using the name from the config file
    model = initialize_embedding_model(model_name=EMBEDDING_MODEL_NAME)
    embeddings = create_embeddings(final_chunks, model)

    # Explicitly set dtype for FAISS
    embeddings = np.asarray(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)  # type: ignore

    faiss.write_index(index, str(FAISS_INDEX_PATH))
    print(f"✅ Saved FAISS index with {index.ntotal} vectors to {FAISS_INDEX_PATH}")

    print("\n🎉 Success! All artifacts are built and ready for the application.")


if __name__ == "__main__":
    build()
