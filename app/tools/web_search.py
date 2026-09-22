import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

_tavily_unavailable = False


def is_web_search_available() -> bool:
    """Return whether Tavily is available for this run."""
    return not _tavily_unavailable


def search_web(query: str) -> list[dict]:
    """
    Search the web using Tavily.

    Returns a list of normalized Tavily search results.
    """

    global _tavily_unavailable

    if _tavily_unavailable:
        return []

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print(
            "Tavily error: TAVILY_API_KEY is not configured."
        )
        _tavily_unavailable = True
        return []

    try:

        client = TavilyClient(
            api_key=api_key
        )

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
        )

        results = response.get(
            "results",
            [],
        )

        normalized_results = []

        for result in results:

            normalized_results.append(
                {
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
                        "score",
                        result.get(
                            "relevance_score",
                            0.0,
                        ),
                    ),
                }
            )

        return normalized_results

    except Exception as error:

        error_message = str(error).lower()

        if (
            "usage limit" in error_message
            or "quota" in error_message
            or "forbidden" in error_message
            or "upgrade your plan" in error_message
            or "plan's set usage limit" in error_message
        ):

            print(
                "Tavily quota/plan limit reached."
            )

        elif (
            "401" in error_message
            or "unauthorized" in error_message
            or "invalid api key" in error_message
        ):

            print(
                "Tavily authentication failed. "
                "Check TAVILY_API_KEY."
            )

        else:

            print(
                f"Tavily search error: {error}"
            )

        _tavily_unavailable = True

        return []