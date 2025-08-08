import faiss  # type: ignore
import json
import numpy as np
import google.generativeai as genai

from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
from fot_recommender.prompts import PROMPT_TEMPLATES
from fot_recommender.config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_CONTENT_KEY,
    GENERATIVE_MODEL_NAME,
    SEARCH_RESULT_COUNT_K,
    MIN_SIMILARITY_SCORE,
)


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
    model_name: str = EMBEDDING_MODEL_NAME,
) -> SentenceTransformer:
    """Initializes and returns a SentenceTransformer model."""
    print(f"Initializing embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Model initialized successfully.")
    return model


def create_embeddings(
    chunks: List[Dict[str, Any]],
    model: SentenceTransformer,
    content_key: str = EMBEDDING_CONTENT_KEY,
) -> np.ndarray:
    """Creates vector embeddings for the content of each chunk."""
    print(f"Creating embeddings for {len(chunks)} chunks...")
    content_to_embed = [chunk[content_key] for chunk in chunks]
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

    index.add(embeddings)  # type: ignore

    print(f"FAISS index created with {index.ntotal} vectors.")
    return index


def search_interventions(
    query: str,
    model: SentenceTransformer,
    index: faiss.Index,
    knowledge_base: List[Dict[str, Any]],
    k: int = SEARCH_RESULT_COUNT_K,
    min_similarity_score: float = MIN_SIMILARITY_SCORE,
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Performs a semantic search to find the most relevant interventions.

    Returns:
        A list of tuples, where each tuple contains the retrieved chunk
        and its similarity score.
    """
    print(f"\nSearching for top {k} interventions for query: '{query[:80]}...'")
    query_embedding = np.asarray(model.encode([query])).astype("float32")
    scores, indices = index.search(query_embedding, k)  # type: ignore
    results = []
    for i, score in zip(indices[0], scores[0]):
        if i != -1:  # FAISS returns -1 for no result
            results.append((knowledge_base[i], score))

    filtered_results = [
        (chunk, score) for chunk, score in results if score >= min_similarity_score
    ]

    print(f"Found {len(filtered_results)} relevant interventions.")
    return filtered_results


def generate_recommendation_summary(
    retrieved_chunks: List[Tuple[Dict[str, Any], float]],
    student_narrative: str,
    api_key: str,
    persona: str = "teacher",
    model_name: str = GENERATIVE_MODEL_NAME,
) -> Tuple[str, Dict[str, Any]]:  # Return text and a details dictionary
    """
    Generates a synthesized recommendation using the Google Gemini API.

    Returns:
        A tuple containing:
        - The synthesized recommendation text (str).
        - A dictionary with detailed prompt information for logging (Dict).
    """
    genai.configure(api_key=api_key)  # type: ignore

    prompt_details = {}
    if persona not in PROMPT_TEMPLATES:
        error_message = f"ERROR: Persona '{persona}' is not a valid choice."
        return error_message, {"error": error_message}

    context = ""
    for i, (chunk, _) in enumerate(retrieved_chunks):
        context += f"--- Intervention Chunk {i + 1} ---\n"
        context += f"Title: {chunk['title']}\n"
        context += f"Content: {chunk['original_content']}\n"
        context += f"(Source Document: {chunk['source_document']})\n\n"

    prompt_template = PROMPT_TEMPLATES[persona]
    prompt = prompt_template.format(
        student_narrative=student_narrative, context=context
    )

    # --- Assemble the prompt dictionary ---
    prompt_details = {
        "persona": persona,
        "llm_model_used": model_name,
        "prompt_template": prompt_template,
        "prompt_variables": {
            "student_narrative": student_narrative,
            "context": context,
        },
        "final_prompt_text": prompt,
    }

    try:
        print(
            f"\nSynthesizing recommendation for persona: '{persona}' using {model_name}..."
        )
        model = genai.GenerativeModel(model_name)  # type: ignore
        response = model.generate_content(prompt)
        print("Synthesis complete.")
        return response.text, prompt_details
    except Exception as e:
        error_message = f"An error occurred while calling the Gemini API: {e}"
        return error_message, prompt_details
