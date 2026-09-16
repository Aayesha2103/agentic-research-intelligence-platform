from app.models.state import ResearchState
from app.tools.web_search import search_web


def company_research_node(state: ResearchState) -> dict:
    """
    Company Research Agent.

    Researches individual companies identified by the Planner.
    """

    company_sources = []

    for company in state.companies_to_research:

        queries = [
            f"{company} India AI startup company product",
            f"{company} funding investors",
            f"{company} customers partnerships AI",
        ]

        for query in queries:
            response = search_web(query)

            for result in response.get("results", []):
                company_sources.append(
                    {
                        "company": company,
                        "query": query,
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "relevance_score": result.get(
                            "score",
                            0.0
                        ),
                    }
                )

    return {
        "company_sources": company_sources
    }