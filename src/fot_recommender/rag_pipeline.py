import faiss  # type: ignore
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple


def load_knowledge_base(path: str) -> List[Dict[str, Any]]:
    """Loads the processed knowledge base from a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Knowledge base file not found at {path}")
        return []
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode the JSON file at {path}")
        return []


def initialize_embedding_model(
    model_name: str = "all-MiniLM-L6-v2",
) -> SentenceTransformer:
    """Initializes and returns a SentenceTransformer model."""
    print(f"Initializing embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Model initialized successfully.")
    return model


def create_embeddings(
    chunks: List[Dict[str, Any]],
    model: SentenceTransformer,
    content_key: str = "content_for_embedding",
) -> np.ndarray:
    """Creates vector embeddings for the content of each chunk."""
    print(f"Creating embeddings for {len(chunks)} chunks...")
    # Extract the content to be embedded
    content_to_embed = [chunk[content_key] for chunk in chunks]

    # Generate embeddings
    embeddings = model.encode(content_to_embed, show_progress_bar=True)
    print("Embeddings created successfully.")
    return embeddings


def create_vector_db(embeddings: np.ndarray) -> faiss.Index:
    """Creates and populates a FAISS vector database."""
    if embeddings.size == 0:
        raise ValueError("Cannot create vector DB with empty embeddings.")

    dimension = embeddings.shape[1]
    print(f"Creating FAISS index with dimension {dimension}...")

    # Explicitly set the dtype to float32 for FAISS compatibility
    embeddings = np.asarray(embeddings).astype("float32")

    # Using IndexFlatIP as planned for Maximum Inner Product search,
    # which is equivalent to cosine similarity for normalized vectors.
    index = faiss.IndexFlatIP(dimension)

    # The SentenceTransformer model ('all-MiniLM-L6-v2') produces normalized vectors.
    index.add(embeddings)  # type: ignore

    print(f"FAISS index created with {index.ntotal} vectors.")
    return index


def search_interventions(
    query: str,
    model: SentenceTransformer,
    index: faiss.Index,
    knowledge_base: List[Dict[str, Any]],
    k: int = 3,
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Performs a semantic search to find the most relevant interventions.

    Returns:
        A list of tuples, where each tuple contains the retrieved chunk
        and its similarity score.
    """
    print(f"\nSearching for top {k} interventions for query: '{query[:80]}...'")
    query_embedding = np.asarray(model.encode([query])).astype("float32")

    # FAISS search returns distances (scores) and indices of the top k results
    scores, indices = index.search(query_embedding, k)  # type: ignore

    # Assemble the results
    results = []
    for i, score in zip(indices[0], scores[0]):
        if i != -1:  # FAISS returns -1 for no result
            results.append((knowledge_base[i], score))

    print(f"Found {len(results)} relevant interventions.")
    return results
