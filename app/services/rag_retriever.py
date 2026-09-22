import httpx

from app.services.embeddings import create_embedding
from app.services.supabase_client import (
    get_supabase_headers,
    get_supabase_url,
)


def retrieve_research_documents(
    query: str,
    match_count: int = 5,
) -> list[dict]:
    """
    Performs semantic similarity search against
    the Supabase pgvector database.
    """

    # Convert the search query into an embedding.
    query_embedding = create_embedding(query)

    # Supabase RPC endpoint.
    url = (
        f"{get_supabase_url()}"
        "/rest/v1/rpc/match_research_documents"
    )

    # Authentication headers.
    headers = get_supabase_headers()

    headers["Accept"] = "application/json"

    # Call the PostgreSQL/pgvector RPC function.
    response = httpx.post(
        url,
        headers=headers,
        json={
            "query_embedding": query_embedding,
            "match_count": match_count,
        },
        timeout=30.0,
    )

    # Give a clear error if authentication fails.
    if response.status_code == 401:
        raise RuntimeError(
            "Supabase RPC authentication failed. "
            "Check SUPABASE_SECRET_KEY."
        )

    # Raise an exception for other HTTP errors.
    response.raise_for_status()

    # Return the matched documents.
    return response.json()