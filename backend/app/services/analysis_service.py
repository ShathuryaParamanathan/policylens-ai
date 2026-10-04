from bson import ObjectId

from ..database import db
from ..models.analysis_result import (
    create_analysis_result,
)


def save_analysis_finding(
    website_id: ObjectId,
    finding: dict,
):
    analysis_result = create_analysis_result(
        website_id=website_id,
        category=finding.get(
            "category",
            "unknown",
        ),
        finding=finding.get(
            "finding",
            "",
        ),
        severity=finding.get(
            "severity",
            "unknown",
        ),
        evidence=finding.get(
            "evidence",
            "",
        ),
        evidence_verified=finding.get(
            "evidence_verified",
            False,
        ),
        explanation=finding.get(
            "explanation",
            "",
        ),
        source_url=finding.get(
            "source_url",
            "",
        ),
        section=finding.get(
            "section",
            "",
        ),
        risk_score=finding.get(
            "risk_score",
            0,
        ),
        risk_level=finding.get(
            "risk_level",
            "unknown",
        ),
    )

    result = db.analysis_results.insert_one(
        analysis_result
    )

    return result.inserted_id


def save_analysis_findings(
    website_id: ObjectId,
    findings: list[dict],
):
    saved_ids = []

    for finding in findings:
        result_id = save_analysis_finding(
            website_id=website_id,
            finding=finding,
        )

        saved_ids.append(result_id)

    return saved_ids