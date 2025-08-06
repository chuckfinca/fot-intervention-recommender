from typing import List, Dict, Any, Tuple


def display_recommendations(results: List[Tuple[Dict[str, Any], float]]):
    """
    A helper function to neatly print the results of a semantic search.
    This function is designed to be called from a notebook or a command-line script.

    Args:
        results: A list of tuples, where each tuple contains a result chunk (dict)
                 and its similarity score (float).
    """
    if not results:
        print("\nNo relevant interventions were found for this query.")
        return

    print("\n--- Top Recommended Interventions ---")
    for i, (chunk, score) in enumerate(results):
        print(f"\n--- Recommendation {i + 1} (Similarity Score: {score:.4f}) ---")
        print(f"  Title: {chunk['title']}")
        print(f"  Source: {chunk['source_document']} ({chunk['fot_pages']})")

        # Indent the content for better readability
        content = chunk["original_content"]
        indented_content = "\n  ".join(content.splitlines())
        print(f'  \n  Content Snippet:\n  "{indented_content[:500]}..."')
        print("-" * 50)
