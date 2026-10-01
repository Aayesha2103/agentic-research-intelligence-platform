<div align="center">

# 🤖 Agentic Research Intelligence Platform

### 🔬 From complex questions to structured, validated research reports

> An evidence-aware **Agentic AI research system** that turns complex research questions into structured, validated reports.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

<p>
  <img src="https://img.shields.io/badge/Agentic_AI-LangGraph-8A2BE2?style=flat-square">
  <img src="https://img.shields.io/badge/RAG-BGE--M3-blue?style=flat-square">
  <img src="https://img.shields.io/badge/LLM-Qwen3_8B-orange?style=flat-square">
  <img src="https://img.shields.io/badge/Validation-Hallucination_Check-success?style=flat-square">
</p>

</div>

---

## 🚀 Overview

Unlike a basic **LLM → Answer** application, this project uses a multi-stage AI workflow:

```mermaid
flowchart TD
    Q[❓ Question] --> P[🧭 Planner]
    P --> W[🔎 Web Research]
    W --> C[🏢 Company Research]
    C --> V[✅ Source Verification]
    V --> R[📚 RAG + Vector Retrieval]
    R --> S[📊 Evidence-Based Scoring]
    S --> L[🧠 LLM Synthesis]
    L --> H[🛡️ Hallucination Validation]
    H --> F[📄 Final Report]
```

<div align="center">

| ❌ Basic LLM App | ✅ This Platform |
|:-:|:-:|
| Question → Answer | Plan → Research → Verify → Score → Validate |
| No evidence trail | Evidence-aware scoring |
| Unchecked output | Hallucination validation |

</div>

---

## ✨ Key Features

| | Feature | Details |
|:-:|---|---|
| 🧠 | **Agentic Workflow** | Built with LangGraph |
| 🔎 | **Web Research** | Powered by Tavily |
| 📚 | **RAG** | BGE-M3 embeddings |
| 🗄️ | **Semantic Retrieval** | PostgreSQL + pgvector |
| 🤖 | **Local LLM** | Qwen3 8B through Ollama |
| 📊 | **Company Scoring** | Evidence-aware |
| 🛡️ | **Validation** | Source verification & hallucination validation |
| 🎯 | **Confidence** | Evidence-based confidence scoring |
| 📈 | **Monitoring** | Token & latency tracking |
| ⚡ | **Interface** | FastAPI backend + Streamlit UI |
| 🧠 | **Memory / Cache** | Optional Redis |
| 🔬 | **Observability** | Optional Langfuse |

---

## 🛠️ Tech Stack

<div align="center">

`Python` `LangGraph` `Qwen3` `Ollama` `RAG` `BGE-M3` `Tavily` `PostgreSQL` `pgvector` `Supabase` `FastAPI` `Streamlit` `Redis` `Langfuse` `Pydantic`

</div>

---

## 🎯 Example

> 💬 **"Analyze the Indian AI startup market and identify promising companies."**

The system plans the research, gathers evidence, retrieves relevant information, scores companies based on available evidence, generates a report, and validates the final output.

---

## 🔮 Future Improvements

- [ ] 🌐 Build a more advanced web interface
- [ ] 🔄 Add hybrid search and reranking
- [ ] 📊 Add retrieval evaluation metrics
- [ ] 🧠 Add stronger conversation history and memory
- [ ] 🐳 Dockerize the application
- [ ] ☁️ Deploy the application
- [ ] 🔗 Add richer source and citation tracking
- [ ] ⚙️ Improve asynchronous/background processing

---

<div align="center">

⭐ **If you found this project interesting, consider giving it a star!** ⭐

</div>
