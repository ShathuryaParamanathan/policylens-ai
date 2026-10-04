from datetime import datetime, timezone
from bson import ObjectId


def create_analysis_result(
    website_id: ObjectId,
    category: str,
    finding: str,
    severity: str,
    evidence: str,
    evidence_verified: bool,
    explanation: str,
    source_url: str,
    section: str,
    risk_score: int,
    risk_level: str,
):
    now = datetime.now(timezone.utc)

    return {
        "website_id": website_id,
        "category": category,
        "finding": finding,
        "severity": severity,
        "evidence": evidence,
        "evidence_verified": evidence_verified,
        "explanation": explanation,
        "source_url": source_url,
        "section": section,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "created_at": now,
        "updated_at": now,
    }