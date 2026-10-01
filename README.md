# 🤖 Agentic Research Intelligence Platform

> An evidence-aware **Agentic AI research system** that turns complex research questions into structured, validated reports.

## 🚀 Overview

Unlike a basic **LLM → Answer** application, this project uses a multi-stage AI workflow:

```text
Question
   ↓
Planner → Web Research → Company Research
   ↓
Source Verification
   ↓
RAG + Vector Retrieval
   ↓
Evidence-Based Scoring
   ↓
LLM Synthesis
   ↓
Hallucination Validation
   ↓
Final Report
```

## ✨ Key Features

- 🧠 **Agentic workflow** with LangGraph
- 🔎 **Web research** using Tavily
- 📚 **RAG** with BGE-M3 embeddings
- 🗄️ **PostgreSQL + pgvector** for semantic retrieval
- 🤖 **Local Qwen3 8B** through Ollama
- 📊 **Evidence-aware company scoring**
- 🛡️ **Source verification & hallucination validation**
- 🎯 **Evidence-based confidence scoring**
- 📈 **Token & latency tracking**
- ⚡ **FastAPI backend + Streamlit UI**
- 🧠 Optional **Redis memory/cache**
- 🔬 Optional **Langfuse observability**

## 🛠️ Tech Stack

**Python · LangGraph · Qwen3 · Ollama · RAG · BGE-M3 · Tavily · PostgreSQL · pgvector · Supabase · FastAPI · Streamlit · Redis · Langfuse · Pydantic**

## 🎯 Example

> **"Analyze the Indian AI startup market and identify promising companies."**

The system plans the research, gathers evidence, retrieves relevant information, scores companies based on available evidence, generates a report, and validates the final output.

## 🔮 Future Improvements

- 🌐 Build a more advanced web interface
- 🔄 Add hybrid search and reranking
- 📊 Add retrieval evaluation metrics
- 🧠 Add stronger conversation history and memory
- 🐳 Dockerize the application
- ☁️ Deploy the application
- 🔗 Add richer source and citation tracking
- ⚙️ Improve asynchronous/background processing

---

<p align="center">

⭐ **If you found this project interesting, consider giving it a star!**

</p>
