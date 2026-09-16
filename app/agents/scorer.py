from app.models.state import ResearchState
from app.models.scoring import CompanyScore
from app.services.llm import get_llm


def scoring_node(
    state: ResearchState
) -> dict:
    """
    Scoring Agent.

    Uses verified research evidence to score each
    qualified company across multiple dimensions.
    """

    llm = get_llm()

    scoring_llm = llm.with_structured_output(
        CompanyScore
    )

    company_scores = []

    qualified_companies = [
        qualification["company_name"]
        for qualification
        in state.company_qualifications
        if qualification["should_research"]
    ]

    for company in qualified_companies:

        company_sources = [
            source
            for source in state.verified_sources
            if source.get("company") == company
        ]

        evidence_text = ""

        for source in company_sources:

            evidence_text += (
                f"Title: {source.get('title', '')}\n"
                f"URL: {source.get('url', '')}\n"
                f"Evidence type: "
                f"{source.get('evidence_type', '')}\n"
                f"Content: "
                f"{source.get('content', '')}\n\n"
            )

        if not evidence_text.strip():
            continue

        score = scoring_llm.invoke(
            f"""
            Evaluate the following Indian AI startup
            using ONLY the supplied research evidence.

            Company:
            {company}

            Research evidence:
            {evidence_text}

            Score each category from 0 to 10.

            funding_score:
            Strength of funding and investor evidence.

            product_score:
            Strength and differentiation of the product
            or AI technology.

            customer_score:
            Evidence of customers, partnerships,
            deployments, or adoption.

            growth_score:
            Evidence of business growth, users,
            revenue, expansion, or momentum.

            market_score:
            Strength of the market opportunity relevant
            to this company.

            competitive_score:
            Evidence of differentiation and competitive
            positioning.

            overall_score:
            Your overall evidence-based assessment.

            IMPORTANT:

            - Use ONLY the supplied evidence.
            - Do not invent facts.
            - Do not assume missing information is positive.
            - If evidence for a category is weak or missing,
              give a conservative score.
            - Do not use popularity as a substitute for evidence.
            - Explain the reasoning briefly.
            """
        )

        company_scores.append(
            score.model_dump()
        )

    return {
        "company_scores": company_scores
    }