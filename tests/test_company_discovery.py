from app.models.state import ResearchState
from app.agents.company_discovery import company_discovery_node


def main():

    print("===== COMPANY DISCOVERY LARGE-INPUT TEST =====")
    print()

    sources = []

    for i in range(160):

        relevance_score = 0.50 + (i % 50) / 100

        sources.append(
            {
                "title": f"Indian AI Startup Research {i + 1}",
                "content": (
                    "Indian AI startup ecosystem research "
                    "covering artificial intelligence companies "
                    "and startup funding."
                ),
                "url": f"https://example.com/source-{i + 1}",
                "relevance_score": relevance_score,
            }
        )

    state = ResearchState(
        question=(
            "Analyze the Indian AI startup market "
            "and tell me which companies are most promising."
        )
    )

    state.sources = sources

    print(
        "Sources provided to discovery:",
        len(state.sources)
    )

    print(
        "Highest relevance score:",
        max(
            source["relevance_score"]
            for source in state.sources
        )
    )

    print(
        "Lowest relevance score:",
        min(
            source["relevance_score"]
            for source in state.sources
        )
    )

    print()
    print("[1] Running company discovery...")
    print()

    result = company_discovery_node(state)

    print()
    print("===== DISCOVERY RESULT =====")
    print()

    print(
        "Companies discovered:",
        result["companies_to_research"]
    )

    print(
        "Number of companies:",
        len(result["companies_to_research"])
    )


if __name__ == "__main__":
    main()