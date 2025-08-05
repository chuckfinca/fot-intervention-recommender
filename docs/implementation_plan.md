# FOT Intervention Recommender
## Detailed Implementation Plan (Revision 2)

---

## Overview

This implementation plan transforms the strategic project plan into executable phases, with specific tasks, deliverables, and success criteria for building the working proof-of-concept.

***Note on Strategic Pivot:*** *We have shifted from programmatic PDF extraction to using a manually curated, high-quality JSON knowledge base (`knowledge_base_raw.json`). This decision was made to bypass the complexities and unreliability of PDF parsing and to focus directly on the core RAG pipeline development.*

**Primary Deliverable**: A working RAG system application that provides intervention recommendations.

---

## Phase 0: Environment Setup & Resource Gathering
**Goal**: Establish a lean development environment and use the pre-processed source materials.

### Tasks

#### 0.1 Development Environment Setup
- [✅] Create local project structure.
- [✅] ~~Install required libraries in first cell:~~
  ```python
  ~~!pip install sentence-transformers faiss-cpu langchain pandas pymupdf pdfplumber transformers~~
  ```
- [✅] **Install simplified libraries:**
  ```bash
  uv pip install langchain sentence-transformers faiss-cpu transformers torch
  ```
- [✅] Import necessary libraries and test basic functionality.

#### 0.2 Source Material Collection
- [✅] ~~**Extract FOT Toolkit pages 43-68**~~
- [✅] ~~**Download 5 external sources**~~
- [✅] **Prepare `knowledge_base_raw.json`**: Manually (or with LLM assistance) extract and structure all relevant interventions from the FOT Toolkit into a clean JSON file. This file becomes our single source of truth.

#### 0.3 Quick Content Reconnaissance
- [✅] ~~Scan each document to identify complexity~~
- [✅] ~~Create a "document complexity map" for processing strategy~~

### Success Criteria
- ✅ Local development environment running with all simplified dependencies.
- ✅ `knowledge_base_raw.json` file is created, validated, and located in `data/processed/`.
- ✅ ~~Basic understanding of each document's structure and complexity~~

---

## Phase 1: Knowledge Base Construction
**Goal**: ~~Extract, process, and structure content~~ **Load and semantically chunk the pre-processed knowledge base.**

### Tasks

#### 1.1 Content Extraction (Hybrid Approach)
- [✅] ~~**Implement PyMuPDF extraction**~~
- [✅] ~~**Implement pdfplumber for tables**~~
- [✅] ~~**Manual extraction for complex pages**~~
- [✅] **Load Pre-processed Knowledge Base**: Implement logic in `main.py` to load the `knowledge_base_raw.json` file.

#### 1.2 Content Processing & Standardization
- [ ] ~~**Create intervention extraction function**~~
- [ ] ~~**Process each document**~~
- [ ] **Implement Semantic Chunker**: Create a `semantic_chunker.py` module that combines related page-based items from the raw JSON into larger, topic-based chunks (e.g., group all pages about "Intervention Evaluation Flowchart" into one chunk).

#### 1.3 Knowledge Base Structuring
- [ ] ~~**Create standardized intervention format**~~
- [ ] ~~**Implement semantic chunking**~~
- [ ] **Define Final Chunk Structure**: Ensure the output of the semantic chunker is a clean list of dictionaries, each containing `title`, `fot_pages`, and a combined `content` string.

### Success Criteria
- ✅ `knowledge_base_raw.json` successfully loaded into the application.
- ✅ Semantic chunking logic correctly combines related pages into fewer, more coherent chunks.
- ✅ A final `knowledge_base_final_chunks.json` file is produced and validated for quality.

---

## Phase 2: RAG Pipeline Implementation
**Goal**: Build and test the core RAG functionality.

### Tasks

#### 2.1 Vector Embedding Setup
- [ ] **Initialize embedding model**:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

- [ ] **Create embeddings for knowledge base**:
```python
def create_embeddings(intervention_chunks):
    embeddings = model.encode(intervention_chunks)
    return embeddings
```

- [ ] **Set up FAISS vector database**:
```python
import faiss
def create_vector_db(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index
```

#### 2.2 Retrieval System
- [ ] **Implement semantic search**:
```python
def search_interventions(query, index, intervention_data, k=3):
    query_embedding = model.encode([query])
    scores, indices = index.search(query_embedding, k)
    return [(intervention_data[i], scores[0][idx]) for idx, i in enumerate(indices[0])]
```

- [ ] **Test retrieval with sample queries**:
  - "Student failing core classes and missing school"
  - "Attendance problems and behavioral issues"
  - "Low credits earned, needs academic support"

#### 2.3 Response Generation
- [ ] **Create educator-friendly formatter**:
```python
def format_recommendations(retrieved_interventions, student_profile):
    formatted_response = []
    for intervention, score in retrieved_interventions:
        recommendation = {
            "intervention_name": intervention["name"],
            "rationale": f"Recommended because: {explain_match(intervention, student_profile)}",
            "implementation_steps": intervention["implementation_steps"],
            "source": intervention["source_document"],
            "confidence_score": score
        }
        formatted_response.append(recommendation)
    return formatted_response
```

