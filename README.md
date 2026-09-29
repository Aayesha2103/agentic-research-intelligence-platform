# 🤖 Agentic Research Intelligence Platform

> **An evidence-aware AI research system that transforms complex
> research questions into structured, multi-stage research using Agentic
> AI, RAG, web search, vector retrieval, evidence-based scoring, and
> hallucination validation.**

```{=html}
<p align="center">
```
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C)
![Qwen3](https://img.shields.io/badge/Qwen3-8B-black)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![RAG](https://img.shields.io/badge/RAG-Enabled-8A2BE2)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-3B6E8F)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)

```{=html}
</p>
```

------------------------------------------------------------------------

## ✨ What is this?

Most GenAI applications follow a simple pattern:

``` text
User Question → LLM → Answer
```

This project takes a different approach.

The **Agentic Research Intelligence Platform** treats research as a
multi-stage engineering workflow:

``` text
Question
   ↓
Planning
   ↓
Web Research
   ↓
Company Discovery
   ↓
Company Research
   ↓
Source Verification
   ↓
RAG Indexing
   ↓
Vector Retrieval
   ↓
Company Qualification
   ↓
Evidence-Aware Scoring
   ↓
LLM Synthesis
   ↓
Hallucination Validation
   ↓
Final Research Report
```

The goal is to demonstrate how modern **Agentic AI + Generative AI +
RAG** systems can be designed beyond a single LLM call.

------------------------------------------------------------------------

# 🚀 Why I Built This

A research question such as:

> **"Analyze the Indian AI startup market and identify promising
> companies."**

requires more than generating a fluent answer.

A useful research system should be able to:

-   break a broad problem into smaller research tasks
-   identify companies and research topics
-   search for external evidence
-   store research knowledge
-   retrieve relevant information semantically
-   distinguish verified and unverified evidence
-   score companies using a consistent methodology
-   measure evidence coverage
-   generate a structured report
-   validate the generated result
-   track tokens, latency, and system performance

This project was built to explore exactly that architecture.

------------------------------------------------------------------------

# 🧠 Core AI Architecture

``` text
                         USER QUESTION
                              │
                              ▼
                       ┌─────────────┐
                       │   PLANNER   │
                       │  Qwen3 8B   │
                       └──────┬──────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        ┌──────────────┐             ┌───────────────┐
        │ Web Research │             │    Company    │
        │    Tavily    │             │   Discovery   │
        └──────┬───────┘             └───────┬───────┘
               │                             │
               └─────────────┬───────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Company Research│
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Source Verifier │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │   RAG Indexer   │
                    │     BGE-M3      │
                    └────────┬────────┘
                             ▼
                 ┌─────────────────────────┐
                 │ PostgreSQL + pgvector  │
                 └────────────┬────────────┘
                              ▼
                    ┌─────────────────┐
                    │  RAG Retriever  │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │   Qualifier     │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ Evidence-Aware  │
                    │     Scorer      │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │   Synthesizer   │
                    │     Qwen3       │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │  Hallucination  │
                    │    Validator    │
                    └────────┬────────┘
                             ▼
                       FINAL REPORT
```

------------------------------------------------------------------------

# ⭐ Key Features

### 🧩 Agentic Planning

The system uses **LangGraph** to coordinate multiple specialized
research stages instead of treating the LLM as a single chatbot.

### 🔎 Web Research

Uses **Tavily** to retrieve external research evidence.

### 📚 Retrieval-Augmented Generation

Research evidence is embedded using **BGE-M3** and stored in
**PostgreSQL + pgvector**.

``` text
Research Text
     ↓
BGE-M3 Embedding
     ↓
1024-dimensional Vector
     ↓
pgvector
     ↓
Semantic Retrieval
     ↓
LLM Context
```

### 🛡️ Source Verification

Sources are explicitly classified as:

-   `verified`
-   `unverified`
-   `demo`

This prevents fallback/demo evidence from being represented as
independently verified research.

### 📊 Evidence-Aware Scoring

Companies are evaluated across six categories:

  Category                      Purpose
  ----------------------------- ----------------------------------
  Funding                       Investment and funding evidence
  Product                       Product and technology evidence
  Customer Traction             Customer/client evidence
  Growth                        Growth and revenue evidence
  Market Opportunity            Market potential
  Competitive Differentiation   Differentiation from competitors

Unsupported categories receive zero rather than being guessed by the
LLM.

### 🎯 Evidence-Based Confidence

Confidence is calculated from actual evidence coverage.

For example:

``` text
Verified Sources: 0
Confidence: 0%
```

is a valid result when the system cannot independently verify the
available evidence.

### 🧪 Hallucination Validation

The final report is checked against deterministic research state.

The validator checks whether:

-   reported companies were actually researched
-   reported scores match deterministic scores
-   reported entities belong to the research plan
-   validation issues need to be surfaced

### 📈 Observability

The system tracks:

-   input tokens
-   output tokens
-   total tokens
-   latency
-   estimated cost
-   optional Langfuse traces

### 🧠 Persistent Memory

Redis can cache previous research results so repeated questions can
reuse previous results.

The application also handles Redis being unavailable without crashing
the research pipeline.

### ⚡ API + Frontend

The AI pipeline is exposed through:

**FastAPI**

and presented through:

**Streamlit**

------------------------------------------------------------------------

# 🏗️ Technology Stack

  Technology       Role
  ---------------- -----------------------------------
  **Python**       Core application
  **LangGraph**    Agent/workflow orchestration
  **Qwen3 8B**     Local generative LLM
  **Ollama**       Local LLM runtime
  **Tavily**       Web search/research
  **BGE-M3**       Embedding model
  **RAG**          Evidence retrieval architecture
  **PostgreSQL**   Persistent database
  **pgvector**     Vector similarity search
  **Supabase**     Managed PostgreSQL + pgvector
  **Pydantic**     Validation and structured outputs
  **FastAPI**      Backend REST API
  **Uvicorn**      ASGI server
  **Streamlit**    Python frontend
  **Redis**        Optional cache/memory
  **Langfuse**     Observability
  **HTTPX**        HTTP communication
  **pytest**       Testing
  **Git/GitHub**   Version control

------------------------------------------------------------------------

# 🔥 What Makes This an AI/ML Project?

This project combines several important modern AI engineering concepts:

``` text
                 Generative AI
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
       Qwen3                   LangGraph
          │                       │
          └───────────┬───────────┘
                      ▼
                  Agentic AI
                      │
                      ▼
                     RAG
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Embeddings              Vector Search
       BGE-M3                  pgvector
          │                       │
          └───────────┬───────────┘
                      ▼
             Evidence Pipeline
                      │
                      ▼
             Validation Layer
```

The project is not simply:

> **"Ask GPT and display the answer."**

It demonstrates the engineering required to build a more reliable AI
application around an LLM.

------------------------------------------------------------------------

# 🔗 Agentic Workflow

The LangGraph workflow can be summarized as:

``` text
START
  │
  ▼
Planner
  │
  ├───────────────┐
  ▼               ▼
Web Research   Market Research
  │               │
  └───────┬───────┘
          ▼
   Company Discovery
          │
          ▼
   Company Research
          │
          ▼
   Source Verification
          │
          ▼
      RAG Indexer
          │
          ▼
      RAG Retriever
          │
          ▼
  Company Qualification
          │
          ▼
        Scorer
          │
          ▼
      Synthesizer
          │
          ▼
 Hallucination Validator
          │
          ▼
         END
```

------------------------------------------------------------------------

# 🧱 Project Structure

``` text
agentic-research-intelligence-platform/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── market_researcher.py
│   │   ├── company_discovery.py
│   │   ├── company_researcher.py
│   │   ├── verifier.py
│   │   ├── rag_indexer.py
│   │   ├── retriever.py
│   │   ├── company_qualifier.py
│   │   ├── scorer.py
│   │   ├── confidence.py
│   │   ├── synthesizer.py
│   │   └── hallucination_validator.py
│   │
│   ├── models/
│   │   ├── planning.py
│   │   └── state.py
│   │
│   ├── services/
│   │   ├── llm.py
│   │   ├── embeddings.py
│   │   ├── supabase_client.py
│   │   ├── rag_retriever.py
│   │   ├── memory.py
│   │   ├── observability.py
│   │   └── usage.py
│   │
│   ├── tools/
│   │   ├── web_search.py
│   │   └── demo_research.py
│   │
│   ├── api.py
│   ├── graph.py
│   ├── main.py
│   └── streamlit_app.py
│
├── tests/
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

------------------------------------------------------------------------

# 🔬 RAG Pipeline

One of the most important parts of the project is the RAG pipeline.

## Step 1 --- Research Evidence

The system collects research content from web sources.

``` text
Company → Research Query → Retrieved Evidence
```

## Step 2 --- Embedding

The evidence is converted into a numerical representation using
**BGE-M3**.

``` text
Text → BGE-M3 → 1024-dimensional vector
```

## Step 3 --- Storage

The vector and metadata are stored in PostgreSQL using pgvector.

``` text
┌─────────────────────────────────────┐
│ PostgreSQL                          │
│                                     │
│ content                             │
│ source_url                          │
│ source_title                        │
│ company_name                        │
│ evidence_type                       │
│ embedding vector(1024)              │
└─────────────────────────────────────┘
```

## Step 4 --- Retrieval

A research query is embedded and compared with stored vectors.

``` text
Query
 ↓
Embedding
 ↓
Vector Similarity Search
 ↓
Top Relevant Documents
```

## Step 5 --- Generation

Retrieved evidence is passed into the synthesis stage.

This is the core RAG pattern:

``` text
Retrieve → Augment → Generate
```

------------------------------------------------------------------------

# 📊 Evidence-Aware Scoring

The project evaluates companies across six dimensions.

Instead of allowing the model to invent missing information, unsupported
categories receive zero.

Conceptually:

``` python
evidence_adjusted_score = (
    supported_score
    * (supported_category_count / 6)
)
```

This means evidence coverage affects the final score.

For example:

``` text
6 supported categories
        ↓
Full evidence coverage

2 supported categories
        ↓
Strong penalty for limited evidence
```

This makes the scoring mechanism more transparent than simply asking an
LLM:

> "Give this startup a score out of 10."

------------------------------------------------------------------------

# 🛡️ Reliability Architecture

The system deliberately combines **probabilistic LLM components** with
**deterministic software logic**.

``` text
LLM
 ↓
Research Plan
 ↓
Deterministic Qualification
 ↓
Retrieved Evidence
 ↓
Deterministic Evidence Scoring
 ↓
LLM Synthesis
 ↓
Deterministic Validation
```

This separation is important because the LLM should not be the only
component responsible for deciding whether its own output is correct.

------------------------------------------------------------------------

# 🧪 Example

### Input

``` text
Analyze the Indian AI startup market and identify promising companies.
```

### Planner

Produces research topics and candidate companies.

### Research

Searches for:

``` text
Funding
Products
Customers
Growth
Market opportunity
Competitive differentiation
```

### Retrieval

Relevant evidence is retrieved from the vector database.

### Scoring

Companies are scored using the available evidence.

### Synthesis

Qwen3 generates a structured report.

### Validation

The final report is checked against the research state.

------------------------------------------------------------------------

# 🖥️ Application

The project provides a Streamlit interface with:

-   research query input
-   research progress state
-   confidence score
-   verified source count
-   latency
-   token usage
-   executive summary
-   market overview
-   company analysis
-   evidence-adjusted scores
-   methodology
-   limitations
-   validation status
-   downloadable research report

------------------------------------------------------------------------

# 🔌 API

FastAPI exposes the research pipeline.

### Health Check

``` http
GET /health
```

Response:

``` json
{
  "status": "ok"
}
```

### Research Endpoint

``` http
POST /research
```

Request:

``` json
{
  "question": "Analyze the Indian AI startup market and identify promising companies."
}
```

The response includes:

``` text
Final Report
Confidence Score
Verified Source Count
Latency
Input Tokens
Output Tokens
Total Tokens
Estimated Cost
```

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the repository

``` bash
git clone https://github.com/Aayesha2103/agentic-research-intelligence-platform.git
cd agentic-research-intelligence-platform
```

## 2. Create a virtual environment

``` bash
python -m venv .venv
```

## 3. Activate it

### Windows PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

``` bash
pip install -r requirements.txt
```

## 5. Install Ollama models

``` bash
ollama pull qwen3:8b
ollama pull bge-m3
```

## 6. Configure environment variables

Create a `.env` file:

``` env
TAVILY_API_KEY=your_tavily_key

SUPABASE_URL=your_supabase_url
SUPABASE_SECRET_KEY=your_supabase_secret_key

REDIS_URL=redis://localhost:6379

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
```

> **Never commit `.env` or API keys to GitHub.**

## 7. Start the backend

``` powershell
uvicorn app.api:app --reload
```

## 8. Start the frontend

Open another terminal:

``` powershell
python -m streamlit run app\streamlit_app.py
```

------------------------------------------------------------------------

# 💡 Important Engineering Decisions

### Why LangGraph?

LangGraph provides explicit stateful workflow orchestration for the
research pipeline.

It allows individual stages to communicate through a shared research
state.

### Why Qwen3 8B?

It provides a capable local generative model without requiring the
primary application to depend on a paid hosted LLM API.

### Why Ollama?

Ollama provides a simple local runtime for running the LLM and embedding
model.

### Why BGE-M3?

BGE-M3 provides local text embeddings that can be used for semantic
retrieval.

### Why PostgreSQL + pgvector?

It combines normal relational storage with vector similarity search.

### Why Supabase?

Supabase provides managed PostgreSQL and pgvector infrastructure
suitable for a portfolio project.

### Why FastAPI?

FastAPI separates the AI pipeline from the presentation layer and
provides a clean API boundary.

### Why Streamlit?

Streamlit provides a Python-based frontend without requiring a separate
React/JavaScript application.

### Why deterministic validation?

Because the system should not rely entirely on an LLM to validate its
own output.

------------------------------------------------------------------------

# 🆚 Basic LLM App vs This Project

  Basic LLM Application     Agentic Research Platform
  ------------------------- -----------------------------
  Single prompt             Multi-stage workflow
  One model call            Multiple specialized stages
  No research planning      Planner
  No external evidence      Web research
  No retrieval layer        RAG
  No vector database        pgvector
  Free-form output          Structured output
  No evidence methodology   Evidence-aware scoring
  No confidence layer       Evidence-based confidence
  No validation             Hallucination validation
  No observability          Tokens + latency
  Chat-only interface       API + frontend

------------------------------------------------------------------------

# 📈 Current Limitations

This project is designed as a strong portfolio/fresher project rather
than a production-scale enterprise platform.

Current limitations include:

-   Local Qwen3 8B can be computationally expensive.
-   BGE-M3 embeddings also consume local resources.
-   Tavily depends on API availability and usage limits.
-   Demo/fallback evidence is not equivalent to independently verified
    web evidence.
-   Confidence is a project-specific evidence heuristic, not a
    statistically calibrated probability.
-   Hallucination validation checks consistency and grounding signals;
    it cannot guarantee factual perfection.
-   Redis is optional and requires a running Redis server for caching.
-   Hosted deployment requires a different LLM strategy if local Ollama
    models are unavailable.

------------------------------------------------------------------------

# 🚀 Future Improvements

Possible future extensions:

-   query rewriting
-   retrieval reranking
-   claim-to-source citation mapping
-   stronger source verification
-   automated evaluation datasets
-   retrieval evaluation metrics
-   calibrated confidence scoring
-   asynchronous research jobs
-   background workers
-   hosted LLM support
-   richer Langfuse dashboards
-   production deployment architecture

------------------------------------------------------------------------

# 🎓 What This Project Demonstrates

This project demonstrates practical experience with:

-   **Agentic AI**
-   **Generative AI**
-   **LLM orchestration**
-   **LangGraph**
-   **RAG**
-   **Embeddings**
-   **Vector databases**
-   **Semantic search**
-   **PostgreSQL**
-   **pgvector**
-   **Web research**
-   **Structured outputs**
-   **Evidence validation**
-   **Hallucination mitigation**
-   **FastAPI**
-   **Streamlit**
-   **Redis**
-   **Observability**
-   **Token tracking**
-   **Latency measurement**
-   **AI system design**

------------------------------------------------------------------------

# 💼 Resume-Level Project Summary

> **Built an end-to-end Agentic Research Intelligence Platform using
> LangGraph, Qwen3, RAG, BGE-M3, PostgreSQL/pgvector, Tavily, FastAPI,
> and Streamlit. Designed a multi-stage research workflow with planning,
> web research, source verification, semantic retrieval, evidence-aware
> scoring, confidence estimation, hallucination validation, and LLM
> observability.**

------------------------------------------------------------------------

# 🗣️ Interview Explanation

If an interviewer asks:

> **"Explain your project."**

A concise answer is:

> I built an Agentic Research Intelligence Platform that automates
> complex research questions using a multi-stage AI workflow. Instead of
> directly sending a question to an LLM, I use LangGraph to coordinate
> planning, web research, source verification, RAG indexing, retrieval,
> company qualification, evidence-based scoring, synthesis, and final
> validation. Qwen3 8B runs locally through Ollama, while BGE-M3
> generates embeddings that are stored in PostgreSQL with pgvector. The
> system also tracks confidence, token usage and latency, and uses
> deterministic validation to detect inconsistencies in the generated
> report. FastAPI exposes the backend and Streamlit provides the user
> interface.

------------------------------------------------------------------------

# 👩‍💻 Author

### Aayesha Singh

**Data Science Engineering \| AI/ML \| Generative AI \| Agentic AI**

GitHub: [Aayesha2103](https://github.com/Aayesha2103)

------------------------------------------------------------------------

## ⭐ If you found this project interesting

Feel free to explore the architecture and implementation.

**The main idea behind this project:**

> ### Don't just ask an LLM for an answer. Build a system around it.
