from fastapi import FastAPI
from pydantic import BaseModel

from app.main import run_research


app = FastAPI(
    title="Agentic Research Intelligence Platform",
    description="AI-powered research and market intelligence API",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/research")
def research(request: ResearchRequest):
    result = run_research(request.question)

    return {
        "question": result.question,
        "final_report": result.final_report,
        "confidence_score": result.confidence_score,
        "total_latency_seconds": result.total_latency_seconds,
        "total_input_tokens": result.total_input_tokens,
        "total_output_tokens": result.total_output_tokens,
        "total_tokens": result.total_tokens,
        "total_cost_usd": result.total_cost_usd,
    }