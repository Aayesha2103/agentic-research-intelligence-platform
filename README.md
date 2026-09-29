Agentic Research Intelligence Platform

An evidence-aware AI research system that turns complex research questions into a structured, multi-agent investigation — with web research, RAG, source verification, scoring, and hallucination validation.














Why this project?

Most AI research demos follow a simple pattern:

User Question
     ↓
     LLM
     ↓
   Answer

That works for a chatbot.

But research is different.

A useful research system needs to:

break a broad question into smaller tasks
search for external evidence
distinguish stronger and weaker sources
store information for semantic retrieval
retrieve relevant evidence before generating an answer
evaluate entities using a consistent framework
track confidence and evidence coverage
validate the generated result
expose measurable latency and token usage

That's the problem this project is designed to address.

What I built

The Agentic Research Intelligence Platform is a LangGraph-based AI research pipeline that transforms a natural-language research question into a structured research report.

For example:

"Analyze the Indian AI startup market and identify promising companies."

The system doesn't simply send this question to an LLM.

Instead, it creates a research workflow:

                     USER QUESTION
                           │
                           ▼
                       PLANNER
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       WEB RESEARCH              COMPANY DISCOVERY
             │                           │
             └─────────────┬─────────────┘
                           ▼
                   COMPANY RESEARCH
                           │
                           ▼
                  SOURCE VERIFICATION
                           │
                           ▼
                    RAG INDEXING
                           │
                    BGE-M3 Embeddings
                           │
                           ▼
                PostgreSQL + pgvector
                           │
                           ▼
                    RAG RETRIEVAL
                           │
                           ▼
                  COMPANY QUALIFICATION
                           │
                           ▼
                 EVIDENCE-AWARE SCORING
                           │
                           ▼
                     SYNTHESIZER
                           │
                           ▼
               HALLUCINATION VALIDATOR
                           │
                           ▼
                     FINAL REPORT
Key Features
Agentic Research Workflow

Uses LangGraph to orchestrate specialized research stages rather than relying on a single LLM call.

Local LLM

Uses Qwen3 8B through Ollama for local planning and report synthesis.

This avoids requiring a paid hosted LLM API for the primary model.

Web Research

Uses Tavily to gather external research evidence.

RAG Pipeline

Research documents are:

Research Evidence
       ↓
BGE-M3 Embedding
       ↓
1024-dimensional Vector
       ↓
PostgreSQL + pgvector
       ↓
Semantic Retrieval
Source Verification

Sources are classified as:

verified
unverified
demo

This prevents fallback/demo evidence from being treated as independently verified research.

Evidence-Aware Scoring

Companies are evaluated across:

Category	What it represents
Funding	Funding/investment evidence
Product	Product/technology evidence
Customer Traction	Customer/client evidence
Growth	Growth/revenue evidence
Market Opportunity	Market potential evidence
Competitive Differentiation	Differentiation evidence

The final score is adjusted according to how many categories are actually supported by evidence.

Confidence Scoring

Confidence is based on evidence coverage, not how confident the LLM sounds.

This means the system can legitimately return:

Confidence: 0%
Verified Sources: 0

when independently verified evidence is unavailable.

Hallucination Validation

After the LLM generates the final report, a validation stage checks that:

reported companies were actually researched
reported scores match deterministic scores
generated entities belong to the research plan
validation issues are surfaced in the final report
Observability

Tracks:

input tokens
output tokens
total tokens
latency
estimated cost
optional Langfuse traces
Persistent Memory

Redis can cache previous research results so repeated questions can reuse previously generated reports.

The application also continues gracefully when Redis is unavailable.

API + UI

The research engine is exposed through:

FastAPI

and presented through:

Streamlit

Architecture
                         ┌──────────────────┐
                         │     Streamlit    │
                         │    Frontend UI   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │      Backend     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         │  Orchestration   │
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
        ┌─────────┐        ┌────────────┐       ┌────────────┐
        │ Planner │        │ Web Search │       │ Discovery  │
        └─────────┘        └─────┬──────┘       └─────┬──────┘
                                  │                    │
                                  └─────────┬──────────┘
                                            ▼
                                  ┌─────────────────┐
                                  │ Source Verifier │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │   BGE-M3 RAG    │
                                  │    Indexing     │
                                  └────────┬────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │ PostgreSQL + pgvector   │
                              └────────────┬────────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │    Retriever    │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │   Qualification │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │     Scorer      │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │    Synthesizer  │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │    Validator    │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  Research Report│
                                  └─────────────────┘
