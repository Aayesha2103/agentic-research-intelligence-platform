import os

import httpx
from dotenv import load_dotenv


load_dotenv()


def get_supabase_headers() -> dict:
    """
    Creates the HTTP headers required to communicate
    with the Supabase Data API.
    """

    secret_key = os.getenv("SUPABASE_SECRET_KEY")

    if not secret_key:
        raise ValueError(
            "SUPABASE_SECRET_KEY is not configured."
        )

    return {
        "apikey": secret_key,
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }


def get_supabase_url() -> str:
    """
    Returns the Supabase project URL.
    """

    url = os.getenv("SUPABASE_URL")

    if not url:
        raise ValueError(
            "SUPABASE_URL is not configured."
        )

    return url


def insert_research_document(document: dict) -> dict:
    """
    Inserts one research document into the
    research_documents table.
    """

    url = (
        f"{get_supabase_url()}"
        "/rest/v1/research_documents"
    )

    response = httpx.post(
        url,
        headers=get_supabase_headers(),
        json=document,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()