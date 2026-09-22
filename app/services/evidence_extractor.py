import re


TARGET_COMPANIES = [
    "Sarvam AI",
    "Krutrim",
    "CoRover",
    "E42",
    "Yellow.ai",
    "Uniphore",
]


def extract_company_evidence(
    content: str,
    company_name: str,
) -> str:
    """
    Extracts sentences from a source that explicitly
    mention the requested company.
    """

    if not content or not company_name:
        return ""

    # Normalize whitespace so sentences are easier to process.
    normalized_content = re.sub(
        r"\s+",
        " ",
        content,
    ).strip()

    # Split the document into sentence-like units.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        normalized_content,
    )

    company_evidence = []

    company_lower = company_name.lower()

    for sentence in sentences:

        if company_lower in sentence.lower():

            sentence = sentence.strip()

            if sentence and sentence not in company_evidence:
                company_evidence.append(sentence)

    return " ".join(company_evidence)
