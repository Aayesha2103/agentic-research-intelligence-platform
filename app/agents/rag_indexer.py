from app.models.state import ResearchState
from app.services.embeddings import create_embedding
from app.services.supabase_client import (
    insert_research_document,
    research_document_exists,
)


def normalize_company_name(company_name: str) -> str:
    """
    Normalizes company names for consistent storage.
    """

    return company_name.strip()


def clean_content(content: str) -> str:
    """
    Removes unnecessary whitespace from source content.
    """

    return " ".join(
        content.strip().split()
    )


def determine_evidence_type(source: dict) -> str:
    """
    Determines the main type of evidence represented
    by a source.
    """

    evidence_type = source.get(
        "evidence_type",
        ""
    ).strip().lower()

    if evidence_type:
        return evidence_type

    query = source.get(
        "query",
        ""
    ).lower()

    if "fund" in query:
        return "funding"

    if (
        "customer" in query
        or "client" in query
    ):
        return "customer_traction"

    if (
        "revenue" in query
        or "growth" in query
    ):
        return "growth"

    if (
        "product" in query
        or "technology" in query
    ):
        return "product"

    if (
        "market" in query
        or "opportunity" in query
    ):
        return "market_opportunity"

    if (
        "differentiation" in query
        or "competitive" in query
    ):
        return "competitive_differentiation"

    return "general"


def prepare_document(source: dict) -> dict | None:
    """
    Converts a verified source into a clean RAG document.
    """

    company_name = normalize_company_name(
        source.get(
            "company",
            source.get(
                "company_name",
                ""
            ),
        )
    )

    title = source.get(
        "title",
        source.get(
            "source_title",
            "",
        ),
    ).strip()

    url = source.get(
        "url",
        source.get(
            "source_url",
            "",
        ),
    ).strip()

    content = clean_content(
        source.get(
            "content",
            "",
        )
    )

    if not company_name:
        return None

    if not title:
        return None

    if not url:
        return None

    if not content:
        return None

    return {
        "content": content,
        "source_url": url,
        "source_title": title,
        "company_name": company_name,
        "evidence_type": determine_evidence_type(
            source
        ),
        "embedding": create_embedding(
            content
        ),
    }


def rag_indexer_node(
    state: ResearchState,
) -> dict:
    """
    Indexes verified research sources into
    Supabase + pgvector.
    """

    indexed_count = 0
    skipped_duplicates = 0
    skipped_invalid = 0

    print()

    print("===== RAG INDEXING =====")

    for source in state.verified_sources:

        document = prepare_document(
            source
        )

        if document is None:
            skipped_invalid += 1
            continue

        exists = research_document_exists(
            source_url=document["source_url"],
            company_name=document[
                "company_name"
            ],
        )

        if exists:
            skipped_duplicates += 1
            continue

        insert_research_document(
            document
        )

        indexed_count += 1

    print(
        f"RAG indexed documents: {indexed_count}"
    )

    print(
        f"RAG skipped duplicates: "
        f"{skipped_duplicates}"
    )

    print(
        f"RAG skipped invalid sources: "
        f"{skipped_invalid}"
    )

    print(
        "===== END RAG INDEXING ====="
    )

    print()

    return {}