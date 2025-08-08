---
title: Fot Recommender Api
emoji: ⚡
colorFrom: green
colorTo: pink
sdk: gradio
sdk_version: 5.41.0
python_version: "3.12"
app_file: app.py
pinned: false
license: mit
short_description: POC - Freshman On-Track RAG Intervention Recommender
---


# Freshman On-Track (FOT) Intervention Recommender

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/chuckfinca/fot-recommender-api)

This repository contains the proof-of-concept for the Freshman On-Track (FOT) Intervention Recommender, an AI-powered tool designed to empower educators.

## 🚀 Live Demo

The full application is deployed as an interactive web API on Hugging Face Spaces.

**[👉 Click Here to Launch the Live FOT Recommender API](https://huggingface.co/spaces/chuckfinca/fot-recommender-api)**

**Note on Access:** The public demo is protected by an access key. If you would like to try the live application, please **[open a GitHub issue in this repository](https://github.com/chuckfinca/fot-intervention-recommender/issues/new)** to request access, and I will be happy to provide a key.

## 1. Project Goal

Freshman year performance is the strongest predictor of high school graduation. However, educators often lack systematic tools to match at-risk 9th graders with the specific, evidence-based interventions they need.

This project addresses that gap by providing a **Retrieval-Augmented Generation (RAG)** system that transforms a simple narrative about a student's challenges into a set of clear, actionable, and evidence-based recommendations. It turns scattered educational research into targeted guidance, enabling educators to support their students more effectively.

## 2. Features

*   **Advanced RAG Architecture**: Utilizes a sophisticated pipeline to ensure recommendations are relevant and grounded in evidence.
    *   **Retrieval**: Employs a `FAISS` vector database and the `all-MiniLM-L6-v2` sentence-transformer model to perform semantic search over the knowledge base.
    *   **Generation**: Uses Google's `gemini-1.5-flash-latest` model to synthesize the retrieved evidence into a coherent, actionable plan.
*   **Persona-Based Recommendations**: Delivers tailored advice for different audiences, fulfilling a key project bonus goal. The system can generate distinct outputs for a **teacher**, **parent**, or **principal**.
*   **Evidence-Backed**: Every recommendation is based on a curated knowledge base of best-practice documents from reputable sources like the Network for College Success, the Institute of Education Sciences, and Attendance Works.
*   **Interactive Web Application**: A user-friendly Gradio UI allows for easy interaction, example scenarios, and a secure access key system for the demo.
*   **Full Transparency**: The "Evidence Base" section in the output shows the exact source documents, page numbers, and content snippets used to generate the recommendation, along with a relevance score for each.

## 3. System Architecture

The project follows a modern RAG architecture designed for quality and scalability.

1.  **Knowledge Base Curation**: A strategic decision was made to manually curate a high-quality `knowledge_base_raw.json` file from the source documents. For this proof-of-concept, this approach ensured maximum quality for the RAG pipeline, bypassing the complexities of programmatic PDF extraction.
2.  **Data Preprocessing**: A `build_knowledge_base.py` script processes the raw JSON. It uses a semantic chunking strategy to group related concepts, creating a final `knowledge_base_final_chunks.json` file.
3.  **Vector Indexing**: During the build process, the pre-processed chunks are encoded into vector embeddings and stored in a `faiss_index.bin` file for efficient similarity search.
4.  **RAG Pipeline (At Runtime)**:
    *   The user enters a student narrative into the Gradio app.
    *   The narrative is converted into a vector embedding.
    *   FAISS performs a similarity search on the vector index to retrieve the most relevant intervention chunks.
    *   The retrieved chunks and the original narrative are formatted into a detailed prompt, tailored to the selected persona (teacher, parent, or principal).
    *   The prompt is sent to the Gemini API, which generates a synthesized recommendation.
    *   The final recommendation and its evidence base are formatted and displayed to the user.

## 4. How to Run Locally

This project uses `uv` for fast and reliable dependency management.

### Prerequisites

1.  **Python >= 3.12**
2.  **`uv` installed**:
    ```bash
    pip install uv
    ```
3.  **Environment Variables**: You must create a `.env` file in the project's root directory. The application loads secrets from this file.
    ```
    # .env
    FOT_GOOGLE_API_KEY="your_google_api_key_here"
    DEMO_PASSWORD="your_local_password" # Sets the password for your local instance of the Gradio app.
    ```

### Setup

Follow this two-step process to ensure hardware-specific dependencies like PyTorch are installed correctly.

1.  **Create the virtual environment:**
    ```bash
    uv venv
    ```
    *Activate the environment:*
    *   macOS/Linux: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`

2.  **Install PyTorch Separately:**
    This command lets `uv` find the correct PyTorch version for your specific hardware (Intel Mac, Apple Silicon, Windows, Linux, etc.).
    ```bash
    uv pip install torch --index-url https://download.pytorch.org/whl/cpu
    ```
    *Note: We explicitly use the CPU-only version of PyTorch, which is perfect for this project and avoids complex CUDA dependencies.*

3.  **Install the Project:**
    Now that the difficult dependency is handled, install the application and its development tools.
    ```bash
    uv pip install -e ".[dev]"
    ```

### Running the Application

After setup, run the Gradio web application using its console script entry point.

```bash
uv run fot-recommender
```

This will launch the interactive Gradio API, which you can access in your browser.

## 5. Development

The project is configured with a suite of standard development tools for maintaining code quality.

*   **Run Tests:**
    ```bash
    uv run pytest
    ```
*   **Format Code:**
    ```bash
    uv run black .
    ```
*   **Lint Code:**
    ```bash
    uv run ruff check .
    ```
*   **Type Checking:**
    ```bash
    uv run mypy src/
    ```

## 6. Project Structure

```
.
├── app.py                  # Gradio UI and web API entry point
├── data/
│   ├── processed/          # Processed data artifacts
│   │   ├── citations.json
│   │   ├── faiss_index.bin
│   │   ├── knowledge_base_final_chunks.json
│   │   └── knowledge_base_raw.json
│   └── source_pdfs/        # Original source documents
├── docs/                     # Project planning documents
├── notebooks/                # Proof-of-concept notebook
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
├── scripts/
│   └── build_knowledge_base.py # Script to build data artifacts
├── src/
│   └── fot_recommender/    # Main Python package
│       ├── __init__.py
│       ├── config.py       # Configuration and environment variables
│       ├── main.py         # Main application logic
│       ├── prompts.py      # Prompts for the generative model
│       ├── rag_pipeline.py # Core RAG logic
│       └── semantic_chunker.py # Logic for chunking source data
└── tests/                    # Unit and integration tests
