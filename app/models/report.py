from pydantic import BaseModel, Field


class CompanyRecommendation(BaseModel):
    """
    Structured recommendation for one company.
    """

    company_name: str

    overall_score: float = Field(
        ge=0,
        le=10
    )

    key_strengths: list[str]

    key_risks: list[str]

    evidence_summary: str


class ResearchReport(BaseModel):
    """
    Structured final research report.
    """

    title: str

    executive_summary: str

    market_overview: str

    companies: list[CompanyRecommendation]

    methodology: str

    limitations: list[str]