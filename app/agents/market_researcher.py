from app.models.state import ResearchState
from app.tools.web_search import search_web


def market_research_node(state: ResearchState) -> dict:
    """
    Market Research Agent.

    Researches the overall Indian AI startup market,
    including market trends, ecosystem growth,
    government support, and major opportunities.
    """

    queries = [
        "current Indian AI startup ecosystem market trends",
        "latest Indian AI startup funding ecosystem",
        "India AI startup government initiatives policy support",
        "Indian AI startup market growth opportunities challenges",
    ]

    market_sources = []

    for query in queries:
        response = search_web(query)

        for result in response.get("results", []):
            market_sources.append(
                {
                    "query": query,
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "relevance_score": result.get("score", 0.0),
                }
            )

    return {
        "market_sources": market_sources
    }