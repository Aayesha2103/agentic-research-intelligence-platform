from typing import Annotated

from pydantic import BaseModel, Field


def merge_lists(existing: list, new: list) -> list:
    """
    Merges two lists together.
    """
    return existing + new


def merge_unique_strings(
    existing: list[str],
    new: list[str]
) -> list[str]:
    """
    Merges string lists while removing duplicates.
    """
    result = existing.copy()

    for item in new:
        if item not in result:
            result.append(item)

    return result


class ResearchState(BaseModel):

    question: str

    research_topics: list[str] = Field(
        default_factory=list
    )

    companies_to_research: Annotated[
        list[str],
        merge_unique_strings
    ] = Field(
        default_factory=list
    )

    search_queries: list[str] = Field(
        default_factory=list
    )

    market_sources: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    company_sources: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    funding_sources: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    sources: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    verified_sources: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    retrieved_documents: list[dict] = Field(
        default_factory=list
    )

    company_qualifications: list[dict] = Field(
        default_factory=list
    )

    company_scores: Annotated[
        list[dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    final_report: str = ""

    confidence_score: float = 0.0

    total_cost_usd: float = 0.0

    total_latency_seconds: float = 0.0