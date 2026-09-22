import json

from app.models.state import ResearchState
from app.services.llm import get_llm


SCORING_CATEGORIES = [
    "funding_score",
    "product_score",
    "customer_traction_score",
    "growth_score",
    "market_opportunity_score",
    "competitive_differentiation_score",
]


def get_evidence_for_company(
    evidence: list[dict],
    company_name: str,
) -> list[dict]:

    company_key = (
        company_name.strip().lower()
    )

    return [
        item
        for item in evidence
        if item.get(
            "company",
            "",
        ).strip().lower()
        == company_key
    ]


def calculate_supported_overall_score(
    company: dict,
    supported_categories: list[str],
) -> float:

    if not supported_categories:
        return 0.0

    scores = []

    for category in supported_categories:

        value = float(
            company.get(
                category,
                0.0,
            )
        )

        value = max(
            0.0,
            min(10.0, value),
        )

        scores.append(value)

    return round(
        sum(scores) / len(scores),
        2,
    )


def calculate_evidence_adjusted_score(
    supported_score: float,
    supported_category_count: int,
) -> float:

    total_categories = len(
        SCORING_CATEGORIES
    )

    evidence_coverage = (
        supported_category_count
        / total_categories
    )

    adjusted_score = (
        supported_score
        * evidence_coverage
    )

    return round(
        adjusted_score,
        2,
    )


def build_evidence(
    state: ResearchState,
) -> list[dict]:

    evidence = []

    for source in state.verified_sources:

        company = source.get(
            "company",
            source.get(
                "company_name",
                "",
            ),
        )

        if not company:
            continue

        evidence.append({
            "company": company,
            "title": source.get(
                "title",
                "",
            ),
            "content": source.get(
                "content",
                "",
            ),
            "evidence_type": source.get(
                "evidence_type",
                "general",
            ),
            "url": source.get(
                "url",
                "",
            ),
            "verification_status": source.get(
                "verification_status",
                "unknown",
            ),
        })

    for document in state.retrieved_documents:

        company = document.get(
            "company_name",
            "",
        )

        if not company:
            continue

        evidence.append({
            "company": company,
            "title": document.get(
                "source_title",
                "",
            ),
            "content": document.get(
                "content",
                "",
            ),
            "evidence_type": document.get(
                "evidence_type",
                "general",
            ),
            "url": document.get(
                "source_url",
                "",
            ),
            "verification_status": "rag",
        })

    return evidence


def build_compact_evidence_text(
    companies: list[str],
    evidence: list[dict],
) -> str:

    sections = []

    for company in companies:

        company_evidence = (
            get_evidence_for_company(
                evidence,
                company,
            )
        )

        if not company_evidence:
            continue

        section = [
            f"COMPANY: {company}"
        ]

        for item in company_evidence:

            content = item.get(
                "content",
                "",
            ).strip()

            content = content[:2500]

            section.append(
                f"TITLE: "
                f"{item.get('title', '')}\n"
                f"TYPE: "
                f"{item.get('evidence_type', 'general')}\n"
                f"VERIFICATION: "
                f"{item.get('verification_status', 'unknown')}\n"
                f"EVIDENCE: {content}\n"
                f"URL: "
                f"{item.get('url', '')}"
            )

        sections.append(
            "\n".join(section)
        )

    return "\n\n".join(sections)


