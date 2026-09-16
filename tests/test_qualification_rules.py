from app.agents.company_qualifier import (
    count_evidence,
    company_qualification_node
)
from app.models.state import ResearchState


print("===== TEST 1: EVIDENCE COUNTING =====")

text = """
Haptik is an artificial intelligence company.
It uses machine learning and conversational AI.
The Indian startup has raised venture funding
from investors.
"""

ai_keywords = [
    "artificial intelligence",
    "ai company",
    "machine learning",
    "generative ai",
    "conversational ai",
]

startup_keywords = [
    "startup",
    "venture funding",
    "funding round",
    "raised",
    "investors",
]

indian_keywords = [
    "india",
    "indian",
    "india-based",
    "based in india",
]

print(
    "AI evidence:",
    count_evidence(text.lower(), ai_keywords)
)

print(
    "Startup evidence:",
    count_evidence(
        text.lower(),
        startup_keywords
    )
)

print(
    "Indian evidence:",
    count_evidence(
        text.lower(),
        indian_keywords
    )
)


print("\n===== TEST 2: QUALIFICATION =====")

state = ResearchState(
    question="Test qualification rules",
    companies_to_research=[
        "Haptik",
        "UnknownCompany"
    ],
    company_sources=[
        {
            "company": "Haptik",
            "title": "Haptik Indian AI startup",
            "content": """
            Haptik is an artificial intelligence company
            using machine learning and conversational AI.
            The Indian startup has raised venture funding
            from investors.
            """,
            "url": "https://example.com/haptik",
            "relevance_score": 0.95,
        },
        {
            "company": "UnknownCompany",
            "title": "Technology company",
            "content": """
            UnknownCompany provides technology services.
            """,
            "url": "https://example.com/unknown",
            "relevance_score": 0.80,
        },
    ],
)


result = company_qualification_node(state)


for qualification in result["company_qualifications"]:

    print(
        "\nCompany:",
        qualification["company_name"]
    )

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