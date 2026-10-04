from typing import Optional


SEVERITY_SCORES = {
    "unknown": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


def normalize_severity(
    severity: Optional[str],
) -> str:
    """
    Normalize an LLM-generated severity value.
    """

    if not severity:
        return "unknown"

    value = severity.lower().strip()

    if value not in SEVERITY_SCORES:
        return "unknown"

    return value


def calculate_risk_score(
    severity: str,
    evidence_found: bool,
) -> int:
    """
    Calculate a basic deterministic risk score.
    """

    severity = normalize_severity(severity)

    if not evidence_found:
        return 0

    return SEVERITY_SCORES[severity]


def calculate_risk_level(
    score: int,
) -> str:
    """
    Convert numerical score into a risk level.
    """

    if score == 0:
        return "unknown"

    if score == 1:
        return "low"

    if score == 2:
        return "medium"

    return "high"
