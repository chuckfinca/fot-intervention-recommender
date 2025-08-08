import gradio as gr
import faiss
import json
import tempfile
import datetime
import numpy as np
import sys
from pathlib import Path

APP_ROOT = Path(__file__).parent
sys.path.insert(0, str(APP_ROOT / "src"))

from fot_recommender.config import ( # noqa: E402
    FAISS_INDEX_PATH,
    FINAL_KB_CHUNKS_PATH,
    CITATIONS_PATH,
    FOT_GOOGLE_API_KEY,
    DEMO_PASSWORD,
    SEARCH_RESULT_COUNT_K,
    MIN_SIMILARITY_SCORE,
)
from fot_recommender.utils import load_citations, format_evidence_for_display # noqa: E402
from fot_recommender.rag_pipeline import ( # noqa: E402
    load_knowledge_base,
    initialize_embedding_model,
    generate_recommendation_summary,
)

# --- Define Example Narratives for the UI (with new 'short_title') ---
EXAMPLE_NARRATIVES = [
    {
        "short_title": "Overwhelmed",
        "title": "Overwhelmed Freshman (Academic & Attendance)",
        "narrative": "A comprehensive support plan is urgently needed for this freshman. Academic performance is a critical concern, with failures in both Math and English leading to a credit deficiency of only 2 out of 4 expected credits. This academic struggle is compounded by a drop in attendance to 85% and a recent behavioral flag for an outburst in class, suggesting the student is significantly overwhelmed by the transition to high school.",
    },
    {
        "short_title": "Withdrawn",
        "title": "Withdrawn Freshman (Social-Emotional)",
        "narrative": "Academically, this freshman appears to be thriving, with a high GPA and perfect attendance. A closer look at classroom performance, however, reveals a student who is completely withdrawn. They do not participate in discussions or engage in any extracurricular activities, and teacher notes repeatedly describe them as 'isolated.' The lack of behavioral flags is a result of non-engagement, not positive conduct, pointing to a clear need for interventions focused on social-emotional learning and school connectedness.",
    },
    {
        "short_title": "Disruptive",
        "title": "Disruptive Freshman (Behavioral)",
        "narrative": "While this student's academics and credits earned are currently on track and attendance is acceptable at 92%, a significant pattern of disruptive behavior is jeopardizing their long-term success. An accumulation of five behavioral flags across multiple classes indicates a primary need for interventions in behavior management and positive conduct. Support should be focused on mentoring and strategies to foster appropriate classroom engagement before these behaviors begin to negatively impact their academic standing.",
    },
]
EXAMPLE_MAP = {ex["short_title"]: ex["narrative"] for ex in EXAMPLE_NARRATIVES}
EXAMPLE_TITLES = list(EXAMPLE_MAP.keys())

# --- Initialize models and data ---
print("--- Initializing API: Loading models and data... ---")
index = faiss.read_index(str(FAISS_INDEX_PATH))
knowledge_base_chunks = load_knowledge_base(str(FINAL_KB_CHUNKS_PATH))
citations_map = load_citations(str(CITATIONS_PATH))
embedding_model = initialize_embedding_model()
print("✅ API initialized successfully.")


