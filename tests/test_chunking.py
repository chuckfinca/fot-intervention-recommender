def test_chunk_by_concept_groups_correctly():
    """
    Ensures that items are correctly grouped by (source_document, concept)
    and that their content is concatenated in the right order.
    """
    from src.fot_recommender.semantic_chunker import chunk_by_concept

    # 1. Arrange: Create simple, predictable raw data
    sample_raw_kb = [
        {"source_document": "doc_A", "concept": "Mentoring", "absolute_page": 1, "content": "First part."},
        {"source_document": "doc_B", "concept": "Tutoring", "absolute_page": 10, "content": "Tutoring info."},
        {"source_document": "doc_A", "concept": "Mentoring", "absolute_page": 2, "content": "Second part."},
    ]

    # 2. Act: Run the function we're testing
    final_chunks = chunk_by_concept(sample_raw_kb)

    # 3. Assert: Check the results
    assert len(final_chunks) == 2  # Should have grouped into 2 concepts

    # Find the 'Mentoring' chunk for detailed checks
    mentoring_chunk = next(c for c in final_chunks if c["title"] == "Mentoring")
    
    assert mentoring_chunk is not None
    assert mentoring_chunk["source_document"] == "doc_A"
    assert mentoring_chunk["fot_pages"] == "Pages: 1, 2"
    assert "First part.\n\nSecond part." in mentoring_chunk["original_content"]
    assert "Title: Mentoring. Content: First part.\n\nSecond part." in mentoring_chunk["content_for_embedding"]
    
