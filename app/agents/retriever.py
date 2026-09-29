from concurrent.futures import ThreadPoolExecutor, as_completed

from app.models.state import ResearchState
from app.services.rag_retriever import retrieve_research_documents


# Keep local embedding work deliberately limited.
# Six concurrent BGE-M3 embedding calls can create a
# large CPU/GPU spike on a laptop.
MAX_RETRIEVAL_WORKERS = 2


def retrieve_for_company(
    company: str,
) -> list[dict]:

    query = (
        f"{company} funding investors products "
        f"technology customers growth"
    )

    results = retrieve_research_documents(
        query=query,
        match_count=6,
    )

    company_documents = []
    seen_urls = set()

    for document in results:

        source_url = document.get(
            "source_url",
            "",
        )

        if not source_url:
            continue

        stored_company = document.get(
            "company_name",
            "",
        ).strip()

        if stored_company.lower() != company.lower():
            continue

        if source_url in seen_urls:
            continue

        seen_urls.add(source_url)

        document["company_name"] = company

        company_documents.append(
            document
        )

    return company_documents


def retriever_node(
    state: ResearchState,
) -> dict:

    companies = state.companies_to_research

    if not companies:
        return {
            "retrieved_documents": []
        }

    documents = []

    worker_count = min(
        len(companies),
        MAX_RETRIEVAL_WORKERS,
    )

    with ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:

        futures = {
            executor.submit(
                retrieve_for_company,
                company,
            ): company
            for company in companies
        }

        for future in as_completed(futures):

            company = futures[future]

            try:
                company_documents = (
                    future.result()
                )

                documents.extend(
                    company_documents
                )

            except Exception as error:
                print(
                    f"RAG retrieval failed for "
                    f"{company}: {error}"
                )

    print(
        "RAG retrieved explicitly "
        "company-tagged documents: "
        f"{len(documents)}"
    )

    return {
        "retrieved_documents": documents
    }
