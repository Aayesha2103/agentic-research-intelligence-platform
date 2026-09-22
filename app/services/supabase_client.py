import os

import httpx

from dotenv import load_dotenv


load_dotenv()


def get_supabase_headers() -> dict:
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
    url = os.getenv("SUPABASE_URL")

    if not url:
        raise ValueError(
            "SUPABASE_URL is not configured."
        )

    return url


def research_document_exists(
    source_url: str,
    company_name: str = "",
) -> bool:

    if not source_url:
        return False

    url = (
        f"{get_supabase_url()}"
        "/rest/v1/research_documents"
    )

    params = {
        "source_url": f"eq.{source_url}",
        "company_name": f"eq.{company_name}",
        "select": "id",
        "limit": 1,
    }

    response = httpx.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=30.0,
    )

    response.raise_for_status()

    return len(response.json()) > 0


def insert_research_document(
    document: dict,
) -> dict:

    url = (
        f"{get_supabase_url()}"
        "/rest/v1/research_documents"
    )

    headers = {
        **get_supabase_headers(),
        "Prefer": "return=representation",
    }

    response = httpx.post(
        url,
        headers=headers,
        json=document,
        timeout=30.0,
    )

    response.raise_for_status()

    if not response.content:
        return {"status": "inserted"}

    return response.json()