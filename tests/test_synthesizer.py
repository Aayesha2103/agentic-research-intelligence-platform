from app.models.state import ResearchState
from app.agents.synthesizer import synthesizer_node


def test_synthesizer_node():

    print("===== SYNTHESIZER AGENT TEST =====")
    print()

    state = ResearchState(
        question="Evaluate an Indian AI startup",
        companies_to_research=["TestAI"],
    )

    state.verified_sources = [
        {
            "company": "TestAI",
            "source_type": "company",
            "title": "TestAI AI Platform",
            "url": "https://techcrunch.com/testai",
            "evidence_type": "product",
            "source_quality": 0.90,
            "content": (
                "TestAI is an Indian AI startup providing "
                "an artificial intelligence platform."
            ),
        },
        {
            "company": "TestAI",
            "source_type": "company",
            "title": "TestAI Funding",
            "url": "https://inc42.com/testai",
            "evidence_type": "funding",
            "source_quality": 0.85,
            "content": (
                "TestAI has raised funding from technology "
                "investors."
            ),
        },
        {
            "source_type": "market",
            "title": "Indian AI Startup Ecosystem",
            "url": "https://yourstory.com/indian-ai",
            "evidence_type": "market",
            "source_quality": 0.80,
            "content": (
                "India has a growing ecosystem of AI startups "
                "across multiple technology sectors."
            ),
        },
    ]

    state.company_scores = [
        {
            "company_name": "TestAI",
            "funding_score": 7,
            "product_score": 8,
            "customer_traction_score": 6,
            "growth_score": 7,
            "market_opportunity_score": 8,
            "competitive_differentiation_score": 6,
            "overall_score": 7.0,
            "reasoning": (
                "The company has evidence of funding, "
                "AI product development, and market opportunity."
            ),
        }
    ]

    state.retrieved_documents = [
        {
            "content": (
                "TestAI provides an artificial intelligence "
                "platform for enterprise customers."
            ),
            "source_url": "https://techcrunch.com/testai",
            "source_title": "TestAI AI Platform",
            "company_name": "TestAI",
            "evidence_type": "product",
            "similarity": 0.85,
        }
    ]

    print("[1] Running synthesizer agent...")
    print()

    result = synthesizer_node(state)

    assert "final_report" in result
    assert result["final_report"]

    assert "confidence_score" in result
    assert 0 <= result["confidence_score"] <= 1

    print("Confidence score:", result["confidence_score"])

    print()
    print("Final report:")
    print(result["final_report"])

    print()
    print("Synthesizer agent test completed successfully.")