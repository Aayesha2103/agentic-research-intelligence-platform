from app.models.state import ResearchState
from app.graph import build_research_graph


def main():

    print("===== FULL AGENTIC GRAPH TEST =====")
    print()

    state = ResearchState(
        question=(
            "Analyze the Indian AI startup market "
            "and tell me which companies are most promising."
        )
    )

    graph = build_research_graph()

    print("[1] Running complete research graph...")
    print()

    result = graph.invoke(state)

    print("===== FINAL GRAPH STATE =====")
    print()

    print(
        "Research topics:",
        len(result["research_topics"])
    )

    print(
        "Search queries:",
        len(result["search_queries"])
    )

    print(
        "Discovered companies:",
        result["companies_to_research"]
    )

    print(
        "General sources:",
        len(result["sources"])
    )

    print(
        "Market sources:",
        len(result["market_sources"])
    )

    print(
        "Company sources:",
        len(result["company_sources"])
    )

    print(
        "Qualifications:",
        len(result["company_qualifications"])
    )

    print(
        "Verified sources:",
        len(result["verified_sources"])
    )

    print()
    print("===== QUALIFICATION RESULTS =====")

    for qualification in result["company_qualifications"]:

        print()
        print("Company:", qualification["company_name"])
        print(
            "AI focused:",
            qualification["is_ai_focused"]
        )
        print(
            "Indian:",
            qualification["is_indian"]
        )
        print(
            "Startup:",
            qualification["is_startup"]
        )
        print(
            "AI is core business:",
            qualification["ai_is_core_business"]
        )
        print(
            "Should research:",
            qualification["should_research"]
        )
        print(
            "Confidence:",
            qualification["qualification_confidence"]
        )
        print(
            "Reason:",
            qualification["reason"]
        )

        print("Evidence:")

        for evidence in qualification["evidence"]:
            print(
                " -",
                evidence
            )

if __name__ == "__main__":
    main()