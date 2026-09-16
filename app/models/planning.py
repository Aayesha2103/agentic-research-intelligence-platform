from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    """
    Structured research plan produced by the planning agent.
    """

    research_topics: list[str] = Field(
        description="Major topics that should be investigated."
    )

    companies_to_research: list[str] = Field(
        description="Companies that should be investigated."
    )

    search_queries: list[str] = Field(
        description="Search queries needed to gather evidence."
    )