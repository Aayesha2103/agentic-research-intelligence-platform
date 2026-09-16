from app.models.state import ResearchState


import re


def count_evidence(
    text: str,
    keywords: list[str]
) -> int:
    """
    Counts how many different evidence keywords
    are present in the supplied text.

    Whole-word matching is used so that a keyword
    does not accidentally match part of another word.
    """

    count = 0

    for keyword in keywords:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):
            count += 1

    return count

def company_qualification_node(
    state: ResearchState
) -> dict:
    """
    Company Qualification Agent.

    Uses deterministic evidence scoring to identify
    companies that are strong candidates for further research.
    """

    qualifications = []

    established_companies = {
        "infosys",
        "tcs",
        "tata consultancy services",
        "wipro",
        "cognizant",
        "bosch india",
    }

    ai_keywords = [
        "artificial intelligence",
        "ai company",
        "ai startup",
        "machine learning",
        "generative ai",
        "conversational ai",
        "computer vision",
        "natural language processing",
        "nlp",
        "robotics",
    ]

    startup_keywords = [
        "startup",
        "venture funding",
        "funding round",
        "raised",
        "investors",
        "backed by",
        "seed funding",
        "series a",
        "series b",
        "series c",
    ]

    indian_keywords = [
        "india",
        "indian",
        "india-based",
        "based in india",
        "headquartered in india",
        "founded in india",
    ]

    for company in state.companies_to_research:

        company_sources = [
            source
            for source in state.company_sources
            if source.get("company") == company
        ]

        evidence_text = ""

        for source in company_sources:

            evidence_text += (
                source.get("title", "")
                + " "
                + source.get("content", "")
                + " "
            )

        evidence_text = evidence_text.lower()

        company_name_lower = company.lower()

        is_established = (
            company_name_lower
            in established_companies
        )

        ai_evidence_count = count_evidence(
            evidence_text,
            ai_keywords
        )

        startup_evidence_count = count_evidence(
            evidence_text,
            startup_keywords
        )

        indian_evidence_count = count_evidence(
            evidence_text,
            indian_keywords
        )

        if is_established:

            qualifications.append(
                {
                    "company_name": company,
                    "is_ai_focused": False,
                    "is_indian": indian_evidence_count > 0,
                    "is_startup": False,
                    "ai_is_core_business": False,
                    "should_research": False,
                    "qualification_confidence": 0.98,
                    "reason": (
                        "Company is classified as an "
                        "established corporation rather "
                        "than an AI startup."
                    ),
                    "evidence": [
                        "Matched established-company exclusion rule."
                    ],
                }
            )

            continue

        has_strong_ai_evidence = (
            ai_evidence_count >= 2
        )

        has_strong_startup_evidence = (
            startup_evidence_count >= 2
        )

        has_indian_evidence = (
            indian_evidence_count >= 1
        )

        if (
            has_strong_ai_evidence
            and has_strong_startup_evidence
            and has_indian_evidence
        ):

            qualifications.append(
                {
                    "company_name": company,
                    "is_ai_focused": True,
                    "is_indian": True,
                    "is_startup": True,
                    "ai_is_core_business": True,
                    "should_research": True,
                    "qualification_confidence": 0.90,
                    "reason": (
                        "Multiple independent evidence indicators "
                        "support the company being an Indian "
                        "AI-focused startup."
                    ),
                    "evidence": [
                        (
                            f"AI evidence indicators: "
                            f"{ai_evidence_count}"
                        ),
                        (
                            f"Startup evidence indicators: "
                            f"{startup_evidence_count}"
                        ),
                        (
                            f"Indian connection indicators: "
                            f"{indian_evidence_count}"
                        ),
                    ],
                }
            )

            continue

        qualifications.append(
            {
                "company_name": company,
                "is_ai_focused": ai_evidence_count > 0,
                "is_indian": indian_evidence_count > 0,
                "is_startup": startup_evidence_count > 0,
                "ai_is_core_business": False,
                "should_research": False,
                "qualification_confidence": 0.55,
                "reason": (
                    "Available evidence is insufficient "
                    "to confidently qualify the company."
                ),
                "evidence": [
                    (
                        f"AI evidence indicators: "
                        f"{ai_evidence_count}"
                    ),
                    (
                        f"Startup evidence indicators: "
                        f"{startup_evidence_count}"
                    ),
                    (
                        f"Indian connection indicators: "
                        f"{indian_evidence_count}"
                    ),
                ],
            }
        )

    return {
        "company_qualifications": qualifications
    }