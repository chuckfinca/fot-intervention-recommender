from .config import PROCESSED_DATA_DIR
from .rag_pipeline import (
    load_knowledge_base,
    initialize_embedding_model,
    create_embeddings,
    create_vector_db,
    search_interventions,
)

# --- Sample Student Profile from Project Description ---
sample_student_profile = {
    "student_id": "9th_Grader_A",
    "data_context": "End of First Semester",
    "indicators": {
        "credits_earned": 2.5,
        "core_course_failures": 1,
        "attendance_percentage": 88,
        "behavioral_flags": 1,
    },
    "narrative_summary_for_embedding": "This student is struggling to keep up with coursework, "
    "having failed one core class and earning only 2.5 credits out of 4 credits "
    "expected for the semester. Attendance is becoming a concern at 88% for an average "
    "annual target of 90%, and they have had one behavioral incident. "
    "The student needs targeted academic and attendance support to get back on track for graduation.",
}


def main():
    """
    Main entry point for the FOT Intervention Recommender application.
    This script now executes Phase 2 of the implementation plan:
    1. Loads the final, chunked knowledge base.
    2. Initializes the embedding model.
    3. Creates vector embeddings for the knowledge base.
    4. Sets up a FAISS vector database.
    5. Tests the retrieval system with the sample student profile.
    """
    print("--- FOT Intervention Recommender: Phase 2 ---")

    # --- Load the final knowledge base created in Phase 1 ---
    final_chunks_path = PROCESSED_DATA_DIR / "knowledge_base_final_chunks.json"
    knowledge_base_chunks = load_knowledge_base(str(final_chunks_path))

    if not knowledge_base_chunks:
        print("Halting execution due to missing knowledge base.")
        return

    print(f"Successfully loaded {len(knowledge_base_chunks)} processed chunks.")
    print("-" * 50)

    # --- Phase 2.1: Vector Embedding Setup ---
    embedding_model = initialize_embedding_model()

    # --- Phase 2.2: Create Embeddings for Knowledge Base ---
    embeddings = create_embeddings(knowledge_base_chunks, embedding_model)

    # --- Phase 2.3: Set up FAISS Vector Database ---
    vector_db = create_vector_db(embeddings)

    print("-" * 50)

    # --- Phase 2.4: Test Retrieval with Sample Student Profile ---
    student_query = sample_student_profile["narrative_summary_for_embedding"]

    # Find the top 3 most relevant interventions
    top_interventions = search_interventions(
        query=student_query,
        model=embedding_model,
        index=vector_db,
        knowledge_base=knowledge_base_chunks,
        k=3,
    )

    print("\n--- Top 3 Recommended Intervention Chunks ---")
    for i, (chunk, score) in enumerate(top_interventions):
        print(f"\n--- Recommendation {i + 1} (Score: {score:.4f}) ---")
        print(f"Title: {chunk['title']}")
        print(f"Source: {chunk['source_document']} ({chunk['fot_pages']})")
        # To keep the output clean, we'll show the first 300 chars of the content
        print(f"Content Snippet: {chunk['original_content'][:300]}...")

    print("-" * 50)
    print("\n✅ PHASE 2 (RAG Pipeline Implementation) is complete!")
    print(
        "The system can now retrieve relevant interventions based on a student narrative."
    )
    print(
        "\nNext step: Phase 3 - System Integration & Testing (Formatting the final output for educators)."
    )


if __name__ == "__main__":
    main()
