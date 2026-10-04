from bson import ObjectId

from ..database import db
from ..models.analysis_report import (
    create_analysis_report,
)


def save_analysis_report(
    website_id: ObjectId,
    findings: list[dict],
):
    report = create_analysis_report(
        website_id=website_id,
        findings=findings,
    )

    result = db.analysis_reports.insert_one(
        report
    )

    return result.inserted_id


def get_analysis_report(
    website_id: ObjectId,
):
    return db.analysis_reports.find_one(
        {
            "website_id": website_id
        },
        sort=[
            ("created_at", -1)
        ],
    )
