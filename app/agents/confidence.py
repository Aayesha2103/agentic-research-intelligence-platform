from app.models.state import ResearchState


def confidence_node(
    state: ResearchState,
) -> dict:

    total_companies = len(
        state.companies_to_research
    )

    if total_companies == 0:
        return {
            "confidence_score": 0.0
        }

    # Only genuinely verified web sources
    # count as independent evidence.
    real_verified_sources = [
        source
        for source in state.verified_sources
        if source.get(
            "verification_status"
        ) == "verified"
    ]

    verified_sources = len(
        real_verified_sources
    )

    # Identify companies supported by
    # genuinely verified web evidence.
    verified_companies = set()

    for source in real_verified_sources:

        company = source.get(
            "company",
            source.get(
                "company_name",
                "",
            ),
        ).strip()

        if company:
            verified_companies.add(
                company.lower()
            )

    verified_company_coverage = (
        len(verified_companies)
        / total_companies
    )

    # Demo sources are tracked separately.
    demo_sources = [
        source
        for source in state.verified_sources
        if source.get(
            "verification_status"
        ) == "demo"
    ]

    demo_source_count = len(
        demo_sources
    )

    # RAG documents are derived from the
    # indexed evidence. They must NOT be
    # treated as independent sources.
    retrieved_documents = len(
        state.retrieved_documents
    )

    # Confidence is intentionally conservative.
    #
    # 60% = verified-source coverage
    # 20% = verified-source quantity
    # 20% = evidence availability
    #
    # Demo/RAG data cannot increase the
    # verified-source components.

    verified_coverage_score = (
        verified_company_coverage
    )

    verified_quantity_score = min(
        verified_sources / 10,
        1.0,
    )

    evidence_available_score = (
        1.0
        if (
            verified_sources > 0
            and retrieved_documents > 0
        )
        else 0.0
    )

    confidence = (
        verified_coverage_score * 0.6
        + verified_quantity_score * 0.2
        + evidence_available_score * 0.2
    )

    confidence = round(
        confidence,
        2,
    )

    print()
    print("===== CONFIDENCE =====")

    print(
        "Companies in research plan: "
        f"{total_companies}"
    )

    print(
        "Companies with verified evidence: "
        f"{len(verified_companies)}/"
        f"{total_companies}"
    )

    print(
        "Real verified sources: "
        f"{verified_sources}"
    )

    print(
        "Demo sources: "
        f"{demo_source_count}"
    )

    print(
        "RAG documents: "
        f"{retrieved_documents}"
    )

    print(
        "Confidence score: "
        f"{confidence}"
    )

    print("======================")
    print()

    return {
        "confidence_score": confidence
    }