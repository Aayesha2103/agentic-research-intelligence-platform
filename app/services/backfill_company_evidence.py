import httpx

from app.services.evidence_extractor import TARGET_COMPANIES
from app.services.evidence_extractor import extract_company_evidence
from app.services.supabase_client import (
    get_supabase_headers,
    get_supabase_url,
)
from app.services.rag_store import store_research_document


def get_general_documents() -> list[dict]:
    """
    Retrieves existing general research documents
    from Supabase.
    """

    url = (
        f"{get_supabase_url()}"
        "/rest/v1/research_documents"
    )

    params = {
        "company_name": "eq.",
        "select": "id,content,source_url,"
        "source_title,evidence_type",
        "order": "id.asc",
    }

    response = httpx.get(
        url,
        headers=get_supabase_headers(),
        params=params,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()


def company_document_exists(
    source_url: str,
    company_name: str,
) -> bool:
    """
    Checks whether company-specific evidence
    has already been stored.
    """

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


def backfill_company_evidence() -> None:
    """
    Extracts company-specific evidence from existing
    general documents and stores it in the RAG database.
    """

    documents = get_general_documents()

    created = 0
    skipped = 0

    print()
    print("===== COMPANY EVIDENCE BACKFILL =====")
    print(f"General documents found: {len(documents)}")
    print()

    for document in documents:

        content = document.get(
            "content",
            "",
        ).strip()

        source_url = document.get(
            "source_url",
            "",
        ).strip()

        source_title = document.get(
            "source_title",
            "",
        ).strip()

        evidence_type = document.get(
            "evidence_type",
            "general",
        )

        if not content or not source_url:
            continue

        for company in TARGET_COMPANIES:

            evidence = extract_company_evidence(
                content,
                company,
            )

            if not evidence:
                continue

            if company_document_exists(
                source_url,
                company,
            ):
                skipped += 1
                continue

            store_research_document(
                content=evidence,
                source_url=source_url,
                source_title=source_title,
                company_name=company,
                evidence_type=evidence_type,
            )

            created += 1

            print(
                f"Indexed: {company} | "
                f"{source_title}"
            )

    print()
    print(f"Company-specific documents created: {created}")
    print(f"Company-specific documents skipped: {skipped}")
    print("===== END COMPANY EVIDENCE BACKFILL =====")
    print()


if __name__ == "__main__":
    backfill_company_evidence()