Tech Stack
Technology	Purpose
Python	Core application
LangGraph	Agent orchestration
Qwen3 8B	Local generative LLM
Ollama	Local model runtime
Tavily	Web research
BGE-M3	Text embeddings
RAG	Evidence retrieval
PostgreSQL	Persistent database
pgvector	Vector similarity search
Supabase	Managed PostgreSQL + pgvector
Pydantic	Data validation + structured outputs
FastAPI	Backend API
Uvicorn	ASGI server
Streamlit	Frontend
Redis	Optional research-result memory/cache
Langfuse	Optional observability
HTTPX	HTTP communication
pytest	Testing
Git/GitHub	Version control
AI / GenAI Architecture

The project combines several important GenAI patterns.

1. Structured LLM Output

The planner doesn't return arbitrary text.

It generates a structured ResearchPlan:

ResearchPlan
├── research_topics
├── companies_to_research
└── search_queries

This makes LLM output usable by deterministic downstream code.

2. Agentic Orchestration

Instead of:

Prompt → LLM → Answer

the system uses:

Goal
 ↓
Plan
 ↓
Act
 ↓
Retrieve
 ↓
Evaluate
 ↓
Generate
 ↓
Validate
3. Retrieval-Augmented Generation

The LLM isn't expected to know everything.

The system retrieves relevant research evidence first:

Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Evidence
   ↓
LLM
   ↓
Grounded Report
4. Deterministic Guardrails

The project deliberately combines probabilistic AI with deterministic logic.

Examples:

LLM
 ↓
Company candidates
 ↓
Deterministic qualification
 ↓
Evidence
 ↓
Deterministic score adjustment
 ↓
LLM synthesis
 ↓
Deterministic validation

This is one of the central engineering ideas behind the project.

Evidence-Aware Scoring

The scoring system does not assume that missing evidence means a company is strong or weak.

Instead:

Supported Categories
        ↓
Calculate Supported Score
        ↓
Measure Evidence Coverage
        ↓
Adjust Overall Score

Conceptually:

evidence_adjusted_score = (
    supported_score
    * (supported_category_count / 6)
)

Therefore, a company with strong evidence in only 2 out of 6 categories doesn't receive the same confidence as a company with evidence across all six.

Reliability Layer

The project contains several layers designed to reduce unsupported output:

                 LLM
                  │
                  ▼
          ┌───────────────┐
          │ Source        │
          │ Verification  │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ Qualification │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ Evidence-aware│
          │    Scoring    │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │   Synthesis   │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ Hallucination │
          │   Validation  │
          └───────────────┘

The goal is not to claim that the system is hallucination-free.

The goal is to make unsupported behavior detectable and constrained.

Example Workflow
Input
Analyze the Indian AI startup market
and identify promising companies.
Planner

Produces:

Research Topics
├── Funding
├── Product
├── Customer Traction
├── Growth
├── Market Opportunity
└── Competitive Differentiation

and generates relevant companies/search queries.

Research

Tavily searches for evidence.

Verification

Sources are classified:

Verified
Unverified
Demo
RAG

Evidence is embedded:

Text
 ↓
BGE-M3
 ↓
1024-dimensional vector
 ↓
pgvector
Retrieval

Relevant company-specific evidence is retrieved.

Scoring

Companies are evaluated across six dimensions.

Synthesis

Qwen3 generates the final structured report.

Validation

The system checks that the generated report matches the deterministic research state.

Project Structure
app/
│
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── market_researcher.py
│   ├── company_discovery.py
│   ├── company_researcher.py
│   ├── verifier.py
│   ├── rag_indexer.py
│   ├── retriever.py
│   ├── company_qualifier.py
│   ├── scorer.py
│   ├── confidence.py
│   ├── synthesizer.py
│   └── hallucination_validator.py
│
├── models/
│   ├── planning.py
│   └── state.py
│
├── services/
│   ├── llm.py
│   ├── embeddings.py
│   ├── supabase_client.py
│   ├── rag_retriever.py
│   ├── memory.py
│   ├── observability.py
│   └── usage.py
│
├── tools/
│   ├── web_search.py
│   └── demo_research.py
│
├── api.py
├── graph.py
├── main.py
└── streamlit_app.py
Running Locally
1. Clone
git clone https://github.com/Aayesha2103/agentic-research-intelligence-platform.git
cd agentic-research-intelligence-platform
2. Create environment
python -m venv .venv
3. Activate

