from app.models.state import ResearchState
from app.agents.scorer import scoring_node


def main():

    print("===== SCORING AGENT TEST =====")
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

    print("[1] Running scoring agent...")
    print()

    result = scoring_node(state)

    print(
        "Number of company scores:",
        len(result["company_scores"])
    )

    print()

    for score in result["company_scores"]:

        print("Company:", score["company_name"])
        print("Funding score:", score["funding_score"])
        print("Product score:", score["product_score"])
        print("Customer score:", score["customer_score"])
        print("Growth score:", score["growth_score"])
        print("Market score:", score["market_score"])
        print(
            "Competitive score:",
            score["competitive_score"]
        )
        print("Overall score:", score["overall_score"])

        print()
        print("Reasoning:")
        print(score["reasoning"])


if __name__ == "__main__":
    main()