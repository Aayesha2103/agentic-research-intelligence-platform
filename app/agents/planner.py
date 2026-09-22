from app.models.state import ResearchState
from app.services.llm import get_planner_llm


DEFAULT_COMPANIES = [
    "Sarvam AI",
    "Krutrim",
    "CoRover",
    "E42",
    "Yellow.ai",
    "Uniphore",
]


DEFAULT_TOPICS = [
    "Indian AI startup funding",
    "Indian AI startup products and technology",
    "Indian AI startup customers and traction",
    "Indian AI startup growth",
    "Indian AI startup market opportunities",
    "Indian AI startup competitive differentiation",
]


EXCLUDED_COMPANIES = {
    "infosys",
    "tcs",
    "tata consultancy services",
    "wipro",
    "cognizant",
    "bosch",
    "bosch india",
}


def clean_company_name(company: str) -> str:
    """
    Removes numbering and unnecessary formatting
    from a company name.
    """

    company = company.strip()

    company = company.lstrip(
        "0123456789.-) "
    )

    return company


def validate_companies(
    companies: list[str],
) -> list[str]:
    """
    Keeps only companies from the approved
    Indian AI startup candidate list.
    """

    validated = []

    allowed = {
        company.lower(): company
        for company in DEFAULT_COMPANIES
    }

    for company in companies:

        company = clean_company_name(company)

        if not company:
            continue

        company_key = company.lower()

        if company_key in EXCLUDED_COMPANIES:
            continue

        if company_key not in allowed:
            continue

        canonical_name = allowed[company_key]

        if canonical_name not in validated:
            validated.append(canonical_name)

    return validated


def clean_query(query: str) -> str:
    """
    Removes accidental year assumptions and
    incomplete query endings.
    """

    query = query.strip()

    year_ranges = [
        "2022-2023",
        "2023-2024",
        "2022–2024",
        "2023–2024",
        "2022 - 2024",
        "2023 - 2024",
    ]

    for year_range in year_ranges:
        query = query.replace(
            year_range,
            "",
        )

    words = query.split()

    cleaned_words = []

    for word in words:

        if (
            len(word) == 4
            and word.isdigit()
            and word.startswith("20")
        ):
            continue

        cleaned_words.append(word)

    query = " ".join(cleaned_words)

    incomplete_endings = [
        "in",
        "with",
        "for",
        "and",
        "or",
        "of",
        "to",
    ]

    changed = True

    while changed:

        changed = False

        lowered = query.lower()

        for ending in incomplete_endings:

            if lowered.endswith(
                f" {ending}"
            ):

                query = query[
                    : -len(ending)
                ].strip()

                changed = True
                break

    return query


def validate_queries(
    queries: list[str],
) -> list[str]:
    """
    Cleans and deduplicates search queries.
    """

    validated = []

    for query in queries:

        query = clean_query(query)

        if len(query) < 10:
            continue

        if query.lower() in {
            item.lower()
            for item in validated
        }:
            continue

        validated.append(query)

    return validated[:10]


def planner_node(
    state: ResearchState,
) -> dict:
    """
    Creates a research plan from the user's question.
    """

    print()
    print("===== RESEARCH PLAN =====")

    llm = get_planner_llm()

    prompt = f"""
You are the planning agent for an Indian AI
startup research platform.

User question:
{state.question}

Create:

1. Research topics
2. Search queries

IMPORTANT:

- Do not invent years.
- Do not invent dates.
- Do not invent time periods.
- Do not create company names.
- Do not provide a company list.
- Focus on funding, products, customers,
  growth, market opportunity, and differentiation.
- Search queries must be complete.
- Never end a query with "in", "with", "for",
  "and", "or", "of", or "to".
- Generate 5 to 10 useful search queries.
- Generate 5 to 8 research topics.
"""

    try:

        plan = llm.invoke(prompt)

        research_topics = [
            topic.strip()
            for topic in plan.research_topics
            if topic.strip()
        ]

        search_queries = validate_queries(
            plan.search_queries
        )

        companies = DEFAULT_COMPANIES.copy()

        if not research_topics:
            research_topics = DEFAULT_TOPICS.copy()

        if not search_queries:
            search_queries = [
                "Indian AI startups funding",
                "Indian AI startups products and technology",
                "Indian AI startups customers and traction",
                "Indian AI startups growth",
                "Indian AI startup market opportunities",
                "Indian AI startup competitive differentiation",
            ]

    except Exception as error:

        print(
            f"Planner failed, using fallback plan: {error}"
        )

        research_topics = DEFAULT_TOPICS.copy()

        search_queries = [
            "Indian AI startups funding",
            "Indian AI startups products and technology",
            "Indian AI startups customers and traction",
            "Indian AI startups growth",
            "Indian AI startup market opportunities",
            "Indian AI startup competitive differentiation",
        ]

        companies = DEFAULT_COMPANIES.copy()

    print()
    print("Research topics:")

    for topic in research_topics:
        print(f"- {topic}")

    print()
    print("Companies to research:")

    for company in companies:
        print(f"- {company}")

    print()
    print("Search queries:")

    for query in search_queries:
        print(f"- {query}")

    print()
    print("===== END RESEARCH PLAN =====")
    print()

    return {
        "research_topics": research_topics,
        "companies_to_research": companies,
        "search_queries": search_queries,
    }