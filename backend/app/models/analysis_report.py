from datetime import datetime, timezone
from bson import ObjectId


def create_analysis_report(
    website_id: ObjectId,
    findings: list[dict],
):
    now = datetime.now(timezone.utc)

    high_risks = 0
    medium_risks = 0
    low_risks = 0
    unknown_risks = 0

    total_score = 0

    for finding in findings:

        risk_level = finding.get(
            "risk_level",
            "unknown",
        )

        risk_score = finding.get(
            "risk_score",
            0,
        )

        total_score += risk_score

        if risk_level == "high":
            high_risks += 1

        elif risk_level == "medium":
            medium_risks += 1

        elif risk_level == "low":
            low_risks += 1

        else:
            unknown_risks += 1

    # Determine overall risk
    if high_risks > 0:
        overall_risk = "high"

    elif medium_risks > 0:
        overall_risk = "medium"

    elif low_risks > 0:
        overall_risk = "low"

    else:
        overall_risk = "unknown"

    return {
        "website_id": website_id,

        "overall_risk": overall_risk,

        "total_score": total_score,

        "total_findings": len(findings),

        "high_risks": high_risks,

        "medium_risks": medium_risks,

        "low_risks": low_risks,

        "unknown_risks": unknown_risks,

        "findings": findings,

        "created_at": now,

        "updated_at": now,
    }
