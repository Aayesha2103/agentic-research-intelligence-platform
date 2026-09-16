from typing import Annotated, List, Dict

from pydantic import BaseModel, Field


def merge_lists(
    existing: List[Dict],
    new: List[Dict]
) -> List[Dict]:
    """
    Merges list-based results from parallel LangGraph nodes.
    """

    return existing + new


def merge_unique_strings(
    existing: List[str],
    new: List[str]
) -> List[str]:
    """
    Merges string lists while removing duplicates.
    """

    result = existing.copy()

    for item in new:
        if item not in result:
            result.append(item)

    return result


class ResearchState(BaseModel):
    """
    Shared state that travels through the LangGraph workflow.
    Every node reads from it and writes back to it.
    """

    question: str

    research_topics: List[str] = Field(
        default_factory=list
    )

    companies_to_research: Annotated[
        List[str],
        merge_unique_strings
    ] = Field(
        default_factory=list
    )

    search_queries: List[str] = Field(
        default_factory=list
    )

    market_sources: Annotated[
        List[Dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    company_sources: Annotated[
        List[Dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    funding_sources: Annotated[
        List[Dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    sources: Annotated[
        List[Dict],
        merge_lists
    ] = Field(
        default_factory=list
    )

    verified_sources: List[Dict] = Field(
        default_factory=list
    )

    company_qualifications: List[Dict] = Field(
        default_factory=list
    )

    company_scores: List[Dict] = Field(
        default_factory=list
    )

    company_scores: List[Dict] = Field(
        default_factory=list
    )

    final_report: str = ""

    confidence_score: float = 0.0

    total_cost_usd: float = 0.0

    total_latency_seconds: float = 0.0