### Success Criteria
- ✅ Vector database successfully created with all intervention embeddings
- ✅ Semantic search returns relevant results for test queries
- ✅ Response format is educator-friendly with clear implementation guidance
- ✅ Source citations are properly maintained throughout pipeline

---

## Phase 3: System Integration & Testing
**Goal**: End-to-end testing with provided student profile

### Tasks

#### 3.1 End-to-End Pipeline Integration
- [ ] **Create main recommendation function**:
```python
def get_fot_recommendations(student_profile_narrative):
    # 1. Process student narrative
    # 2. Perform semantic search  
    # 3. Retrieve top 3 interventions
    # 4. Format for educators
    # 5. Return structured recommendations
    pass
```

#### 3.2 Testing with Sample Student Profile
- [ ] **Test with provided profile**:
```python
sample_student = """This student is struggling to keep up with coursework, 
having failed one core class and earning only 2.5 credits out of 4 credits 
expected for the semester. Attendance is becoming a concern at 88% for an 
average annual target of 90%, and they have had one behavioral incident. 
The student needs targeted academic and attendance support to get back on 
track for graduation."""

recommendations = get_fot_recommendations(sample_student)
```

#### 3.3 Quality Validation & Refinement
- [ ] **Evaluate recommendation quality**:
  - Do recommendations address student's specific risk factors?
  - Are implementation steps clear and actionable?
  - Are source citations accurate and helpful?

- [ ] **Refine retrieval if needed**:
  - Adjust embedding model parameters
  - Modify chunking strategy if results are poor
  - Fine-tune response formatting

### Success Criteria
- ✅ End-to-end pipeline processes student profile successfully
- ✅ Returns exactly 3 relevant intervention recommendations
- ✅ Each recommendation includes implementation steps and source citation
- ✅ Recommendations directly address student's risk factors (credits, attendance, behavior)

---

## Phase 4: Documentation & Presentation Preparation
**Goal**: Create clear notebook documentation and prepare for video presentation

### Tasks

#### 4.1 Colab Notebook Documentation
- [ ] **Add comprehensive markdown cells**:
  - Project overview and goals
  - Knowledge base composition and rationale
  - Technical architecture explanation
  - Step-by-step process documentation

- [ ] **Code documentation**:
  - Add docstrings to all functions
  - Include inline comments for complex logic
  - Add example usage for key functions

#### 4.2 Demonstration Preparation
- [ ] **Create demonstration workflow**:
  - Show knowledge base construction process
  - Demonstrate search functionality with different queries
  - Walk through the sample student profile analysis
  - Display formatted recommendations

- [ ] **Prepare talking points for video**:
  - Project value proposition (30 seconds)
  - Technical approach overview (60 seconds)
  - Live demonstration (2 minutes)
  - Next steps and product vision (90 seconds)

### Success Criteria
- ✅ Notebook is well-documented with clear explanations
- ✅ All code cells execute successfully from top to bottom
- ✅ Demonstration workflow is smooth and highlights key features
- ✅ Ready for 5-minute video recording

---

## Phase 5: Bonus Features (Optional)
**Goal**: Implement advanced features to differentiate the solution

### Option A: API Microservice (Bonus 1)
- [ ] **Create FastAPI application**:
```python
from fastapi import FastAPI
app = FastAPI(title="FOT Intervention Recommender")

@app.post("/recommend")
async def get_recommendations(student_narrative: str):
    return get_fot_recommendations(student_narrative)
```

- [ ] **Containerize with Docker**
- [ ] **Create deployment documentation**

### Option B: Persona-Based Recommendations (Bonus 2)
- [ ] **Implement persona-specific prompts**:
```python
def generate_persona_recommendations(interventions, persona):
    # Teacher: Classroom-focused, actionable steps
    # Parent: Supportive language, home-based strategies  
    # Principal: Resource requirements, systemic approach
    pass
```

### Success Criteria (if attempted)
- ✅ Bonus feature fully functional and demonstrated
- ✅ Added value is clear and well-articulated
- ✅ Implementation quality matches core system standards

---

## Risk Mitigation Strategies

### Technical Risks
- **~~Complex PDF extraction fails~~**: **(RESOLVED)** This risk has been completely eliminated by pivoting to a manually curated JSON file.
- **Poor embedding quality**: Test alternative models (e.g., `all-mpnet-base-v2`).
- **Retrieval returns irrelevant results**: Adjust chunking strategy or add filtering.
- **New Risk - Poor Manual Extraction**: The quality of the RAG system now depends entirely on the quality of the `knowledge_base_raw.json`. Mitigation: Manually review and edit the JSON for clarity, accuracy, and completeness.

### Time Management Risks
- **~~Document processing takes too long~~**: **(RESOLVED)** This risk is eliminated.
- **Perfectionism trap**: Focus on working MVP first, refinements second.
- **Scope creep**: Stick to core deliverables, save enhancements for bonus phase.

---
