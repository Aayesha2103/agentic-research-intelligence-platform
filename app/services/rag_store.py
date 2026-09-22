from app.services.embeddings import create_embedding
from app.services.supabase_client import insert_research_document


def store_research_document(
    content: str,
    source_url: str = "",
    source_title: str = "",
    company_name: str = "",
    evidence_type: str = "",
) -> dict:
    embedding = create_embedding(content)

    document = {
        "content": content,
        "source_url": source_url,
        "source_title": source_title,
        "company_name": company_name,
        "evidence_type": evidence_type,
        "embedding": embedding,
    }

    return insert_research_document(document)