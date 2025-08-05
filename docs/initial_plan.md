# Freshman On-Track Intervention Recommender
## Project Plan & Technical Design

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
- **Pandas**: Data processing and manipulation for knowledge base preparation

**Vector Embeddings**: `all-MiniLM-L6-v2` model
- Optimized for semantic similarity tasks
- Balanced performance vs. computational efficiency
- Strong performance on educational/instructional text

**Cloud Services** (Production Path):
- **Google Cloud Run**: Serverless, auto-scaling container deployment
- **Pinecone/Weaviate**: Managed vector database for production scale
- **Google Cloud Storage**: Document storage and versioning

### RAG Pipeline Architecture

1. **Knowledge Base Ingestion**: Extract and preprocess intervention documents
2. **Chunking Strategy**: Semantic chunking by intervention type and implementation steps
3. **Vector Embedding**: Transform text chunks into searchable vector representations
4. **Retrieval**: Take the narrative_summary_for_embedding from the student profile as the query. Perform semantic search against the vector database to retrieve the top 3 most relevant intervention chunks
5. **Synthesis**: Generate educator-friendly recommendations with source citations

### Alignment with Architectural Principles

- **RAG as Core**: Semantic search ensures recommendations are grounded in evidence-based research
- **Actionable for Educators**: Output format prioritizes clear, implementable steps over raw research
- **Startup Scale**: FAISS for PoC, cloud-native services for production scalability
- **Bias for Action**: Minimal viable architecture focused on core functionality first

---

## Knowledge Base & Data Processing Strategy

### Selected Best-Practice Documents

1. **FOT Toolkit - Tool Set C: Developing and Tracking Interventions** (Pages 43-68)
   - *Primary Source*: Comprehensive intervention framework
   - *Focus*: Systematic approach to intervention selection and tracking

2. **Check & Connect Intervention** (University of Minnesota/WWC)
   - *Evidence Level*: Only dropout prevention program with WWC "Positive Effects" rating
   - *Focus*: Structured mentoring for attendance and credit recovery

3. **Predictive Power of Ninth-Grade GPA** (University of Chicago Consortium)
   - *Strategic Value*: Research foundation explaining why FOT interventions matter
   - *Focus*: Data-driven rationale for early intervention

4. **Preventing Chronic Absence and Promoting Attendance** (REL Program)
   - *Evidence Base*: Tiered, research-validated attendance strategies
   - *Focus*: Family engagement, transportation, and systemic barriers

5. **Addressing Root Causes of Disparities in School Discipline** (NCSSLE)
   - *Methodology*: Systematic root-cause analysis for behavioral interventions
   - *Focus*: Data-driven behavioral support strategies

### Data Processing Strategy

**Content Extraction** (Hybrid Strategy):
- **Tier 1**: PyMuPDF (fitz) for rapid extraction of simple, single-column text pages
- **Tier 2**: pdfplumber for structured tabular data to preserve relational integrity
- **Tier 3**: Nougat (Meta AI) layout-aware model for complex multi-column layouts and flowcharts
- **Quality Assurance**: Manual review and validation of extracted content accuracy

**Chunking Approach**:
- **Semantic Chunking**: Break documents by intervention type, not arbitrary word limits
- **Chunk Size**: 300-500 words to maintain context while enabling precise retrieval
- **Overlap Strategy**: 50-word overlap to preserve cross-boundary context
- **Metadata Tagging**: Source document, intervention category, target indicators

**Content Preparation**:
- Standardize intervention descriptions with consistent format
- Extract key implementation steps and required resources
- Tag interventions by target risk factors (attendance, credits, behavior)
- Create intervention summaries optimized for educator consumption

---

## AI as a Co-pilot Strategy

### Development Acceleration

**GitHub Copilot**: 
- Code generation for standard RAG pipeline components
- Boilerplate reduction for data processing and API endpoints
- Test case generation for validation scenarios

**Large Language Models (GPT-4/Claude)**:
- **Document Analysis**: Rapid extraction of key intervention strategies from research papers
- **Prompt Engineering**: Optimize prompts for educator-specific output formatting
- **Content Synthesis**: Transform academic language into practitioner-friendly recommendations
- **Code Review**: Architecture validation and optimization suggestions

### Problem-Solving Workflow

1. **Research Phase**: Use LLMs to quickly synthesize intervention research and identify gaps
2. **Architecture Design**: Validate technical approach against startup scaling requirements
3. **Implementation**: Leverage Copilot for rapid prototype development
4. **Testing**: AI-assisted generation of diverse student profile test cases
5. **Optimization**: LLM-powered analysis of retrieval quality and recommendation relevance

### Quality Assurance

- **Prompt Validation**: Use AI to generate edge cases for robust testing
- **Content Review**: AI-assisted verification that academic content translates to actionable guidance
- **Bias Detection**: Systematic review of recommendations for potential equity issues

---

## Success Metrics & Next Steps

**PoC Success Criteria**:
- Accurate retrieval of top 3 relevant interventions for sample student profile
- Educator-friendly output format with clear implementation guidance
- Sub-2 second response time for typical queries
- Proper source citation for all recommendations

**Production Evolution Path**:
1. **Enhanced Knowledge Base**: Scale to 50+ intervention documents
2. **Persona-Based Outputs**: Tailored recommendations for teachers, parents, principals
3. **API Microservice**: RESTful service for integration with SIS platforms
4. **Analytics Dashboard**: Track intervention effectiveness and usage patterns

This PoC establishes the foundation for a scalable, evidence-based intervention recommendation system that can transform how educators support at-risk freshmen nationwide.