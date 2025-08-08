# FOT Intervention Recommender
## Final Implementation Plan (Annotated)

---

## Overview

This implementation plan documents the executable phases, tasks, and deliverables used to build the working proof-of-concept for the Freshman On-Track Intervention Recommender. This plan was updated from its original version to reflect the final, successful implementation path.

**Primary Deliverable**: A working RAG system, deployed as an interactive web application, that provides evidence-based intervention recommendations.

---

## Phase 0: Environment Setup & Resource Gathering
**Goal**: Establish a lean development environment and prepare all source materials.

### Tasks

#### 0.1 Development Environment Setup
- [✅] Create local project structure (`pyproject.toml`, `src/`, `tests/`).
- [✅] Configure a modern, fast dependency manager (`uv`).
- [✅] Install core libraries: `torch`, `sentence-transformers`, `faiss-cpu`, `google-generativeai`, `gradio`.
- [✅] Create a `.env` file for secure management of API keys.

#### 0.2 Source Material Collection
- [✅] Identify and download the primary source document (NCS FOT Toolkit) and five additional high-quality, evidence-based articles.
- [✅] Manually extract and structure all relevant interventions from these sources into a clean, high-quality `knowledge_base_raw.json` file.
- [✅] Create a `citations.json` file to store metadata for all source documents.

### Success Criteria
- ✅ Local development environment running with all simplified dependencies.
- ✅ `knowledge_base_raw.json` and `citations.json` files are created, validated, and located in `data/processed/`.

---

## Phase 1: Knowledge Base Construction
**Goal**: Load and semantically chunk the curated knowledge base to prepare it for embedding.

> **_Strategic Pivot: From Programmatic Extraction to Curated Knowledge Base_**
>
> *   **Initial Approach:** My original plan detailed a complex pipeline to programmatically extract text and tables from source PDFs using tools like PyMuPDF and pdfplumber.
> *   **Challenge & Insight:** I quickly identified this approach as a significant project risk. The complexity and unreliability of PDF parsing could easily consume the majority of development time, detracting from the core task: building a high-quality RAG system. The ultimate goal is to provide relevant recommendations, which depends entirely on the *quality* and *cleanliness* of the knowledge base, not the sophistication of the extraction method.
> *   **Decision & Rationale:** In line with the "Bias for Action" and "Startup Urgency" principles, I made a strategic decision to pivot. I manually curated a high-quality `knowledge_base_raw.json` file, a process accelerated by using an LLM as a co-pilot. This action de-risked the project, guaranteed the highest possible quality for the RAG pipeline's input, and allowed me to focus my efforts on the more critical tasks of semantic chunking, embedding, and retrieval logic.
> *   **Result:** This pivot resulted in a more robust and effective PoC. The final system is built on a foundation of clean, reliable data, directly leading to more relevant and trustworthy recommendations.

### Tasks

#### 1.1 Content Loading
- [✅] Implement logic in `scripts/build_knowledge_base.py` to load the `knowledge_base_raw.json` file.

#### 1.2 Content Processing & Chunking
- [✅] Create a `src/fot_recommender/semantic_chunker.py` module to group related items from the raw JSON file.
- [✅] Implement a `chunk_by_concept` strategy that combines page-based items into larger, topic-based chunks.

#### 1.3 Knowledge Base Structuring
- [✅] Define a final chunk structure, ensuring the output is a clean list of dictionaries, each containing `title`, `source_document`, `fot_pages`, and a combined `content_for_embedding` string.
- [✅] Save the processed data as `knowledge_base_final_chunks.json`.

### Success Criteria
- ✅ `knowledge_base_raw.json` successfully loaded into the build script.
- ✅ Semantic chunking logic correctly combines related pages into fewer, more coherent chunks.
- ✅ A final `knowledge_base_final_chunks.json` file is produced and validated for quality.

---

## Phase 2: RAG Pipeline Implementation
**Goal**: Build and test the core Retrieval-Augmented Generation functionality.

### Tasks

#### 2.1 Vector Embedding Setup
- [✅] **Initialize embedding model**: In `rag_pipeline.py`, initialize `all-MiniLM-L6-v2` using the `sentence-transformers` library.
- [✅] **Create embeddings**: Implement a function to create embeddings from the `content_for_embedding` field of each chunk.
- [✅] **Set up FAISS vector database**: Implement `create_vector_db` to build an `IndexFlatIP` index from the embeddings and save it to `faiss_index.bin`.

#### 2.2 Retrieval System
- [✅] **Implement semantic search**: Create a `search_interventions` function that takes a query, embeds it, and uses the FAISS index to retrieve the top-k most relevant chunks.
- [✅] **Test retrieval**: Validate that sample queries return relevant and high-scoring results.

#### 2.3 Response Generation
- [✅] **Implement Generative Model**: Use the `google-generativeai` library to call the Gemini API.
- [✅] **Create persona-based prompts**: In `prompts.py`, create distinct, detailed prompts for 'teacher', 'parent', and 'principal' personas.
- [✅] **Synthesize response**: Create a `generate_recommendation_summary` function that formats the retrieved chunks and user query into the selected persona's prompt and sends it to the Gemini API.

### Success Criteria
- ✅ Vector database successfully created with all intervention embeddings.
- ✅ Semantic search returns relevant results for test queries.
- ✅ Response generation successfully synthesizes retrieved chunks into a coherent, persona-specific recommendation.

---

## Phase 3: System Integration & Application Deployment
**Goal**: Build a user-facing application, create a full test suite, and deploy the system.

### Tasks
- [✅] **Create an Interactive Web Application**: In `app.py`, build an interactive UI using Gradio.
- [✅] **Integrate RAG Pipeline**: Connect the UI components to the full RAG pipeline (embedding, search, generation).
- [✅] **Add Examples and UI Polish**: Include example scenarios and helper functions to improve user experience.
- [✅] **Implement Access Key**: Add a simple password field to protect the demo.
- [✅] **Deploy to Hugging Face Spaces**: Configure the repository for deployment and launch the live application.
- [✅] **Create a Full Test Suite**: In the `tests/` directory, write unit tests using `pytest` for key logic, including semantic chunking and RAG pipeline functions.

### Success Criteria
- ✅ End-to-end pipeline is fully functional within the Gradio application.
- ✅ Application successfully deployed and accessible via a public URL.
- ✅ Core logic is validated with passing unit tests, ensuring system resilience.

---

## Phase 4: Documentation & Presentation
**Goal**: Create clear, comprehensive documentation for the project.

### Tasks
- [✅] **Write a comprehensive `README.md`**:
    - Include project goals, features, and system architecture.
    - Provide clear, step-by-step instructions for local setup and execution.
    - Add a link to the live deployed application.
- [✅] **Document code**: Add docstrings and inline comments to all major functions and modules.
- [✅] **Prepare for presentation**: Create a logical flow for a 5-minute video demonstration, walking through the project's "why," the PoC notebook, and the final live application.

### Success Criteria
- ✅ `README.md` is professional, clear, and comprehensive.
- ✅ Code is well-documented and easy to understand.
- ✅ A clear plan for the final presentation is established.