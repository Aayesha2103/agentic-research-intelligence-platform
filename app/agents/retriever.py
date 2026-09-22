from concurrent.futures import ThreadPoolExecutor, as_completed

from app.models.state import ResearchState
from app.services.rag_retriever import retrieve_research_documents


def retrieve_for_company(company: str) -> list[dict]:
    """
    Retrieves relevant RAG documents for one company
    using a single combined semantic query.
    """

    query = (
        f"{company} funding investors "
        f"products technology customers "
        f"growth"
    )

    results = retrieve_research_documents(
        query=query,
        match_count=8,
    )

    company_documents = []
    seen_urls = set()

    for document in results:
        source_url = document.get("source_url", "")

        if not source_url:
            continue

        stored_company = document.get(
            "company_name",
            "",
        ).strip()

        # Keep only documents explicitly tagged
        # with the company being researched.
        if stored_company.lower() != company.lower():
            continue

        # Avoid duplicate sources.
        if source_url in seen_urls:
            continue

        seen_urls.add(source_url)

        # Normalize the company name.
        document["company_name"] = company

        company_documents.append(document)

    return company_documents


def retriever_node(state: ResearchState) -> dict:
    """
    Retrieves RAG documents for all planned companies
    in parallel.
    """

    companies = state.companies_to_research

    if not companies:
        return {
            "retrieved_documents": []
        }

    documents = []

    # Run company retrieval concurrently.
    with ThreadPoolExecutor(
        max_workers=min(len(companies), 6)
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
                company_documents = future.result()

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
        f"company-tagged documents: {len(documents)}"
    )

    return {
        "retrieved_documents": documents
    }