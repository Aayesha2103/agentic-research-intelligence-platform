from app.models.state import ResearchState
from app.tools.web_search import (
    search_web,
    is_web_search_available,
)
from app.tools.demo_research import (
    get_demo_research_sources,
)
from app.utils.retry import retry


def market_research_node(
    state: ResearchState,
) -> dict:

    queries = [
        "current Indian AI startup ecosystem market trends",
        "latest Indian AI startup funding ecosystem",
        "India AI startup government initiatives policy support",
        "Indian AI startup market growth opportunities challenges",
    ]

    market_sources = []

    # --------------------------------------------------
    # Try live market research.
    # --------------------------------------------------

    if is_web_search_available():

        for query in queries:

            try:
                results = retry(
                    lambda q=query: search_web(q),
                    attempts=1,
                    delay=2.0,
                )

            except Exception as error:

                print(
                    f"Market research skipped for "
                    f"query '{query}': {error}"
                )

                continue

            for result in results:

                market_sources.append({
                    "title": result.get(
                        "title",
                        "",
                    ),
                    "url": result.get(
                        "url",
                        "",
                    ),
                    "content": result.get(
                        "content",
                        "",
                    ),
                    "relevance_score": result.get(
                        "relevance_score",
                        0.0,
                    ),
                    "query": query,
                })

            if not is_web_search_available():

                print(
                    "Stopping market research because "
                    "Tavily is unavailable."
                )

                break

    # --------------------------------------------------
    # Fall back to demo data.
    # --------------------------------------------------

    if not market_sources:

        print(
            "Using demo data for market research."
        )

        demo_sources = (
            get_demo_research_sources()
        )

        for source in demo_sources:

            market_sources.append({
                **source,
                "query": "demo market research",
            })

    print(
        f"Market research collected "
        f"{len(market_sources)} sources."
    )

    return {
        "market_sources": market_sources
    }