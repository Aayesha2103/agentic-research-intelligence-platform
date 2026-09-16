from app.models.state import ResearchState
from app.tools.web_search import search_web


def web_research_node(state: ResearchState) -> dict:
    """
    Web Research Agent.

    Executes the search queries created by the Planner
    and returns the collected company/startup research sources.
    """

    all_sources = []

    for query in state.search_queries:
        response = search_web(query)

        for result in response.get("results", []):
            all_sources.append(
                {
                    "query": query,
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "relevance_score": result.get("score", 0.0),
                }
            )

    return {
        "sources": all_sources
    }