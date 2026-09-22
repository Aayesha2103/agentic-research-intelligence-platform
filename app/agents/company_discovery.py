from app.models.state import ResearchState
from app.services.llm import get_llm


CANONICAL_COMPANIES = {
    "sarvam ai": "Sarvam AI",
    "krutrim": "Krutrim",
    "krutrim ai": "Krutrim",
    "corover": "CoRover",
    "e42": "E42",
    "yellow.ai": "Yellow.ai",
    "yellow ai": "Yellow.ai",
    "uniphore": "Uniphore",
}


def normalize_company_name(
    company_name: str,
) -> str:

    cleaned = company_name.strip()

    # Remove common numbering produced by LLMs.
    cleaned = cleaned.lstrip(
        "0123456789.-) "
    )

    key = cleaned.lower()

    return CANONICAL_COMPANIES.get(
        key,
        cleaned,
    )


def normalize_companies(
    companies: list[str],
) -> list[str]:

    normalized = []

    for company in companies:

        company = normalize_company_name(
            company
        )

        if not company:
            continue

        if company not in normalized:
            normalized.append(
                company
            )

    return normalized


def company_discovery_node(
    state: ResearchState,
) -> dict:

    print()
    print(
        "===== COMPANY DISCOVERY INPUT ====="
    )

    sources = (
        state.sources
        + state.market_sources
        + state.company_sources
    )

    print(
        f"Number of research sources: "
        f"{len(sources)}"
    )

    print()

    print("Research source titles:")

    for source in sources:
        print(
            f"- {source.get('title', '')}"
        )

    print(
        "===== END COMPANY DISCOVERY INPUT ====="
    )
    print()

    if not sources:
        print(
            "No research sources available "
            "for company discovery."
        )

        return {
            "companies_to_research": []
        }

    evidence_text_parts = []

    for source in sources:

        company = source.get(
            "company",
            "",
        )

        title = source.get(
            "title",
            "",
        )

        content = source.get(
            "content",
            "",
        )

        evidence_text_parts.append(
            f"COMPANY: {company}\n"
            f"TITLE: {title}\n"
            f"CONTENT: {content}"
        )

    evidence_text = "\n\n".join(
        evidence_text_parts
    )

    prompt = f"""
You are the company discovery agent
for an Indian AI startup research platform.

User question:
{state.question}

Research evidence:
{evidence_text}

Identify the Indian AI startups or
AI-focused companies that should be
researched further.

Rules:

1. Use ONLY company names supported by
   the supplied research evidence.

2. Do not invent company names.

3. Do not include large traditional IT
   service companies such as Infosys,
   TCS, Wipro, Cognizant, or Bosch.

4. Return only company names.

5. Do not add explanations.

6. Do not add rankings.

7. Do not add scores.

8. Prefer the company's standard name.

9. If the evidence says "Krutrim AI",
   return "Krutrim".

10. Return one company per line.

Example:

Sarvam AI
Krutrim
CoRover
"""

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    text = response.content

    if not text:
        print(
            "Company discovery returned "
            "empty output."
        )

        return {
            "companies_to_research": []
        }

    print()
    print(
        "===== RAW COMPANY DISCOVERY RESPONSE ====="
    )

    print(text)

    print(
        "===== END RAW COMPANY DISCOVERY RESPONSE ====="
    )
    print()

    discovered_companies = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        company = normalize_company_name(
            line
        )

        if company not in discovered_companies:
            discovered_companies.append(
                company
            )

    discovered_companies = normalize_companies(
        discovered_companies
    )

    print(
        "Normalized discovered companies:"
    )

    for company in discovered_companies:
        print(
            f"- {company}"
        )

    print()

    return {
        "companies_to_research":
            discovered_companies
    }