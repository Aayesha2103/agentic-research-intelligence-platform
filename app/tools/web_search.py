import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


def search_web(query: str):
    """
    Searches the web using Tavily and returns search results.
    """

    client = TavilyClient(
        api_key=os.getenv("TAVILY_API_KEY")
    )

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    return response