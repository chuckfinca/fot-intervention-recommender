# Freshman On-Track Intervention Recommender
## Project Plan & Technical Design (Final)

---

## 1. Problem Understanding

**Core Problem**: Freshman year performance is the strongest predictor of high school graduation, yet educators lack systematic tools to match at-risk 9th graders with evidence-based interventions. Currently, intervention selection often relies on educator intuition rather than proven best practices, leading to inconsistent support for struggling students.

**Goal of this PoC**: Build a Retrieval-Augmented Generation (RAG) system that takes a simple narrative about a student's challenges and automatically recommends the most relevant, evidence-based intervention strategies from a curated knowledge base of proven FOT practices.

**Value Proposition**: This system transforms scattered educational research into actionable guidance, enabling educators to quickly identify targeted interventions. By democratizing access to best practices, we can systematically improve outcomes for at-risk freshmen.

---

## 2. Proposed RAG Architecture

### Technical Stack & Rationale

The final technical stack was chosen to prioritize development speed, robustness, and alignment with modern AI engineering practices.

**Programming Language**: Python 3.12
- *Rationale*: Industry standard for AI/ML, rich library ecosystem, and rapid prototyping capabilities.

**Core Libraries**:
- **Sentence Transformers & FAISS**: For high-quality semantic search. `all-MiniLM-L6-v2` offers an excellent balance of performance and efficiency. FAISS provides a fast, in-memory vector store ideal for a PoC.
- **Google Generative AI**: To leverage the powerful `gemini-1.5-flash` model for the "Generation" step, synthesizing evidence into actionable, persona-based advice.
- **Gradio**: To rapidly build and deploy a user-friendly, interactive web application for the demo.
- **uv**: A modern, high-speed project and environment manager used to ensure fast, reliable dependency installation and management.

> **_Stack Evolution_**
> My initial plan considered using `LangChain` for pipeline orchestration. However, for a focused PoC, implementing the RAG logic directly provided greater control, transparency into the prompts, and avoided an additional dependency. The successful pivot away from programmatic PDF extraction also eliminated the need for data manipulation libraries like `Pandas`, resulting in a leaner and more focused final stack.

### Deployment & Production Path

- **PoC Deployment**: The application was successfully deployed to **Hugging Face Spaces**.
    - *Rationale*: This platform is ideal for hosting interactive Gradio applications, providing a public URL for live demonstrations and stakeholder feedback without complex infrastructure setup.

- **Production Path**:
    - The core logic would be packaged into a formal **REST API microservice** using a framework like FastAPI and containerized with Docker.
    - This API would be deployed on a scalable, serverless platform like **Google Cloud Run** or **AWS Lambda** for cost-effective, high-availability serving.
    - The FAISS index would be replaced by a managed vector database like **Pinecone** or **Weaviate** to handle a larger knowledge base and higher query volumes.

### RAG Pipeline Architecture

1.  **Knowledge Base Curation**: A high-quality JSON file (`knowledge_base_raw.json`) was manually curated from source documents to ensure maximum data quality.
2.  **Chunking & Indexing (Build Time)**: A build script processes the raw JSON, performs semantic chunking by concept, and creates a FAISS vector index (`faiss_index.bin`).
3.  **Retrieval (Runtime)**: A user's narrative is embedded and used to perform a semantic search against the FAISS index, retrieving the most relevant intervention chunks.
4.  **Synthesis (Runtime)**: The retrieved chunks and the original query are formatted into a persona-specific prompt and sent to the Gemini API.
5.  **Output**: The API generates a synthesized, actionable recommendation tailored to a teacher, parent, or principal.

---

## 3. Knowledge Base & Data Processing Strategy

### Selected Best-Practice Documents
The knowledge base was built from the primary source and five additional high-quality, evidence-based resources:

