from urllib.parse import urlparse

from app.models.state import ResearchState


TRUSTED_DOMAINS = {
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


BLOCKED_DOMAINS = {
    "wikipedia.org",
    "medium.com",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
}


def get_domain(url: str) -> str:
    try:
        domain = urlparse(url).netloc.lower()
        return domain.removeprefix("www.")
    except Exception:
        return ""


def is_trusted_domain(domain: str) -> bool:
    return any(
        domain == trusted
        or domain.endswith(f".{trusted}")
        for trusted in TRUSTED_DOMAINS
    )


def is_blocked_domain(domain: str) -> bool:
    return any(
        domain == blocked
        or domain.endswith(f".{blocked}")
        for blocked in BLOCKED_DOMAINS
    )


def determine_evidence_type(source: dict) -> str:
    existing_type = source.get(
        "evidence_type",
        "",
    ).strip().lower()

    if existing_type:
        return existing_type

    query = source.get(
        "query",
        "",
    ).lower()

    if "fund" in query:
        return "funding"

    if "customer" in query or "client" in query:
        return "customer_traction"

    if "revenue" in query or "growth" in query:
        return "growth"

    if "product" in query or "technology" in query:
        return "product"

    if "market" in query or "opportunity" in query:
        return "market_opportunity"

    if (
        "differentiation" in query
        or "competitive" in query
    ):
        return "competitive_differentiation"

    return "general"


def source_key(source: dict) -> str:
    return source.get(
        "url",
        "",
    ).strip().lower()


def is_demo_source(
    source: dict,
    domain: str,
) -> bool:
    source_type = source.get(
        "source_type",
        "",
    ).strip().lower()

    url = source.get(
        "url",
        "",
    ).strip().lower()

    return (
        source_type == "demo"
        or domain == "example.com"
        or domain.endswith(".example.com")
        or "/demo/" in url
    )


def source_verifier_node(
    state: ResearchState,
) -> dict:

    print()
    print("===== SOURCE VERIFICATION =====")

    candidate_sources = (
        state.sources
        + state.market_sources
        + state.company_sources
    )

    unique_sources = {}

    for source in candidate_sources:
        url = source_key(source)

        if not url:
            continue

        if url not in unique_sources:
            unique_sources[url] = source

    verified_sources = []

    for source in unique_sources.values():

        url = source.get(
            "url",
            "",
        ).strip()

        content = source.get(
            "content",
            "",
        ).strip()

        if not url or not content:
            continue

        domain = get_domain(url)

        if not domain:
            continue

        # Demo sources are explicitly marked as demo.
        # They are kept for pipeline testing but are
        # never treated as real verified evidence.
        if is_demo_source(
            source,
            domain,
        ):
            verified_sources.append({
                **source,
                "source_type": "demo",
                "verification_status": "demo",
                "evidence_type": determine_evidence_type(
                    source
                ),
            })
            continue

        if is_blocked_domain(domain):
            continue

        if is_trusted_domain(domain):
            verification_status = "verified"
        else:
            verification_status = "unverified"

        verified_sources.append({
            **source,
            "source_type": "web",
            "verification_status": verification_status,
            "evidence_type": determine_evidence_type(
                source
            ),
        })

    real_verified_sources = [
        source
        for source in verified_sources
        if source.get(
            "verification_status"
        ) == "verified"
    ]

    demo_sources = [
        source
        for source in verified_sources
        if source.get(
            "verification_status"
        ) == "demo"
    ]

    unverified_web_sources = [
        source
        for source in verified_sources
        if (
            source.get("source_type") == "web"
            and source.get(
                "verification_status"
            ) == "unverified"
        )
    ]

    print(
        f"Candidate sources: "
        f"{len(candidate_sources)}"
    )

    print(
        f"Unique sources: "
        f"{len(unique_sources)}"
    )

    print(
        f"Verified web sources: "
        f"{len(real_verified_sources)}"
    )

    print(
        f"Demo sources: "
        f"{len(demo_sources)}"
    )

    print(
        f"Unverified web sources: "
        f"{len(unverified_web_sources)}"
    )

    print(
        "===== END SOURCE VERIFICATION ====="
    )
    print()

    return {
        "verified_sources": verified_sources
    }