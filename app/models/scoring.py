from pydantic import BaseModel, Field


class CompanyScore(BaseModel):
    """
    Structured score for an AI startup based on
    verified research evidence.
    """

    company_name: str

    funding_score: float = Field(
        ge=0,
        le=10
    )

    product_score: float = Field(
        ge=0,
        le=10
    )

    customer_score: float = Field(
        ge=0,
        le=10
    )

    growth_score: float = Field(
        ge=0,
        le=10
    )

    market_score: float = Field(
        ge=0,
        le=10
    )

    competitive_score: float = Field(
        ge=0,
        le=10
    )

    overall_score: float = Field(
        ge=0,
        le=10
    )

    reasoning: str