from unittest.mock import MagicMock, patch
import numpy as np


def test_search_interventions_filters_by_score():
    """
    Ensures the search function correctly filters out results
    that are below the minimum similarity score threshold.
    """
    from src.fot_recommender.rag_pipeline import search_interventions

    # 1. Arrange: Create mock objects and sample data
    mock_model = MagicMock()
    mock_index = MagicMock()

    # Fake knowledge base
    sample_kb = [{"id": 1, "content": "high score"}, {"id": 2, "content": "low score"}]

    # Configure the mock FAISS index to return specific scores and indices
    # Let's say it finds two results, one with a high score (0.9) and one low (0.3)
    mock_index.search.return_value = (
        np.array([[0.9, 0.3]]),  # scores
        np.array([[0, 1]]),  # indices
    )

    # 2. Act: Run the search with a minimum score of 0.5
    results = search_interventions(
        query="test query",
        model=mock_model,
        index=mock_index,
        knowledge_base=sample_kb,
        k=2,
        min_similarity_score=0.5,
    )

    # 3. Assert: Check that only the high-scoring result was returned
    assert len(results) == 1
    assert results[0][0]["content"] == "high score"  # Check the chunk content
    assert results[0][1] == 0.9  # Check the score


def test_generate_recommendation_summary_builds_correct_prompt():
    """
    Ensures that the context from retrieved chunks and the student narrative
    are correctly formatted into the final prompt sent to the LLM.
    """
    from src.fot_recommender.rag_pipeline import generate_recommendation_summary

    # 1. Arrange: Create sample inputs
    sample_chunks = [
        (
            {
                "title": "Tip 1",
                "original_content": "Do this.",
                "source_document": "doc_A",
            },
            0.9,
        ),
    ]
    student_narrative = "Student is struggling."

    # 2. Act & Assert: Use a patch to intercept the API call
    # This temporarily replaces genai.GenerativeModel with our mock
    with patch(
        "src.fot_recommender.rag_pipeline.genai.GenerativeModel"
    ) as mock_gen_model:
        # Create a mock instance that the function will use
        mock_model_instance = MagicMock()
        mock_gen_model.return_value = mock_model_instance

        generate_recommendation_summary(
            retrieved_chunks=sample_chunks,
            student_narrative=student_narrative,
            api_key="fake_key",
            persona="teacher",
        )

        # 3. Assert: Check what our function tried to do
        # Was the API call made once?
        mock_model_instance.generate_content.assert_called_once()

        # Get the actual prompt that was passed to the LLM
        actual_prompt = mock_model_instance.generate_content.call_args[0][0]

        # Check if our key pieces of information are in the prompt
        assert "Student is struggling." in actual_prompt
        assert "--- Intervention Chunk 1 ---" in actual_prompt
        assert "Title: Tip 1" in actual_prompt
        assert "Content: Do this." in actual_prompt
        assert "(Source Document: doc_A)" in actual_prompt
