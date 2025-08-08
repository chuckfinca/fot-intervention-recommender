import os

from dotenv.main import load_dotenv

from fot_recommender.config import PROCESSED_DATA_DIR
from fot_recommender.rag_pipeline import (
    load_knowledge_base,
    initialize_embedding_model,
    create_embeddings,
    create_vector_db,
    search_interventions,
    generate_recommendation_summary,
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
    print("--- FOT Intervention Recommender ---")

    # --- Load the final knowledge base ---
    final_chunks_path = PROCESSED_DATA_DIR / "knowledge_base_final_chunks.json"
    knowledge_base_chunks = load_knowledge_base(str(final_chunks_path))

    if not knowledge_base_chunks:
        print("Halting execution due to missing knowledge base.")
        return

    print(f"Successfully loaded {len(knowledge_base_chunks)} processed chunks.")
    print("-" * 50)

    # --- Vector Embedding Setup ---
    embedding_model = initialize_embedding_model()

    # --- Create Embeddings for Knowledge Base ---
    embeddings = create_embeddings(knowledge_base_chunks, embedding_model)

    # --- Set up FAISS Vector Database ---
    vector_db = create_vector_db(embeddings)

    print("-" * 50)

    # --- Test Retrieval with Sample Student Profile ---
    student_query = sample_student_profile["narrative_summary_for_embedding"]

    # Find the top 3 most relevant interventions
    top_interventions = search_interventions(
        query=student_query,
        model=embedding_model,
        index=vector_db,
        knowledge_base=knowledge_base_chunks,
        min_similarity_score=0.4,
        k=3,
    )

    if not top_interventions:
        print("Could not find relevant interventions for the student.")
        return

    # --- 4. Generate Synthesized Recommendation (for 'teacher' persona) ---
    load_dotenv()
    api_key = os.getenv("FOT_GOOGLE_API_KEY")
    if not api_key:
        return "ERROR: FOT_GOOGLE_API_KEY not found. Please create a .env file and add your key."

    synthesized_recommendation, _ = generate_recommendation_summary(
        top_interventions, student_query, api_key=api_key, persona="teacher"
    )

    # --- 5. Display Final Output ---
    print("\n" + "=" * 50)
    print("      FINAL SYNTHESIZED RECOMMENDATION FOR EDUCATOR")
    print("=" * 50 + "\n")
    print(synthesized_recommendation)

    print("\n" + "-" * 50)
    print("Evidence retrieved from the following sources:")
    for chunk, score in top_interventions:
        print(
            f"- {chunk['title']} (Source: {chunk['source_document']}, Relevance: {score:.2f})"
        )

    print("\n\n✅ Full RAG process complete!")


if __name__ == "__main__":
    main()
