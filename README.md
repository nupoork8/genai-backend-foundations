# 🚀 Generative AI Backend Foundations

A hands-on 7-day engineering sprint focused on building a production-style Retrieval-Augmented Generation (RAG) backend from scratch using Python.

Instead of relying on black-box abstractions, this repository documents the step-by-step evolution of:

* API request handling
* Document chunking strategies
* Vector database integration
* Semantic search pipelines
* Defensive backend validation
* LLM orchestration layers

The goal was simple: understand the real backend plumbing behind modern AI systems.

---

# 🏗️ Project Architecture

```text
[ Client Request ]
        │
        ▼
┌──────────────────────────────┐
│ FastAPI + Pydantic Layer     │
│ Request validation & routing │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Text Splitting Pipeline      │
│ Recursive chunk generation   │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ ChromaDB Vector Store        │
│ Semantic similarity search   │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Gemini LLM Gateway           │
│ Context-aware generation     │
└──────────────────────────────┘
        │
        ▼
[ Structured JSON Response ]
```

---

# 📁 Repository Structure

## Day 1 — Payload Parsing

`day_01_payload_parsing.py`

* JSON parsing fundamentals
* Dictionary traversal
* API response extraction
* Data structure handling

---

## Day 2 — Text Splitting

`day_02_text_splitting.py`

* Recursive character chunking
* Chunk overlap mechanics
* Context preservation strategies
* Token-aware ingestion logic

---

## Day 3 — Vector Storage

`day_03_vector_storage.py`

* ChromaDB integration
* Embedding-based indexing
* Semantic similarity search
* Local vector database setup

---

## Day 4 — FastAPI Server

`day_04_fastapi_server.py`

* FastAPI backend setup
* Asynchronous routing
* Swagger/OpenAPI documentation
* JSON API responses

---

## Day 5 — API Integration

`day_05_api_integration.py`

* External LLM connectivity
* Prompt formatting pipelines
* Dynamic request orchestration
* API gateway architecture

---

## Day 6 — Defensive Backend Engineering

`day_06_defensive_api.py`

* Pydantic validation models
* Input sanitization
* Structured error handling
* Protection against malformed payloads

---

## Day 7 — Final RAG Pipeline

`day_07_8_final_rag.py`

* End-to-end RAG orchestration
* Semantic retrieval workflow
* Context injection into LLM prompts
* Production-style response generation

---

# ⚙️ Tech Stack

* Python
* FastAPI
* Pydantic
* ChromaDB
* LangChain
* Gemini API
* Uvicorn

---

# 🛠️ Installation

## 1. Clone the Repository

```bash
git clone <your-repo-link>
cd genai-backend-foundations
```

## 2. Install Dependencies

```bash
pip install fastapi uvicorn pydantic langchain-text-splitters langchain-chroma langchain-core langchain-google-genai
```

---

# 🔐 Environment Variables

## Windows (CMD)

```bash
set GEMINI_API_KEY=your_api_key_here
```

## Mac/Linux

```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

# ▶️ Running the Final Pipeline

```bash
uvicorn day_07_8_final_rag:app --port 8080
```

---

# 📊 API Testing

Once the server is running, open:

```text
http://127.0.0.1:8080/docs
```

FastAPI automatically generates an interactive Swagger UI for endpoint testing.

---

# 🧪 Example Request

```json
{
  "question": "What tools are mentioned for backend GenAI endpoints?"
}
```

# ✅ Example Response

```json
{
  "success": true,
  "engine": "RAG-Pipeline-v1",
  "user_question": "What tools are mentioned for backend GenAI endpoints?",
  "retrieved_context": "web endpoints, while ChromaDB serves as the core vector store for handling semantic search operations.",
  "llm_generated_answer": "Based on the provided context, ChromaDB is mentioned as the core vector store used for semantic search operations."
}
```

---

# 🧠 Key Engineering Learnings

### Semantic Search > Keyword Matching

The system retrieves context using vector similarity instead of exact text matches.

### Defensive APIs Matter

Strict schema validation prevents malformed requests from reaching downstream systems.

### RAG = Data Plumbing

Modern AI systems rely heavily on:

* retrieval pipelines
* vector databases
* prompt orchestration
* backend infrastructure

—not just prompting.

---

# 🛡️ Real-World Problems Solved

### API Deprecation Handling

Managed upstream provider model/version migration issues safely.

### Windows Port Conflicts

Resolved `WinError 10048` socket conflicts during local server deployment.

### Secret Management

Removed exposed API keys using Git history rewriting and environment variables.

---

# 🚀 Future Improvements

* Streaming responses
* Authentication layer
* Docker deployment
* Cloud vector database integration
* Async background ingestion jobs
* Multi-model provider routing

---

# 📌 Note

This project was built to deeply understand how GenAI backend systems actually work under the hood from raw text ingestion to live LLM response generation.

