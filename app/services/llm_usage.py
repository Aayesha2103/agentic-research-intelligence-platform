from dataclasses import dataclass


@dataclass
class LLMUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


def extract_usage(response) -> LLMUsage:
    """Extract token usage from a LangChain LLM response."""

    usage = getattr(
        response,
        "usage_metadata",
        None,
    )

    if not usage:
        return LLMUsage()

    input_tokens = int(
        usage.get(
            "input_tokens",
            0,
        )
    )

    output_tokens = int(
        usage.get(
            "output_tokens",
            0,
        )
    )

    total_tokens = int(
        usage.get(
            "total_tokens",
            input_tokens + output_tokens,
        )
    )

    return LLMUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=0.0,
    )


def add_usage(
    current: LLMUsage,
    new: LLMUsage,
) -> LLMUsage:
    """Combine two LLM usage records."""

    return LLMUsage(
        input_tokens=(
            current.input_tokens
            + new.input_tokens
        ),
        output_tokens=(
            current.output_tokens
            + new.output_tokens
        ),
        total_tokens=(
            current.total_tokens
            + new.total_tokens
        ),
        estimated_cost_usd=(
            current.estimated_cost_usd
            + new.estimated_cost_usd
        ),
    )