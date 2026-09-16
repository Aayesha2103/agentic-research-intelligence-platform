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

    print(
        "Company scores:",
        len(result["company_scores"])
    )

    print(
        "Final report stored:",
        bool(result["final_report"])
    )

    print(
        "Final report length:",
        len(result["final_report"])
    )

    print()
    print("===== COMPANY SCORES =====")

    for score in result["company_scores"]:

        print()
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

    print()
    print("===== FINAL REPORT PREVIEW =====")
    print()

    print(
        result["final_report"][:1000]
    )


if __name__ == "__main__":
    main()