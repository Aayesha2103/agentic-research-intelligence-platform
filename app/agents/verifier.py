from urllib.parse import urlparse

from app.models.state import ResearchState


def classify_evidence(source: dict) -> str:
    """
    Classifies a source according to the type of evidence
    it most likely contains.
    """

    query = source.get("query", "").lower()
    title = source.get("title", "").lower()
    content = source.get("content", "").lower()

    primary_text = query + " " + title

    if any(
        keyword in primary_text
        for keyword in [
            "funding",
            "funded",
            "investment",
            "investor",
            "raised",
            "funding round",
            "valuation",
        ]
    ):
        return "funding"

    if any(
        keyword in primary_text
        for keyword in [
            "customer",
            "client",
            "partnership",
            "partner",
            "deployment",
            "case study",
            "adoption",
        ]
    ):
        return "customers"

    if any(
        keyword in primary_text
        for keyword in [
            "product",
            "platform",
            "technology",
            "solution",
            "generative ai",
            "machine learning",
            "computer vision",
            "artificial intelligence",
        ]
    ):
        return "product"

    if any(
        keyword in primary_text
        for keyword in [
            "government",
            "policy",
            "regulation",
            "initiative",
            "scheme",
            "ministry",
            "indiaai",
        ]
    ):
        return "policy"

    if any(
        keyword in primary_text
        for keyword in [
            "market",
            "ecosystem",
            "industry",
            "market size",
            "market growth",
            "startup landscape",
        ]
    ):
        return "market"

    if any(
        keyword in primary_text
        for keyword in [
            "revenue",
            "users",
            "growth",
            "employees",
            "profit",
            "business growth",
        ]
    ):
        return "growth"

    return "general"


def get_domain(url: str) -> str:
    """
    Extracts the hostname from a URL.
    """

    parsed_url = urlparse(url)

    hostname = parsed_url.hostname or ""

    return hostname.lower()


def calculate_source_quality(
    relevance_score: float,
    domain_trusted: bool
) -> float:
    """
    Calculates the final quality score for a source.

    Tavily relevance provides the base score.
    Trusted domains receive a small quality bonus.
    """

    quality_score = relevance_score

    if domain_trusted:
        quality_score += 0.10

    return min(
        quality_score,
        1.0
    )


def source_verifier_node(
    state: ResearchState
) -> ResearchState:
    """
    Source Verification Agent.

    Combines sources collected by all research agents
    and evaluates their quality using:

    - URL validation
    - domain trust
    - blocked-source rules
    - relevance score
    - evidence classification
    - URL deduplication
    """

    trusted_domains = {
        "gov.in",
        "indiaai.gov.in",
        "ycombinator.com",
        "inc42.com",
        "tracxn.com",
        "techcrunch.com",
        "economictimes.indiatimes.com",
        "livemint.com",
        "yourstory.com",
        "moneycontrol.com",
        "reuters.com",
    }

    blocked_domains = {
        "wikipedia.org",
        "medium.com",
        "linkedin.com",
        "facebook.com",
        "instagram.com",
        "youtube.com",
    }

    all_sources = []

    # Add general research sources

    for source in state.sources:

        source_copy = source.copy()

        source_copy["source_type"] = "general"

        all_sources.append(source_copy)

    # Add market research sources

    for source in state.market_sources:

        source_copy = source.copy()

        source_copy["source_type"] = "market"

        all_sources.append(source_copy)

    # Add company research sources

    for source in state.company_sources:

        source_copy = source.copy()

        source_copy["source_type"] = "company"

        all_sources.append(source_copy)

    # Remove duplicate URLs

    unique_sources = {}

    for source in all_sources:

        url = source.get("url", "").strip()

        if not url:
            continue

        if url not in unique_sources:

            unique_sources[url] = source

        else:

            existing_source = unique_sources[url]

            if (
                source.get("relevance_score", 0.0)
                >
                existing_source.get(
                    "relevance_score",
                    0.0
                )
            ):

                unique_sources[url] = source

    verified_sources = []

    for source in unique_sources.values():

        url = source.get("url", "").strip()

        relevance_score = source.get(
            "relevance_score",
            0.0
        )

        domain = get_domain(url)

        domain_trusted = any(
            domain == trusted_domain
            or domain.endswith(
                "." + trusted_domain
            )
            for trusted_domain in trusted_domains
        )

        domain_blocked = any(
            domain == blocked_domain
            or domain.endswith(
                "." + blocked_domain
            )
            for blocked_domain in blocked_domains
        )

        # Reject blocked domains

        if domain_blocked:
            continue

        source_quality_score = calculate_source_quality(
            relevance_score,
            domain_trusted
        )

        # Keep only sufficiently relevant sources

        if source_quality_score < 0.75:
            continue

        source["domain"] = domain

        source["domain_trusted"] = domain_trusted

        source["domain_blocked"] = domain_blocked

        source["source_quality_score"] = (
            source_quality_score
        )

        source["evidence_type"] = classify_evidence(
            source
        )

        source["verification_status"] = "verified"

        verified_sources.append(source)

    # Strongest sources first

    verified_sources.sort(
        key=lambda source: source[
            "source_quality_score"
        ],
        reverse=True
    )

    state.verified_sources = verified_sources

    return state