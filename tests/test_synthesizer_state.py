from app.models.state import ResearchState
from app.agents.synthesizer import synthesizer_node


def main():

    print("===== SYNTHESIZER → STATE TEST =====")
    print()

    state = ResearchState(
        question=(
            "Analyze the Indian AI startup market "
            "and tell me which companies are most promising."
        )
    )

    state.company_scores = [
        {
            "company_name": "TestAI",
            "funding_score": 8.0,
            "product_score": 8.0,
            "customer_score": 7.0,
            "growth_score": 7.0,
            "market_score": 8.0,
            "competitive_score": 7.0,
            "overall_score": 7.5,
            "reasoning": (
                "The company has evidence of funding, "
                "a differentiated AI product, customer adoption, "
                "and a relevant market opportunity."
            ),
        }
    ]

    state.verified_sources = [
        {
            "source_type": "market",
            "title": "Indian AI Market Overview",
            "url": "https://example.com/market",
            "evidence_type": "market",
            "content": (
                "India has a growing artificial intelligence "
                "startup ecosystem with increasing investment "
                "and adoption."
            ),
        },
        {
            "source_type": "company",
            "company": "TestAI",
            "title": "TestAI Raises Funding",
            "url": "https://example.com/testai",
            "evidence_type": "funding",
            "content": (
                "TestAI raised funding from investors to expand "
                "its artificial intelligence product."
            ),
        },
    ]

    print("[1] Running synthesizer...")
    print()

    result = synthesizer_node(state)

    print("[2] Updating state with synthesizer result...")
    print()

    state.final_report = result["final_report"]

    print("===== STATE RESULT =====")
    print()

    print(
        "Final report stored:",
        bool(state.final_report)
    )

    print(
        "Final report length:",
        len(state.final_report)
    )

    print()
    print("===== FIRST 300 CHARACTERS =====")
    print()

    print(state.final_report[:300])


if __name__ == "__main__":
    main()
    