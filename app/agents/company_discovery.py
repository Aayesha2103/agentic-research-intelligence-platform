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

    for source in state.sources:
        research_text += (
            source.get("title", "")
            + "\n"
            + source.get("content", "")
            + "\n\n"
        )

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

        Return ONLY the company names,
        one company per line.

        Do not provide explanations.
        """
    )

    companies = []

    for line in response.content.splitlines():

        company = line.strip()

        company = company.lstrip(
            "-•0123456789. "
        )

        if company and company not in companies:
            companies.append(company)

    return {
        "companies_to_research": companies[:8]
    }