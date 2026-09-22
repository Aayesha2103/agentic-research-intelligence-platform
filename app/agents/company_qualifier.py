from app.models.state import ResearchState


ESTABLISHED_COMPANIES = {
    "infosys",
    "tcs",
    "tata consultancy services",
    "wipro",
    "cognizant",
    "bosch",
    "bosch india",
}


AI_KEYWORDS = {
    "artificial intelligence",
    "ai company",
    "ai startup",
    "machine learning",
    "generative ai",
    "conversational ai",
    "computer vision",
    "natural language processing",
    "nlp",
    "robotics",
    "ai cloud",
}


STARTUP_KEYWORDS = {
    "startup",
    "venture funding",
    "funding round",
    "raised",
    "investors",
    "backed by",
    "seed funding",
    "series a",
    "series b",
    "series c",
    "revenue growth",
    "revenue",
    "profit",
    "valuation",
    "strategic pivot",
}


INDIAN_KEYWORDS = {
    "india",
    "indian",
    "india-based",
    "based in india",
    "headquartered in india",
    "indian market",
}


def company_qualification_node(state: ResearchState) -> dict:

    qualifications = []

    evidence_by_company = {}

    for document in state.retrieved_documents:

        company = document.get(
            "company_name",
            "",
        ).strip()

        if not company:
            continue

        evidence_by_company.setdefault(
            company,
            [],
        ).append(
            document.get("content", "")
        )

    companies = []

    for company in state.companies_to_research:

        company = company.strip()

        if company and company not in companies:
            companies.append(company)

    for company in evidence_by_company:

        if company and company not in companies:
            companies.append(company)

    for company in companies:

        normalized_name = company.lower().strip()

        if normalized_name in ESTABLISHED_COMPANIES:

            qualifications.append(
                {
                    "company_name": company,
                    "should_research": False,
                    "confidence": 0.98,
                    "reason": (
                        "Established company excluded from "
                        "startup-focused analysis."
                    ),
                }
            )

            continue

        evidence = evidence_by_company.get(
            company,
            [],
        )

        evidence_text = " ".join(
            evidence
        ).lower()

        if not evidence:

            qualifications.append(
                {
                    "company_name": company,
                    "should_research": False,
                    "confidence": 0.40,
                    "reason": (
                        "No company-specific evidence "
                        "was retrieved."
                    ),
                }
            )

            continue

        ai_evidence = sum(
            1
            for keyword in AI_KEYWORDS
            if keyword in evidence_text
        )

        startup_evidence = sum(
            1
            for keyword in STARTUP_KEYWORDS
            if keyword in evidence_text
        )

        indian_evidence = sum(
            1
            for keyword in INDIAN_KEYWORDS
            if keyword in evidence_text
        )

        company_name_evidence = (
            company.lower() in evidence_text
        )

        enough_evidence = (
            company_name_evidence
            and ai_evidence >= 1
            and (
                indian_evidence >= 1
                or startup_evidence >= 1
            )
        )

        qualifications.append(
            {
                "company_name": company,
                "should_research": enough_evidence,
                "confidence": (
                    0.90
                    if enough_evidence
                    else 0.55
                ),
                "reason": (
                    "Company-specific evidence supports "
                    "AI activity and business/startup relevance."
                    if enough_evidence
                    else
                    "Evidence is insufficient to qualify "
                    "the company."
                ),
            }
        )

    print()
    print("===== COMPANY QUALIFICATION =====")
    print(
        f"Companies evaluated: "
        f"{len(qualifications)}"
    )

    for qualification in qualifications:

        print(
            f"{qualification['company_name']}: "
            f"{qualification['should_research']}"
        )

    print(
        "===== END COMPANY QUALIFICATION ====="
    )
    print()

    return {
        "company_qualifications": qualifications
    }