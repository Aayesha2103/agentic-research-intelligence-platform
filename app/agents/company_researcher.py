from app.models.state import ResearchState
from app.tools.web_search import search_web, is_web_search_available
from app.utils.retry import retry


def company_research_node(state: ResearchState) -> dict:
    if not is_web_search_available():
        print("Company research skipped: Tavily is unavailable.")
        return {"company_sources": []}

    company_sources = []

    for company in state.companies_to_research:
        queries = [
            f"{company} India AI startup product customers",
            f"{company} India AI startup funding investors growth",
        ]

        for query in queries:
            try:
                results = retry(
                    lambda q=query: search_web(q),
                    attempts=1,
                    delay=2.0,
                )
            except Exception as error:
                print(
                    f"Company research skipped for "
                    f"{company}, query '{query}': {error}"
                )
                continue

            for result in results:
                company_sources.append(
                    {
                        "company": company,
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "relevance_score": result.get(
                            "relevance_score",
                            0.0,
                        ),
                        "query": query,
                    }
                )

            if not is_web_search_available():
                print(
                    "Stopping company research because "
                    "Tavily is unavailable."
                )
                return {"company_sources": company_sources}

    print(
        f"Company research collected "
        f"{len(company_sources)} sources."
    )

    return {"company_sources": company_sources}