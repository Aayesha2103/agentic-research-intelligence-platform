import json

from app.models.state import ResearchState
from app.services.llm import get_llm
from app.services.llm_usage import extract_usage


SCORING_CATEGORIES = [
    "funding_score",
    "product_score",
    "customer_traction_score",
    "growth_score",
    "market_opportunity_score",
    "competitive_differentiation_score",
]


def build_company_evidence(
    state: ResearchState,
    company: str,
) -> list[dict]:
    """Collect only evidence belonging to the requested company."""

    evidence = []

    for source in state.verified_sources:
        source_company = source.get(
            "company",
            source.get("company_name", ""),
        ).strip()

        if source_company.lower() == company.lower():
            evidence.append(source)

    for document in state.retrieved_documents:
        document_company = document.get(
            "company_name",
            "",
        ).strip()

        if document_company.lower() == company.lower():
            evidence.append(document)

    return evidence


def parse_score_response(response) -> dict:
    """Convert the LLM response into a Python dictionary."""

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)


def calculate_evidence_adjusted_score(
    scores: dict,
    evidence_count: int,
) -> tuple[float, float, int]:
    """Calculate a score using only categories supported by evidence."""

    supported_scores = []

    for category in SCORING_CATEGORIES:
        value = scores.get(category)

        if isinstance(value, (int, float)) and value > 0:
            supported_scores.append(float(value))

    supported_category_count = len(supported_scores)

    if supported_category_count == 0:
        return 0.0, 0.0, 0

    supported_score = (
        sum(supported_scores) / supported_category_count
    )

    if evidence_count <= 2:
        supported_score = min(supported_score, 2.0)

    evidence_adjusted_score = (
        supported_score
        * (supported_category_count / len(SCORING_CATEGORIES))
    )

    return (
        round(supported_score, 2),
        round(evidence_adjusted_score, 2),
        supported_category_count,
    )


def scoring_node(state: ResearchState) -> dict:
    """Score qualified companies using only company-specific evidence."""

    llm = get_llm()

    company_scores = []

    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_cost_usd = 0.0

    for company in state.companies_to_research:

        evidence = build_company_evidence(
            state,
            company,
        )

        if not evidence:
            continue

        evidence_text = "\n\n".join(
            [
                (
                    f"Title: {item.get('title', item.get('source_title', ''))}\n"
                    f"URL: {item.get('url', item.get('source_url', ''))}\n"
                    f"Evidence type: {item.get('evidence_type', 'unknown')}\n"
                    f"Content: {item.get('content', '')}"
                )
                for item in evidence
            ]
        )

        prompt = f"""
You are scoring an Indian AI startup using ONLY the evidence supplied below.

Company:
{company}

Evidence:
{evidence_text}

Score each category from 0 to 5.

Categories:

1. funding_score
2. product_score
3. customer_traction_score
4. growth_score
5. market_opportunity_score
6. competitive_differentiation_score

Rules:

- Use ONLY the supplied evidence.
- Evidence belonging to another company must not be used.
- Unsupported categories must receive 0.
- Investor interest is NOT customer traction.
- Revenue growth is NOT customer traction.
- Do not assume facts that are not explicitly supported.
- Return ONLY valid JSON.
- Do not include markdown.

Required JSON format:

{{
    "funding_score": 0,
    "product_score": 0,
    "customer_traction_score": 0,
    "growth_score": 0,
    "market_opportunity_score": 0,
    "competitive_differentiation_score": 0
}}
"""

        try:
            response = llm.invoke(prompt)

            usage = extract_usage(response)

            total_input_tokens += usage.input_tokens
            total_output_tokens += usage.output_tokens
            total_tokens += usage.total_tokens
            total_cost_usd += usage.estimated_cost_usd

            scores = parse_score_response(response)

        except Exception as error:
            print(
                f"Scoring failed for {company}: {error}"
            )
            continue

        evidence_count = len(evidence)

        (
            supported_score,
            evidence_adjusted_score,
            supported_category_count,
        ) = calculate_evidence_adjusted_score(
            scores,
            evidence_count,
        )

        company_scores.append(
            {
                "company": company,
                **{
                    category: scores.get(category, 0)
                    for category in SCORING_CATEGORIES
                },
                "supported_score": supported_score,
                "evidence_adjusted_score": evidence_adjusted_score,
                "overall_score": evidence_adjusted_score,
                "supported_category_count": supported_category_count,
                "evidence_count": evidence_count,
            }
        )

    print()
    print("===== SCORING =====")
    print(
        f"Scored companies: {len(company_scores)}"
    )
    print(
        "Scorer LLM usage: "
        f"input={total_input_tokens}, "
        f"output={total_output_tokens}, "
        f"total={total_tokens}, "
        f"cost=${total_cost_usd:.4f}"
    )
    print("===== END SCORING =====")
    print()

    return {
        "company_scores": company_scores,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
        "total_cost_usd": total_cost_usd,
    }