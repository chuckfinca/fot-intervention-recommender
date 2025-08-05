# Freshman On-Track Intervention Recommender
## Project Plan & Technical Design (Revision 3)

---

## Problem Understanding

**Core Problem**: Freshman year performance is the strongest predictor of high school graduation, yet educators lack systematic tools to match at-risk 9th graders with evidence-based interventions. Currently, intervention selection relies on educator intuition rather than proven best practices, leading to inconsistent support for struggling students.

**Goal of this PoC**: Build a Retrieval-Augmented Generation (RAG) system that takes a student's on-track indicators (credits, attendance, behavioral flags) and automatically recommends the most relevant, evidence-based intervention strategies from a curated knowledge base of proven FOT practices.

**Value Proposition**: This system transforms scattered research into actionable guidance, enabling educators to quickly identify targeted interventions without requiring deep expertise in educational research. By democratizing access to best practices, we can systematically improve outcomes for at-risk freshmen.

---

## Proposed RAG Architecture

### Technical Stack & Rationale

**Programming Language**: Python
- Industry standard for ML/AI development
- Rich ecosystem of libraries for RAG implementation
- Rapid prototyping capabilities align with "bias for action" principle

**Core Libraries**:
- **LangChain**: Framework for RAG pipeline orchestration and prompt management
- **Sentence Transformers**: High-quality semantic embeddings optimized for educational content
- **FAISS**: Fast, in-memory vector search for PoC (Facebook AI Similarity Search)
- **Simplified Stack**: Focus on `langchain`, `sentence-transformers`, `faiss-cpu`, `torch`, and `transformers` to directly support the core RAG pipeline, removing dependencies for direct PDF processing.

**Vector Embeddings**: `all-MiniLM-L6-v2` model
- Optimized for semantic similarity tasks
- Balanced performance vs. computational efficiency
- Strong performance on educational/instructional text

**Cloud Services** (Production Path):
- **Google Cloud Run**: Serverless, auto-scaling container deployment
- **Pinecone/Weaviate**: Managed vector database for production scale
- **Google Cloud Storage**: Document storage and versioning

### RAG Pipeline Architecture

1.  **Knowledge Base Ingestion**: Load and process a manually curated, high-quality JSON knowledge base (`knowledge_base_raw.json`). This bypasses unreliable PDF parsing to focus on core RAG functionality.
2.  **Chunking Strategy**: Semantic chunking by intervention type and implementation steps.
3.  **Vector Embedding**: Transform text chunks into searchable vector representations.
4.  **Retrieval**: Take the `narrative_summary_for_embedding` from the student profile as the query. Perform semantic search against the vector database to retrieve the top 3 most relevant intervention chunks.
5.  **Synthesis**: Generate educator-friendly recommendations with source citations.

### Alignment with Architectural Principles

- **RAG as Core**: Semantic search ensures recommendations are grounded in evidence-based research.
- **Actionable for Educators**: Output format prioritizes clear, implementable steps over raw research.
- **Startup Scale**: FAISS for PoC, cloud-native services for production scalability.
- **Bias for Action**: Minimal viable architecture focused on core functionality first.

---

## Knowledge Base & Data Processing Strategy

### Selected Best-Practice Documents

The knowledge base is built from the primary source document provided and is complemented by five additional high-quality, evidence-based resources to provide specific, actionable "playbooks" for educators.

**Primary Source Document:**
1.  **Freshman On‑Track Toolkit (2nd Edition)** (Network for College Success, 2017)
    -   ***Primary Focus Area***: **Tool Set C: Developing and Tracking Interventions (Pages 43-68)**, which provides the core framework for intervention planning, tracking, and evaluation.

**Additional Curated Sources:**
2.  **17 Quick Tips for Your Credit Recovery Program** (Edmentum, 2024)
    -   *Focus*: Actionable strategies for designing and implementing effective credit recovery programs at both the district and school levels.
3.  **Handout: Strategies to Address Chronic Absenteeism** (Institute of Education Sciences, REL Southwest, 2025)
    -   *Focus*: Evidence-based interventions for chronic absenteeism, including Early Warning Systems, Mentoring, and Check & Connect.
