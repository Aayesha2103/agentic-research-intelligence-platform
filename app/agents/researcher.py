from app.models.state import ResearchState
from app.tools.web_search import (
    search_web,
    is_web_search_available,
)
from app.tools.demo_research import (
    get_demo_research_sources,
)
from app.utils.retry import retry


def web_research_node(
    state: ResearchState,
) -> dict:

    sources = []

    # --------------------------------------------------
    # Try live Tavily research first.
    # --------------------------------------------------

    if is_web_search_available():

        for query in state.search_queries:

            try:
                results = retry(
                    lambda q=query: search_web(q),
                    attempts=1,
                    delay=2.0,
                )

            except Exception as error:

                print(
                    f"Web research skipped for "
                    f"query '{query}': {error}"
                )

                continue

            for result in results:

                sources.append({
                    "query": query,
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
                })

            if not is_web_search_available():

                print(
                    "Stopping web research because "
                    "Tavily is unavailable."
                )

                break

    # --------------------------------------------------
    # Fall back to local demo data.
    # --------------------------------------------------

    if not sources:

        print(
            "Using local demo research data "
            "because live web research is unavailable."
        )

        sources = get_demo_research_sources()

    print(
        f"Web research collected "
        f"{len(sources)} sources."
    )

    return {
        "sources": sources
    }