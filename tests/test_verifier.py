from app.models.state import ResearchState
from app.agents.verifier import source_verifier_node


def main():

    print("===== SOURCE VERIFIER TEST =====")
    print()

    state = ResearchState(
        question="Test source verification"
    )

    state.sources = [
        {
            "query": "Indian AI startup funding",
            "title": "Indian AI Startup Raises Funding",
            "url": "https://inc42.com/example",
            "content": "AI startup raised funding from investors.",
            "relevance_score": 0.90,
        },
        {
            "query": "Indian AI startup funding",
            "title": "Same Article",
            "url": "https://inc42.com/example",
            "content": "Duplicate source.",
            "relevance_score": 0.80,
        },
        {
            "query": "Indian AI startup",
            "title": "Low Relevance Source",
            "url": "https://example.com/low",
            "content": "Some information.",
            "relevance_score": 0.50,
        },
        {
            "query": "Indian AI startup",
            "title": "Blocked Source",
            "url": "https://wikipedia.org/example",
            "content": "Some information.",
            "relevance_score": 0.95,
        },
    ]

    result = source_verifier_node(state)

    print(
        "Verified sources:",
        len(result.verified_sources)
    )

    print()

    for source in result.verified_sources:

        print("Title:", source["title"])
        print("Domain:", source["domain"])
        print(
            "Domain trusted:",
            source["domain_trusted"]
        )
        print(
            "Quality score:",
            source["source_quality_score"]
        )
        print(
            "Evidence type:",
            source["evidence_type"]
        )
        print(
            "Verification status:",
            source["verification_status"]
        )

        print()


if __name__ == "__main__":
    main()