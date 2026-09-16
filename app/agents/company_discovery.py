from app.models.state import ResearchState
from app.services.llm import get_llm


def company_discovery_node(
    state: ResearchState
) -> dict:
    """
    Company Discovery Agent.

    Uses the research collected from the web to identify
    candidate Indian AI-focused startups.
    """

    llm = get_llm()

    research_text = ""

    sorted_sources = sorted(
        state.sources,
        key=lambda source: source.get(
            "relevance_score",
            0.0
        ),
        reverse=True
    )

    selected_sources = sorted_sources[:30]

    for source in selected_sources:
        research_text += (
            source.get("title", "")
            + "\n"
            + source.get("content", "")
            + "\n\n"
        )

    print()
    print("===== COMPANY DISCOVERY INPUT =====")
    print(
        "Number of research sources:",
        len(state.sources)
    )

    print()
    print("Research source titles:")

    for source in state.sources[:20]:
        print(
            "-",
            source.get("title", "")
        )

    print("===== END COMPANY DISCOVERY INPUT =====")
    print()

    if not research_text.strip():
        return {
            "companies_to_research": []
        }

    response = llm.invoke(
        f"""
        Identify candidate Indian AI-focused startups
        from the following research evidence.

        Research evidence:
        {research_text}

        Rules:

        1. Return only specific company names.

        2. The company should be relevant to the
           Indian AI startup ecosystem.

        3. AI should be a core part of the company's
           primary product or business.

        4. Do not include large established corporations
           such as Infosys, TCS, Wipro, Cognizant, or Bosch.

        5. Do not include companies merely because
           they use AI internally.

        6. Do not include companies merely because
           they have an office or operations in India.

        7. Do not include companies headquartered
           outside India merely because they operate
           in India.

        8. Do not invent company names.

        9. Only select companies that are actually
           mentioned or clearly supported by the
           supplied research evidence.

        10. Return at most 8 companies.

        11. If the evidence does not contain enough
            information to identify any suitable companies,
            return exactly:

            No companies found.

        Return ONLY the company names,
        one company per line.

        Do not provide explanations.
        """
    )

    print()
    print("===== RAW COMPANY DISCOVERY RESPONSE =====")
    print(response.content)
    print("===== END RAW COMPANY DISCOVERY RESPONSE =====")
    print()

    companies = []

    response_text = response.content.strip()

    no_company_phrases = [
        "no companies listed",
        "no companies found",
        "no suitable companies",
        "no company names",
        "no companies identified",
    ]

    if any(
        phrase in response_text.lower()
        for phrase in no_company_phrases
    ):
        return {
            "companies_to_research": []
        }

    for line in response_text.splitlines():

        company = line.strip()

        company = company.lstrip(
            "-•0123456789. "
        )

        if not company:
            continue

        if "excluded" in company.lower():
            continue

        if company.lower().startswith(
            (
                "the provided",
                "the research",
                "there are",
                "no "
            )
        ):
            continue

        if company not in companies:
            companies.append(company)

    return {
        "companies_to_research": companies[:8]
    }