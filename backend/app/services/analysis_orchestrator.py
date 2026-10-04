from bson import ObjectId

from .risk_categories import RISK_CATEGORIES
from .risk_analysis_service import analyze_website
from .analysis_service import save_analysis_findings
from .report_service import save_analysis_report


def run_website_analysis(
    website_id: ObjectId,
):
    print("========================================")
    print("POLICY ANALYSIS")
    print("========================================")

    print(
        "Website ID:",
        website_id
    )

    # -----------------------------------------
    # 1. Analyze risk categories
    # -----------------------------------------

    findings = analyze_website(
        website_id=website_id,
        categories=RISK_CATEGORIES,
    )

    # -----------------------------------------
    # 2. Save individual findings
    # -----------------------------------------

    print(
        "\nSaving analysis findings..."
    )

    saved_finding_ids = (
        save_analysis_findings(
            website_id=website_id,
            findings=findings,
        )
    )

    # -----------------------------------------
    # 3. Create analysis report
    # -----------------------------------------

    print(
        "\nCreating analysis report..."
    )

    report_id = save_analysis_report(
        website_id=website_id,
        findings=findings,
    )

    # -----------------------------------------
    # 4. Calculate status
    # -----------------------------------------

    successful_categories = [
        finding["category"]
        for finding in findings
        if finding["status"] == "analyzed"
    ]

    failed_categories = [
        finding["category"]
        for finding in findings
        if finding["status"] == "error"
    ]

    no_evidence_categories = [
        finding["category"]
        for finding in findings
        if finding["status"] == "no_evidence"
    ]

    return {
        "status": "completed",

        "report_id": report_id,

        "findings": findings,

        "saved_finding_ids": (
            saved_finding_ids
        ),

        "successful_categories": (
            successful_categories
        ),

        "failed_categories": (
            failed_categories
        ),

        "no_evidence_categories": (
            no_evidence_categories
        ),
    }
