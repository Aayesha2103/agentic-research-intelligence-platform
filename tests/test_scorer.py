from app.models.state import ResearchState
from app.agents.scorer import scoring_node


def test_scoring_node():

    print("===== SCORING AGENT TEST =====")
    print()

    state = ResearchState(
        question="Evaluate an Indian AI startup",
        companies_to_research=["TestAI"],
    )

    state.company_qualifications = [
        {
            "company_name": "TestAI",
            "should_research": True
        }
    ]

    state.verified_sources = [
        {
            "company": "TestAI",
            "title": "TestAI Raises Funding",
            "url": "https://inc42.com/testai-funding",
            "evidence_type": "funding",
            "content": (
                "TestAI is an Indian AI startup that "
                "raised funding from technology investors."
            )
        },
        {
            "company": "TestAI",
            "title": "TestAI Launches AI Platform",
            "url": "https://techcrunch.com/testai-platform",
            "evidence_type": "product",
            "content": (
                "TestAI provides an artificial intelligence "
                "platform using machine learning technology "
                "for enterprise customers."
            )
        },
        {
            "company": "TestAI",
            "title": "TestAI Expands Customer Base",
            "url": "https://yourstory.com/testai-customers",
            "evidence_type": "customers",
            "content": (
                "TestAI has expanded its customer base and "
                "formed partnerships with several businesses."
            )
        }
    ]

    # Simulated RAG result
    state.retrieved_documents = [
        {
            "content": (
                "TestAI provides an artificial intelligence "
                "platform for enterprise customers."
            ),
            "source_url": "https://techcrunch.com/testai-platform",
            "source_title": "TestAI Launches AI Platform",
            "company_name": "TestAI",
            "evidence_type": "product",
            "similarity": 0.85
        }
    ]

    print("[1] Running scoring agent...")
    print()

    result = scoring_node(state)

    assert "company_scores" in result
    assert len(result["company_scores"]) > 0

    print(
        "Number of company scores:",
        len(result["company_scores"])
    )

    print()

    for score in result["company_scores"]:

        print("Company:", score["company_name"])
        print("Overall score:", score["overall_score"])

        print()
        print("Reasoning:")
        print(score["reasoning"])

    print()
    print("Scoring agent test completed successfully.")