from app.models.state import ResearchState
from app.agents.company_discovery import company_discovery_node


def main():

    state = ResearchState(
        question="Analyze the Indian AI startup market.",
        sources=[
            {
                "title": "Top Indian AI Startups",
                "content": """
                Haptik is an Indian conversational AI company.
                Sarvam AI is an Indian AI startup building generative
                AI models and applications.
                Infosys provides AI services to enterprise customers.
                """
            },
            {
                "title": "Indian AI Startup Ecosystem",
                "content": """
                Indian AI startups include Haptik and Sarvam AI.
                Several established IT companies also invest in AI.
                """
            }
        ]
    )

    result = company_discovery_node(state)

    print("===== COMPANY DISCOVERY TEST =====")
    print()
    print("Discovered companies:")

    for company in result["companies_to_research"]:
        print("-", company)


if __name__ == "__main__":
    main()