Windows PowerShell:

.\.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Install and run Ollama

Install Ollama and pull the required models:

ollama pull qwen3:8b
ollama pull bge-m3
6. Configure environment variables

Create:

.env

and configure:

TAVILY_API_KEY=your_tavily_key

SUPABASE_URL=your_supabase_url
SUPABASE_SECRET_KEY=your_supabase_secret_key

REDIS_URL=redis://localhost:6379

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key

Never commit .env to GitHub.

7. Start FastAPI
uvicorn app.api:app --reload
8. Start Streamlit

In another terminal:

python -m streamlit run app\streamlit_app.py
Example API
Health check
GET /health

Response:

{
  "status": "ok"
}
Research
POST /research

Request:

{
  "question": "Analyze the Indian AI startup market and identify promising companies."
}

The response contains:

final report
confidence score
verified source information
latency
token usage
cost tracking information
Engineering Decisions
Why Qwen3 locally?

To avoid depending on a paid LLM API for the main model and to demonstrate local LLM deployment.

Why BGE-M3?

To generate local semantic embeddings for RAG.

Why pgvector?

To combine relational metadata with vector similarity search inside PostgreSQL.

Why LangGraph?

To explicitly represent the multi-stage research workflow and state transitions.

Why FastAPI?

To separate the AI research engine from the UI and expose it through an API.

Why Streamlit?

To build the frontend entirely in Python without introducing a separate React/JavaScript application.

Why deterministic validation?

Because an LLM should not be the only component deciding whether its own output is correct.

What Makes This Different From a Basic Chatbot?
Basic LLM App	This Project
Single prompt	Multi-stage workflow
One LLM call	Multiple specialized stages
No explicit research plan	Planner agent
No evidence pipeline	Web research + verification
No semantic memory	RAG + pgvector
Free-form output	Structured outputs
No scoring methodology	Evidence-aware scoring
No validation	Hallucination validation
No confidence measurement	Evidence-based confidence
No system metrics	Tokens + latency
Chat UI only	FastAPI + Streamlit
Hosted model dependency	Local Qwen3 option
Current Limitations

This project intentionally prioritizes a practical portfolio architecture over production-scale infrastructure.

Current limitations include:

Local Qwen3 8B can be computationally expensive.
BGE-M3 embedding generation also consumes local resources.
Tavily depends on API availability and quota.
Demo/fallback evidence is not equivalent to independently verified web evidence.
The confidence score is a project-specific heuristic rather than a statistically calibrated probability.
Hallucination validation checks structural consistency; it does not guarantee factual perfection.
Redis is optional and requires a running Redis server for caching.
Hosted deployment cannot assume that the local Ollama models are available.
Future Improvements

Potential extensions include:

query rewriting
retrieval reranking
claim-to-source citation mapping
stronger source verification
evaluation datasets
automated evaluation metrics
calibrated confidence scoring
asynchronous research workers
hosted LLM support
background research jobs
richer observability dashboards
production deployment architecture
What I Learned

Building this project helped me work with:

Agentic AI architecture
LLM orchestration
LangGraph state management
Structured LLM outputs
RAG
Embeddings
Vector databases
Semantic search
PostgreSQL
pgvector
Web research APIs
Evidence validation
Hallucination mitigation
FastAPI
Streamlit
Redis
Observability
Token and latency tracking
AI system design

The most important lesson was that building an AI application is not just about calling an LLM.

The engineering challenge is designing the system around the LLM.

Portfolio Highlight

Built an end-to-end agentic research system that combines LLM reasoning, web retrieval, RAG, vector search, deterministic scoring, source verification, and post-generation validation into a single research workflow.

Author

Aayesha Singh

Data Science Engineering | AI/ML | Generative AI | Agentic AI

If you want to understand the project deeply

The repository's architecture is intentionally designed so that each major AI capability has a distinct responsibility:

PLAN
 ↓
SEARCH
 ↓
VERIFY
 ↓
INDEX
 ↓
RETRIEVE
 ↓
QUALIFY
 ↓
SCORE
 ↓
SYNTHESIZE
 ↓
VALIDATE

That is the core story of the project.