def scoring_node(
    state: ResearchState,
) -> dict:

    if not state.company_qualifications:

        print(
            "No companies available "
            "for scoring."
        )

        return {
            "company_scores": []
        }

    companies = []

    for qualification in (
        state.company_qualifications
    ):

        company_name = qualification.get(
            "company_name",
            "",
        )

        should_research = qualification.get(
            "should_research",
            False,
        )

        if (
            company_name
            and should_research
            and company_name not in companies
        ):
            companies.append(
                company_name
            )

    if not companies:

        print(
            "No qualified companies "
            "available for scoring."
        )

        return {
            "company_scores": []
        }

    evidence = build_evidence(
        state
    )

    evidence_text = (
        build_compact_evidence_text(
            companies,
            evidence,
        )
    )

    if not evidence_text.strip():

        print(
            "No company-specific "
            "evidence available "
            "for scoring."
        )

        return {
            "company_scores": []
        }

    prompt = f"""
You are an evidence-based scoring agent.

Companies:
{", ".join(companies)}

Evidence:
{evidence_text}

Score every company from 0 to 10
for these categories:

- funding_score
- product_score
- customer_traction_score
- growth_score
- market_opportunity_score
- competitive_differentiation_score

Rules:

1. Use ONLY supplied evidence.

2. Never use outside knowledge.

3. Evidence for one company cannot
   support another company.

4. Give 0 when a category is not
   supported by evidence.

5. Investor interest is NOT customer
   traction.

6. Revenue growth is NOT customer
   traction.

7. Revenue growth is NOT automatically
   competitive differentiation.

8. Do not assume market opportunity.

9. Be conservative when evidence is sparse.

10. Do NOT calculate overall_score.

11. Return one object for every
    qualified company.

12. Return ONLY valid JSON.

Format:

[
  {{
    "company_name": "Company",
    "funding_score": 0,
    "product_score": 0,
    "customer_traction_score": 0,
    "growth_score": 0,
    "market_opportunity_score": 0,
    "competitive_differentiation_score": 0,
    "reasoning": "Short evidence-based explanation."
  }}
]
"""

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    text = response.content

    if not text:

        print(
            "Scorer returned empty output."
        )

        return {
            "company_scores": []
        }

    print()
    print(
        "===== RAW SCORER OUTPUT ====="
    )
    print(text)
    print(
        "============================="
    )
    print()

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip()
            == "```"
        ):
            lines = lines[:-1]

        text = "\n".join(
            lines
        ).strip()

    company_scores = []

    try:

        parsed = json.loads(
            text
        )

        if isinstance(
            parsed,
            dict,
        ):
            parsed = [parsed]

        if not isinstance(
            parsed,
            list,
        ):
            parsed = []

        for company in parsed:

            if not isinstance(
                company,
                dict,
            ):
                continue

            company_name = company.get(
                "company_name",
                "",
            )

            if company_name not in companies:
                continue

            cleaned_company = {
                "company_name":
                    company_name
            }

            for category in (
                SCORING_CATEGORIES
            ):

                try:

                    value = float(
                        company.get(
                            category,
                            0,
                        )
                    )

                except (
                    ValueError,
                    TypeError,
                ):

                    value = 0.0

                value = max(
                    0.0,
                    min(10.0, value),
                )

                cleaned_company[
                    category
                ] = value

            actual_evidence = (
                get_evidence_for_company(
                    evidence,
                    company_name,
                )
            )

            evidence_count = len(
                actual_evidence
            )

            # Prevent sparse evidence
            # from producing very high
            # category scores.
            if evidence_count == 1:

                for category in (
                    SCORING_CATEGORIES
                ):
                    cleaned_company[
                        category
                    ] = min(
                        cleaned_company[
                            category
                        ],
                        6.0,
                    )

            elif evidence_count == 2:

                for category in (
                    SCORING_CATEGORIES
                ):
                    cleaned_company[
                        category
                    ] = min(
                        cleaned_company[
                            category
                        ],
                        8.0,
                    )

            supported_categories = [
                category
                for category in (
                    SCORING_CATEGORIES
                )
                if cleaned_company[
                    category
                ] > 0
            ]

            supported_score = (
                calculate_supported_overall_score(
                    cleaned_company,
                    supported_categories,
                )
            )

            evidence_adjusted_score = (
                calculate_evidence_adjusted_score(
                    supported_score,
                    len(
                        supported_categories
                    ),
                )
            )

            cleaned_company[
                "supported_score"
            ] = supported_score

            cleaned_company[
                "overall_score"
            ] = evidence_adjusted_score

            cleaned_company[
                "reasoning"
            ] = company.get(
                "reasoning",
                "",
            )

            cleaned_company[
                "supported_categories"
            ] = supported_categories

            cleaned_company[
                "supported_category_count"
            ] = len(
                supported_categories
            )

            cleaned_company[
                "evidence_count"
            ] = evidence_count

            company_scores.append(
                cleaned_company
            )

    except json.JSONDecodeError as error:

        print(
            "Scorer returned invalid JSON."
        )

        print(
            f"JSON parsing error: {error}"
        )

    print(
        f"Companies scored: "
        f"{len(company_scores)}"
    )

    print()

    print(
        "===== FINAL EVIDENCE-ADJUSTED SCORES ====="
    )

    for score in company_scores:

        print(
            f"{score.get('company_name')} "
            f"=> "
            f"{score.get('overall_score')} "
            f"(supported: "
            f"{score.get('supported_score')}, "
            f"categories: "
            f"{score.get('supported_category_count')}/"
            f"{len(SCORING_CATEGORIES)})"
        )

    print(
        "==========================================="
    )

    print()

    return {
        "company_scores":
            company_scores
    }