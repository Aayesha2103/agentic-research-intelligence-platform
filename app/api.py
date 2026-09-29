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

    # state.verified_sources intentionally contains three
    # evidence classes:
    #   1. genuinely verified web sources
    #   2. unverified web sources
    #   3. demo/fallback sources
    #
    # The UI must not call all three "verified".
    all_sources = result.verified_sources or []

    verified_sources = [
        source
        for source in all_sources
        if source.get("verification_status") == "verified"
    ]

    unverified_sources = [
        source
        for source in all_sources
        if (
            source.get("source_type") == "web"
            and source.get("verification_status")
            == "unverified"
        )
    ]

    demo_sources = [
        source
        for source in all_sources
        if source.get("verification_status") == "demo"
    ]

    return {
        "question": result.question,
        "final_report": result.final_report,
        "confidence_score": result.confidence_score,
        "total_latency_seconds": result.total_latency_seconds,
        "total_input_tokens": result.total_input_tokens,
        "total_output_tokens": result.total_output_tokens,
        "total_tokens": result.total_tokens,
        "total_cost_usd": result.total_cost_usd,

        # Only real verified sources are exposed here.
        "verified_sources": verified_sources,
        "verified_source_count": len(verified_sources),

        # Kept separately so the UI can explain why
        # confidence may still be low.
        "unverified_source_count": len(unverified_sources),
        "demo_source_count": len(demo_sources),
    }
