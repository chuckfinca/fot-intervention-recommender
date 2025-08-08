import datetime
import json
from IPython.display import display, Markdown


def display_recommendations(results: list, citations_map: dict):
    """
    Displays the retrieved recommendations in a rich, Markdown-formatted output
    directly within a Jupyter/Colab notebook by using the shared formatter.
    """
    if not results:
        display(Markdown("### No relevant interventions were found for this query."))
        return

    # 1. Get the formatted data from the shared function
    formatted_evidence = format_evidence_for_display(results, citations_map)

    display(Markdown("### Evidence Base"))

    # 2. Loop through the clean data and render it for the notebook
    for evidence in formatted_evidence:
        recommendation_md = f"""
**{evidence["title"]}**
- **Source:** {evidence["source"]}
- **Page(s):** {evidence["pages"]}
- **Relevance Score:** {evidence["score"]}
- **Content Snippet:**
> {evidence["content_snippet"]}

---
"""
        display(Markdown(recommendation_md))


def create_evaluation_bundle(
    student_narrative: str,
    persona: str,
    retrieved_chunks_with_scores: list,
    synthesized_recommendation: str,
    citations_map: dict,
) -> dict:
    """
    Assembles a comprehensive dictionary for evaluation and logging purposes.
    """
    evaluation_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "inputs": {
            "student_narrative": student_narrative,
            "persona": persona,
        },
        "retrieval_results": [
            {
                "chunk_title": chunk["title"],
                "relevance_score": float(score),
                "source_document": chunk["source_document"],
                "page_info": chunk.get("fot_pages", "N/A"),
                "original_content": chunk.get("original_content", ""),
                "citation_info": citations_map.get(chunk["source_document"], {}),
            }
            for chunk, score in retrieved_chunks_with_scores
        ],
        "llm_output": {"synthesized_recommendation": synthesized_recommendation},
    }
    return evaluation_data


def format_evidence_for_display(results: list, citations_map: dict) -> list:
    """
    Takes raw search results and formats them into a structured list of dictionaries
    ready for display in any environment.
    """
    evidence_list = []
    for chunk, score in results:
        source_doc = chunk.get("source_document", "N/A")
        citation_info = citations_map.get(source_doc, {})

        # Consolidate all the formatting logic here
        title = citation_info.get("title", "N/A")
        author = citation_info.get("author", "N/A")
        year = citation_info.get("year", "N/A")
        source_string = f"*{title}* ({author}, {year})."

        page_info = chunk.get("fot_pages", "N/A")

        original_content = chunk.get(
            "original_content", "Content not available."
        ).strip()
        blockquote_content = original_content.replace("\n", "\n> ")

        evidence_list.append(
            {
                "title": chunk["title"],
                "source": source_string,
                "pages": page_info,
                "score": f"{score:.2f}",
                "content_snippet": blockquote_content,
            }
        )

    return evidence_list


def load_citations(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            citations_list = json.load(f)
        return {item["source_document"]: item for item in citations_list}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