def get_recommendations_api(student_narrative, persona, password):
    """The main function that runs the RAG pipeline and prepares data for export."""
    if password != DEMO_PASSWORD:
        yield (
            "Authentication failed. Please enter a valid Access Key.",
            gr.update(interactive=True),
            gr.update(visible=False),
            None,
            gr.update(visible=False),
        )
        return

    if not FOT_GOOGLE_API_KEY:
        yield (
            "ERROR: The Google API Key is not configured. Please set the FOT_GOOGLE_API_KEY in the .env file.",
            gr.update(interactive=True),
            gr.update(visible=False),
            None,
            gr.update(visible=False),
        )
        return

    if not student_narrative:
        yield (
            "Please enter a student narrative.",
            gr.update(interactive=True),
            gr.update(visible=False),
            None,
            gr.update(visible=False),
        )
        return

    yield (
        "Processing...",
        gr.update(interactive=False),
        gr.update(visible=False),
        None,
        gr.update(visible=False),
    )

    # 1. RETRIEVE
    query_embedding = np.asarray(embedding_model.encode([student_narrative])).astype(
        "float32"
    )
    scores, indices = index.search(query_embedding, k=SEARCH_RESULT_COUNT_K)
    retrieved_chunks_with_scores = [
        (knowledge_base_chunks[i], score)
        for i, score in zip(indices[0], scores[0])
        if score >= MIN_SIMILARITY_SCORE
    ]

    if not retrieved_chunks_with_scores:
        yield (
            "Could not find relevant interventions.",
            gr.update(interactive=True),
            gr.update(visible=False),
            None,
            gr.update(visible=False),
        )
        return

    # 2. GENERATE
    synthesized_recommendation, llm_prompt_details = generate_recommendation_summary(
        retrieved_chunks=retrieved_chunks_with_scores,
        student_narrative=student_narrative,
        api_key=FOT_GOOGLE_API_KEY,
        persona=persona,
    )

    # 3. Augment with evidence for UI
    formatted_evidence = format_evidence_for_display(
        retrieved_chunks_with_scores, citations_map
    )
    evidence_header = "\n\n---\n\n### Evidence Base\n"
    evidence_list_str = ""
    for evidence in formatted_evidence:
        evidence_list_str += f"\n- **{evidence['title']}**\n"
        evidence_list_str += f"  - **Source:** {evidence['source']}\n"
        evidence_list_str += f"  - **Page(s):** {evidence['pages']}\n"
        evidence_list_str += f"  - **Relevance Score:** {evidence['score']}\n"
        evidence_list_str += (
            f"  - **Content Snippet:**\n  > {evidence['content_snippet']}\n"
        )
    final_ui_output = synthesized_recommendation + evidence_header + evidence_list_str

    # 4. Assemble Evaluation Data
    evaluation_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "inputs": {"student_narrative": student_narrative, "persona": persona},
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
        "llm_prompt_details": llm_prompt_details,
        "outputs": {
            "llm_synthesized_recommendation": synthesized_recommendation,
            "final_formatted_ui_output": final_ui_output,
        },
    }

    # 5. Create a temporary file for download
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as f:
        json.dump(evaluation_data, f, indent=4)
        temp_file_path = f.name

    yield (
        final_ui_output,
        gr.update(interactive=True),
        gr.update(visible=True),
        evaluation_data,
        gr.update(value=temp_file_path, visible=True),
    )


# --- UI Helper Functions ---
def clear_all():
    return (
        "",
        None,
        "",
        gr.update(visible=False),
        None,
        gr.update(visible=False, value=None),
    )


def update_narrative_from_example(selection):
    return EXAMPLE_MAP.get(selection, "")


CUSTOM_CSS = """
.radio-horizontal .gr-form { flex-direction: row; flex-wrap: wrap; gap: 0.5rem; }
"""

# --- Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), css=CUSTOM_CSS) as interface:  # type: ignore
    gr.Markdown(
        "# Freshman On-Track Intervention Recommender\n*A live API demonstrating the FOT Recommender.*"
    )
    with gr.Row(equal_height=False):
        with gr.Column(scale=1):
            with gr.Group():
                narrative_input = gr.Textbox(
                    lines=8,
                    label="Student Narrative",
                    placeholder="Describe the student's situation here, or select an example below.",
                )
                example_radio = gr.Radio(
                    EXAMPLE_TITLES,
                    label="Load an Example Scenario",
                    info="Select one to populate the narrative above. Typing a custom narrative will clear this selection.",
                    elem_classes=["radio-horizontal"],
                )
                persona_input = gr.Radio(
                    ["teacher", "parent", "principal"],
                    label="Who is this recommendation for?",
                    value="teacher",
                    elem_classes=["radio-horizontal"],
                )
                password_input = gr.Textbox(
                    label="Access Key",
                    type="password",
                    info="Enter the access key for the demo.",
                )
                with gr.Row():
                    clear_btn = gr.Button("Clear")
                    submit_btn = gr.Button("Submit", variant="primary")
        with gr.Column(scale=2):
            recommendation_output = gr.Markdown(
                label="Synthesized Recommendation", show_copy_button=True
            )
            with gr.Accordion(
                "Evaluation Data", open=False, visible=False
            ) as eval_accordion:
                json_viewer = gr.JSON(label="Evaluation JSON")
                download_btn = gr.DownloadButton("Download JSON", visible=False)

    # --- Event Handlers ---
    example_radio.change(
        fn=update_narrative_from_example, inputs=example_radio, outputs=narrative_input
    )
    narrative_input.input(fn=lambda: None, inputs=None, outputs=example_radio)
    submit_btn.click(
        fn=get_recommendations_api,
        inputs=[narrative_input, persona_input, password_input],
        outputs=[
            recommendation_output,
            submit_btn,
            eval_accordion,
            json_viewer,
            download_btn,
        ],
    )
    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            narrative_input,
            example_radio,
            recommendation_output,
            eval_accordion,
            json_viewer,
            download_btn,
        ],
    )


if __name__ == "__main__":
    interface.launch()
