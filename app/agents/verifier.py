from urllib.parse import urlparse

from app.models.state import ResearchState


def classify_evidence(source: dict) -> str:
    """
    Classifies a source according to the type of evidence
    it most likely contains.

    Search query and title are given higher priority
    than the full article content.
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

    content_keywords = {
        "funding": [
            "funding round",
            "raised",
            "investment",
            "investor",
        ],
        "customers": [
            "customer",
            "client",
            "partnership",
            "deployment",
        ],
        "product": [
            "product launch",
            "ai platform",
            "machine learning platform",
            "technology",
        ],
        "policy": [
            "government policy",
            "government initiative",
            "regulation",
            "ministry",
        ],
        "market": [
            "market size",
            "startup ecosystem",
            "industry growth",
        ],
        "growth": [
            "revenue growth",
            "user growth",
            "business growth",
        ],
    }

    for evidence_type, keywords in content_keywords.items():
        if any(keyword in content for keyword in keywords):
            return evidence_type

    return "general"


def source_verifier_node(state: ResearchState) -> ResearchState:
    """
    Source Verification Agent.

    Combines sources collected by all research agents
    and evaluates their quality using:
    - search relevance
    - domain trust
    - blocked-source rules
    - evidence classification
    - URL-based deduplication

    The strongest sources are kept and ranked first.
    """

    verified_sources = []

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

    for source in state.sources:
        source_copy = source.copy()
        source_copy["source_type"] = "general"
        all_sources.append(source_copy)

    for source in state.market_sources:
        source_copy = source.copy()
        source_copy["source_type"] = "market"
        all_sources.append(source_copy)

    for source in state.company_sources:
        source_copy = source.copy()
        source_copy["source_type"] = "company"
        all_sources.append(source_copy)

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
                > existing_source.get("relevance_score", 0.0)
            ):
                unique_sources[url] = source

    for source in unique_sources.values():
        url = source.get("url", "")
        relevance_score = source.get("relevance_score", 0.0)

        parsed_url = urlparse(url)

        hostname = parsed_url.hostname or ""
        hostname = hostname.lower()

        domain_trusted = any(
            hostname == domain
            or hostname.endswith("." + domain)
            for domain in trusted_domains
        )

        domain_blocked = any(
            hostname == domain
            or hostname.endswith("." + domain)
            for domain in blocked_domains
        )

        if domain_blocked:
            continue

        source_quality_score = relevance_score

        if domain_trusted:
            source_quality_score += 0.10

        if source_quality_score < 0.75:
            continue

        source["domain_trusted"] = domain_trusted
        source["domain_blocked"] = domain_blocked
        source["source_quality_score"] = min(
            source_quality_score,
            1.0
        )

        source["evidence_type"] = classify_evidence(source)

        verified_sources.append(source)

    verified_sources.sort(
        key=lambda source: source["source_quality_score"],
        reverse=True
    )

    state.verified_sources = verified_sources

    return state