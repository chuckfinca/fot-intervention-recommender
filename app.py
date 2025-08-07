import gradio as gr
import faiss
import os
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fot_recommender.rag_pipeline import ( # noqa: E402
    load_knowledge_base,
    initialize_embedding_model,
    generate_recommendation_summary,
)

ACCESS_PASSWORD = os.getenv("DEMO_PASSWORD", "innovare2025")

print("--- Initializing API: Loading models and data... ---")

FAISS_INDEX_PATH = "data/processed/faiss_index.bin"
KB_PATH = "data/processed/knowledge_base_final_chunks.json"

index = faiss.read_index(str(FAISS_INDEX_PATH))
knowledge_base_chunks = load_knowledge_base(str(KB_PATH))
embedding_model = initialize_embedding_model()

print("✅ API initialized successfully.")

# --- Define the core RAG function that the API exposes ---


def get_recommendations_api(student_narrative, persona, password):
    """The main function that runs the RAG pipeline, protected by a password."""
    if password != ACCESS_PASSWORD:
        return "Authentication failed. Please check the access key."
    if not student_narrative:
        return "Please enter a student narrative."

    # 1. RETRIEVE
    query_embedding = np.asarray(embedding_model.encode([student_narrative])).astype(
        "float32"
    )
    scores, indices = index.search(query_embedding, k=3)
    retrieved_chunks_with_scores = [
        (knowledge_base_chunks[i], score)
        for i, score in zip(indices[0], scores[0])
        if score >= 0.4
    ]
    if not retrieved_chunks_with_scores:
        return "Could not find relevant interventions for this query."

    # 2. GENERATE
    synthesized_recommendation = generate_recommendation_summary(
        retrieved_chunks=retrieved_chunks_with_scores,
        student_narrative=student_narrative,
        persona=persona,
    )

    # 3. Augment with evidence
    evidence_header = "\n\n---\n\n**Evidence Base:**"
    evidence_list = ""
    for chunk, score in retrieved_chunks_with_scores:
        evidence_list += f"\n- **{chunk['title']}** (Source: {chunk['source_document']}, Relevance: {score:.2f})"
    return synthesized_recommendation + evidence_header + evidence_list


# --- Create and launch the Gradio Interface ---
sample_narrative = "This student is struggling to keep up with coursework, having failed one core class and earning only 2.5 credits..."
interface = gr.Interface(
    fn=get_recommendations_api,
    inputs=[
        gr.Textbox(lines=5, label="Student Narrative", value=sample_narrative),
        gr.Radio(
            ["teacher", "parent", "principal"],
            label="Who is this for?",
            value="teacher",
        ),
        gr.Textbox(
            label="Access Key",
            type="password",
            info="Enter the access key provided for the demo.",
        ),
    ],
    outputs=gr.Markdown(label="Synthesized Recommendation", show_copy_button=True),
    title="Freshman On-Track Intervention Recommender API",
    description="A live API demonstrating the FOT Recommender. Enter the provided access key to use.",
    theme=gr.themes.Soft(), # type: ignore
).launch()