4.  **High-Quality Tutoring: An Evidence-Based Strategy to Tackle Learning Loss** (Institute of Education Sciences, 2021)
    -   *Focus*: Defines the characteristics of effective, high-impact tutoring to accelerate student learning.
5.  **WWC Intervention Report: Check & Connect** (Institute of Education Sciences, What Works Clearinghouse, 2015)
    -   *Evidence Level*: A detailed report on a key dropout prevention program with positive effects on keeping students in school.
6.  **Early Intervention Strategies: Using Teams to Monitor and Identify Students in Need of Support** (Attendance Works, 2019)
    -   *Focus*: A multi-tiered team-based approach to monitoring attendance data and implementing early interventions.

### Data Processing Strategy

~~**Content Extraction** (Hybrid Strategy):~~
- ~~**Tier 1**: PyMuPDF (fitz) for rapid extraction of simple, single-column text pages~~
- ~~**Tier 2**: pdfplumber for structured tabular data to preserve relational integrity~~
- ~~**Tier 3**: Nougat (Meta AI) layout-aware model for complex multi-column layouts and flowcharts~~
- ~~**Quality Assurance**: Manual review and validation of extracted content accuracy~~

**Pivoted Content Extraction Strategy:**
- **Manual Curation**: Bypassed programmatic PDF extraction due to complexity and unreliability. Instead, key interventions were manually extracted (with LLM assistance) from all source documents into a single, high-quality `knowledge_base_raw.json` file. This ensures maximum quality and allows direct focus on the RAG pipeline.

**Chunking Approach**:
- **Semantic Chunking**: Break documents by intervention type, not arbitrary word limits.
- **Chunk Size**: 300-500 words to maintain context while enabling precise retrieval.
- **Overlap Strategy**: 50-word overlap to preserve cross-boundary context.
- **Metadata Tagging**: Source document, intervention category, target indicators.

**Content Preparation**:
- Standardize intervention descriptions with consistent format.
- Extract key implementation steps and required resources.
- Tag interventions by target risk factors (attendance, credits, behavior).
- Create intervention summaries optimized for educator consumption.

---

## AI as a Co-pilot Strategy

### Development Acceleration

**GitHub Copilot**:
- Code generation for standard RAG pipeline components.
- Boilerplate reduction for data processing and API endpoints.
- Test case generation for validation scenarios.

**Large Language Models (GPT-4/Claude)**:
- **Knowledge Base Curation**: Accelerated the manual extraction process by summarizing dense academic PDFs and structuring the content into the clean `knowledge_base_raw.json` format.
- **Prompt Engineering**: Optimize prompts for educator-specific output formatting.
- **Content Synthesis**: Transform academic language into practitioner-friendly recommendations.
- **Code Review**: Architecture validation and optimization suggestions.

### Problem-Solving Workflow

1.  **Research Phase**: Use LLMs to quickly synthesize intervention research and identify gaps.
2.  **Architecture Design**: Validate technical approach against startup scaling requirements.
3.  **Implementation**: Leverage Copilot for rapid prototype development.
4.  **Testing**: AI-assisted generation of diverse student profile test cases.
5.  **Optimization**: LLM-powered analysis of retrieval quality and recommendation relevance.

### Quality Assurance

- **Prompt Validation**: Use AI to generate edge cases for robust testing.
- **Content Review**: AI-assisted verification that academic content translates to actionable guidance.
- **Bias Detection**: Systematic review of recommendations for potential equity issues.

---

## Success Metrics & Next Steps

**PoC Success Criteria**:
- Accurate retrieval of top 3 relevant interventions for sample student profile.
- Educator-friendly output format with clear implementation guidance.
- Sub-2 second response time for typical queries.
- Proper source citation for all recommendations.

**Production Evolution Path**:
1.  **Enhanced Knowledge Base**: Scale to 50+ intervention documents.
2.  **Persona-Based Outputs**: Tailored recommendations for teachers, parents, principals.
3.  **API Microservice**: RESTful service for integration with SIS platforms.
4.  **Analytics Dashboard**: Track intervention effectiveness and usage patterns.

This PoC establishes the foundation for a scalable, evidence-based intervention recommendation system that can transform how educators support at-risk freshmen nationwide.