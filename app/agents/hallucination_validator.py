import json

from app.models.state import ResearchState


def validate_report(state: ResearchState) -> dict:
    """
    Validates the generated report against trusted
    structured data already present in ResearchState.
    """

    if not state.final_report:
        print(
            "No final report available for validation."
        )

        return {}


    # --------------------------------------------------
    # Parse the synthesizer output.
    # --------------------------------------------------

    try:
        report = json.loads(
            state.final_report
        )

    except json.JSONDecodeError:
        print(
            "Hallucination validator: "
            "report is not valid JSON."
        )

        return {
            "final_report": state.final_report
        }


    # --------------------------------------------------
    # Build trusted score lookup.
    # --------------------------------------------------

    scored_companies = {
        item.get("company_name", item.get("company", "")):
            item["overall_score"]
        for item in state.company_scores
    }


    # --------------------------------------------------
    # Store validation issues.
    # --------------------------------------------------

    issues = []


    # --------------------------------------------------
    # Check 1:
    # Every reported company must have been scored.
    # --------------------------------------------------

    for company in report.get(
        "companies",
        []
    ):

        company_name = company.get(
            "company_name",
            ""
        )

        if company_name not in scored_companies:

            issues.append(
                "Unsupported company in report: "
                f"{company_name}"
            )


    # --------------------------------------------------
    # Check 2:
    # Reported scores must match deterministic scores.
    # --------------------------------------------------

    for company in report.get(
        "companies",
        []
    ):

        company_name = company.get(
            "company_name",
            ""
        )

        if company_name in scored_companies:

            expected_score = (
                scored_companies[
                    company_name
                ]
            )

            reported_score = company.get(
                "overall_score"
            )

            if reported_score != expected_score:

                issues.append(
                    f"Score mismatch for "
                    f"{company_name}: "
                    f"expected {expected_score}, "
                    f"got {reported_score}"
                )


    # --------------------------------------------------
    # Check 3:
    # Every company must belong to the
    # original research plan.
    # --------------------------------------------------

    researched_companies = set(
        state.companies_to_research
    )

    for company in report.get(
        "companies",
        []
    ):

        company_name = company.get(
            "company_name",
            ""
        )

        if company_name not in researched_companies:

            issues.append(
                "Company was not part of "
                "the research plan: "
                f"{company_name}"
            )


    # --------------------------------------------------
    # Determine validation status.
    # --------------------------------------------------

    validation_status = (
        "passed"
        if not issues
        else "needs_review"
    )


    # --------------------------------------------------
    # Add validation information to report.
    # --------------------------------------------------

    report["validation"] = {
        "status": validation_status,
        "issues": issues,
        "hallucination_check": (
            validation_status == "passed"
        ),
    }


    # --------------------------------------------------
    # Print validation results.
    # --------------------------------------------------

    print()
    print(
        "===== HALLUCINATION VALIDATION ====="
    )

    print(
        f"Status: {validation_status}"
    )

    if issues:

        print("Issues:")

        for issue in issues:
            print(
                f"- {issue}"
            )

    else:

        print(
            "No structural hallucination "
            "issues detected."
        )

    print(
        "===================================="
    )

    print()


    # --------------------------------------------------
    # Return updated report.
    # --------------------------------------------------

    return {
        "final_report": json.dumps(
            report,
            indent=2
        )
    }