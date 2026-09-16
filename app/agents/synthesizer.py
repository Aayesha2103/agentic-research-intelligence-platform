from app.models.state import ResearchState
from app.models.report import ResearchReport
from app.services.llm import get_llm


def synthesizer_node(
    state: ResearchState
) -> dict:
    """
    Report Synthesizer Agent.

    Combines verified research evidence and company scores
    into a structured final research report.
    """

    llm = get_llm()

    report_llm = llm.with_structured_output(
        ResearchReport
    )

    company_scores_text = ""

    for score in state.company_scores:

        company_scores_text += (
            f"Company: {score.get('company_name', '')}\n"
            f"Funding score: "
            f"{score.get('funding_score', 0)}\n"
            f"Product score: "
            f"{score.get('product_score', 0)}\n"
            f"Customer score: "
            f"{score.get('customer_score', 0)}\n"
            f"Growth score: "
            f"{score.get('growth_score', 0)}\n"
            f"Market score: "
            f"{score.get('market_score', 0)}\n"
            f"Competitive score: "
            f"{score.get('competitive_score', 0)}\n"
            f"Overall score: "
            f"{score.get('overall_score', 0)}\n"
            f"Reasoning: "
            f"{score.get('reasoning', '')}\n\n"
        )

    market_evidence_text = ""

    for source in state.verified_sources:

        if source.get("source_type") == "market":

            market_evidence_text += (
                f"Title: {source.get('title', '')}\n"
                f"URL: {source.get('url', '')}\n"
                f"Evidence type: "
                f"{source.get('evidence_type', '')}\n"
                f"Content: "
                f"{source.get('content', '')}\n\n"
            )

    company_evidence_text = ""

    for source in state.verified_sources:

        if source.get("source_type") == "company":

            company_evidence_text += (
                f"Company: "
                f"{source.get('company', '')}\n"
                f"Title: {source.get('title', '')}\n"
                f"URL: {source.get('url', '')}\n"
                f"Evidence type: "
                f"{source.get('evidence_type', '')}\n"
                f"Content: "
                f"{source.get('content', '')}\n\n"
            )

    report = report_llm.invoke(
        f"""
        Create a structured research report for this question:

        {state.question}

        MARKET EVIDENCE:
        {market_evidence_text}

        COMPANY EVIDENCE:
        {company_evidence_text}

        COMPANY SCORES:
        {company_scores_text}

        IMPORTANT RULES:

        1. Base the report only on the supplied evidence.

        2. Do not invent funding amounts, customers,
           revenue, valuations, products, or market statistics.

        3. Do not treat an overall score as an objective
           prediction of future success.

        4. Explain why companies received their scores
           using the available evidence.

        5. Clearly identify important risks and evidence gaps.

        6. The executive summary should answer the user's
           research question directly.

        7. The market overview should summarize the
           Indian AI startup ecosystem using the supplied
           market evidence.

        8. Include only companies for which company scores
           are available.

        9. The methodology should explain that the system:

           - discovered companies through web research,
           - qualified companies using evidence,
           - verified sources,
           - scored companies across multiple dimensions,
           - and synthesized the findings.

        10. The limitations section should mention
            meaningful limitations in the available evidence.

        11. Keep the report concise but informative.

        Return the result using the ResearchReport schema.
        """
    )

    return {
        "final_report": report.model_dump_json(
            indent=2
        )
    }