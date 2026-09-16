from pydantic import BaseModel, Field


class CompanyQualification(BaseModel):
    """
    Structured qualification result for an AI company candidate.
    """

    company_name: str = Field(
        description="Name of the company being evaluated."
    )

    is_ai_focused: bool = Field(
        description=(
            "Whether AI is a central part of the company's "
            "primary product or business."
        )
    )

    is_indian: bool = Field(
        description=(
            "Whether the company is based in India or is "
            "meaningfully an Indian AI company."
        )
    )

    is_startup: bool = Field(
        description=(
            "Whether the company should reasonably be considered "
            "a startup rather than a large established corporation."
        )
    )

    ai_is_core_business: bool = Field(
        description=(
            "Whether AI is fundamental to the company's primary "
            "product or business rather than merely being used internally."
        )
    )

    should_research: bool = Field(
        description=(
            "Whether this company should remain in the research set "
            "for further analysis."
        )
    )

    qualification_confidence: float = Field(
        description=(
            "Confidence in the qualification decision, from 0.0 to 1.0."
        )
    )

    reason: str = Field(
        description=(
            "Short explanation of why the company was qualified "
            "or rejected."
        )
    )

    evidence: list[str] = Field(
        description=(
            "Important evidence from the collected research sources "
            "that supports the qualification decision."
        )
    )