1.  **Freshman On‑Track Toolkit (2nd Edition)** (Network for College Success, 2017)
2.  **17 Quick Tips for Your Credit Recovery Program** (Edmentum, 2024)
3.  **Handout: Strategies to Address Chronic Absenteeism** (IES, REL Southwest, 2025)
4.  **High-Quality Tutoring: An Evidence-Based Strategy...** (IES, 2021)
5.  **WWC Intervention Report: Check & Connect** (IES, What Works Clearinghouse, 2015)
6.  **Early Intervention Strategies...** (Attendance Works, 2019)

### Data Processing Strategy

> **_Strategic Pivot Summary_**
> My initial plan involved complex programmatic PDF extraction. I pivoted to a manually curated `knowledge_base_raw.json` file, a decision driven by the "Bias for Action" principle. This approach guaranteed high-quality data, de-risked the project, and allowed me to focus on building a more effective core RAG pipeline.

**Final Processing Approach**:
- **Manual Curation**: Key interventions were manually extracted from all source documents into a single, high-quality `knowledge_base_raw.json`.
- **Semantic Chunking**: A script groups the raw data by `concept` (e.g., "Intervention: Mentoring") to create meaningful, coherent chunks for embedding. This is more effective than chunking by arbitrary word counts.
- **Content Preparation**: The title is prepended to the content for each chunk (`"Title: {concept}. Content: {content}"`) to improve the contextual richness of the embeddings.

---

## 4. AI as a Co-pilot: A Human-Directed Workflow

My approach to AI collaboration treats large language models as strategic partners, with the human acting as the director and critical thinker. This involves a structured, iterative dialogue rather than simple prompting.

### Strategic Planning & Ideation
The project and implementation plans were developed through an iterative, multi-model process.
- **Initial Drafting:** I engaged both Gemini Pro and Claude Sonnet to generate independent approaches for structuring the project and tackling the core tasks.
- **Iterative Refinement:** I then orchestrated a dialogue between the models, using prompts like *"What do you think of this take?"* to have each model critique the other's feedback. This iterative loop allowed me to synthesize their strengths and converge on a robust, detailed plan.

### Core Technique: Active Context Management
Throughout the collaboration, I carefully managed the conversational context to ensure high-quality, relevant outputs.
- **Preventing Confusion:** I actively curated the chat history to avoid "muddying the results." If multiple versions of code or text were present, I would remove obsolete versions from the context window to prevent the model from referring to the wrong information.
- **Tool-Specific Workflows:** I leveraged the unique features of different browser-based interfaces. **Claude.ai's** "Artifacts" feature was invaluable for creating and editing planning documents. **Google's AI Studio** offered a significant advantage with its ability to fork conversations and delete individual messages from the context window, enabling precise context control.

### Foundational Best Practices
This AI-driven workflow is built on a foundation of solid engineering hygiene. The project was initiated from a pre-configured template with standard tooling (`ruff`, `uv`, `.gitignore`), ensuring a clean and maintainable codebase from the start.

This creates a **virtuous cycle of code quality**. By starting with and consistently adding well-structured code, that uses best practices, the context window provided to the AI is enriched with high-quality exemplars. The model's in-context learning capabilities mean it, in turn, generates new code that adheres to these established patterns, further elevating the quality baseline. This compounding effect is a deliberate strategy to maintain a high standard of maintainability and robustness throughout the development lifecycle.

---

## 5. Success Metrics & Production Path

**PoC Success Criteria (Achieved)**:
- ✅ Accurate retrieval of the most relevant interventions for sample student narratives.
- ✅ Persona-based output is clear, actionable, and tailored to the audience.
- ✅ Sub-second response time for the entire RAG pipeline.
- ✅ All recommendations are grounded in evidence, with source documents and relevance scores displayed.
- ✅ Project is fully documented, tested, and deployed as a live, interactive web application.

**Production Evolution Path**:
1.  **Enhanced Knowledge Base**: Scale the knowledge base to include a wider range of interventions.
2.  **Formal REST API**: Package the final logic into a production-ready REST API (e.g., using FastAPI and Docker) for robust integration with School Information Systems (SIS).
3.  **Feedback Loop & Analytics**: Add a mechanism for educators to rate the usefulness of recommendations and build an analytics dashboard to track intervention effectiveness.
