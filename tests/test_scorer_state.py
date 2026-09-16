from app.models.state import ResearchState
from app.agents.scorer import scoring_node


def main():

    print("===== SCORER → STATE TEST =====")
    print()

    state = ResearchState(
        question="Evaluate an Indian AI startup"
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
            "title": "TestAI AI Platform",
            "url": "https://techcrunch.com/testai-platform",
            "evidence_type": "product",
            "content": (
                "TestAI provides an artificial intelligence "
                "platform using machine learning technology "
                "for enterprise customers."
            )
        }
    ]

    print("[1] Running scoring agent...")
    print()

    result = scoring_node(state)

    print(
        "Scores returned:",
        len(result["company_scores"])
    )

    print()

    state.company_scores = result["company_scores"]

    print(
        "Scores stored in state:",
        len(state.company_scores)
    )

    print()

    for score in state.company_scores:

        print(
            "Company:",
            score["company_name"]
        )

        print(
            "Overall score:",
            score["overall_score"]
        )

        print(
            "Reasoning:",
            score["reasoning"]
        )


if __name__ == "__main__":
    main()