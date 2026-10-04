from bson import ObjectId

from .rag_service import retrieve_context
from .policy_analyzer import analyze_policy_evidence
from .risk_engine import (
    calculate_risk_score,
    calculate_risk_level,
)
from .evidence_verifier import verify_evidence


def analyze_category(
    website_id: ObjectId,
    category: dict,
):
    """
    Analyze one policy risk category.

    Flow:

    1. Retrieve relevant policy evidence
    2. Analyze evidence with LLM
    3. Verify generated evidence
    4. Calculate deterministic risk
    5. Return structured finding
    """

    category_name = category["name"]
    question = category["question"]

    print(
        f"Analyzing category: {category_name}"
    )

    # -----------------------------------------
    # 1. Retrieve relevant policy evidence
    # -----------------------------------------

    context, sources = retrieve_context(
        question=question,
        website_id=website_id,
        limit=5,
    )

    # -----------------------------------------
    # 2. No evidence found
    # -----------------------------------------

    if not sources:

        return {
            "category": category_name,
            "status": "no_evidence",
            "finding": "",
            "severity": "unknown",
            "evidence": "",
            "evidence_verified": False,
            "explanation": (
                "No relevant policy evidence "
                "was found."
            ),
            "source_url": "",
            "section": "",
            "risk_score": 0,
            "risk_level": "unknown",
        }

    # -----------------------------------------
    # 3. Analyze retrieved evidence
    # -----------------------------------------

    finding = analyze_policy_evidence(
        question=question,
        context=context,
    )

    # -----------------------------------------
    # 4. Verify evidence
    # -----------------------------------------

    verification = verify_evidence(
        evidence=finding.get(
            "evidence",
            "",
        ),
        sources=sources,
    )

    evidence_verified = (
        verification["verified"]
    )

    # -----------------------------------------
    # 5. Calculate risk
    # -----------------------------------------

    evidence = finding.get(
        "evidence",
        "",
    ).strip()

    severity = finding.get(
        "severity",
        "unknown",
    )

    evidence_found = (
        bool(evidence)
        and evidence_verified
    )

    risk_score = calculate_risk_score(
        severity=severity,
        evidence_found=evidence_found,
    )

    risk_level = calculate_risk_level(
        risk_score
    )

    # -----------------------------------------
    # 6. Build final finding
    # -----------------------------------------

    return {
        "category": category_name,
        "status": "analyzed",
        "finding": finding.get(
            "finding",
            "",
        ),
        "severity": severity,
        "evidence": evidence,
        "evidence_verified": evidence_verified,
        "explanation": finding.get(
            "explanation",
            "",
        ),
        "source_url": finding.get(
            "source_url",
            "",
        ),
        "section": finding.get(
            "section",
            "",
        ),
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


def analyze_website(
    website_id: ObjectId,
    categories: list[dict],
):
    """
    Analyze all requested risk categories.

    Each category is processed independently.
    """

    findings = []

    for category in categories:

        try:

            finding = analyze_category(
                website_id=website_id,
                category=category,
            )

            findings.append(
                finding
            )

        except Exception as error:

            category_name = category["name"]

            print(
                f"Category failed: {category_name}"
            )

            print(
                "Error:",
                error
            )

            findings.append(
                {
                    "category": category_name,
                    "status": "error",
                    "finding": "",
                    "severity": "unknown",
                    "evidence": "",
                    "evidence_verified": False,
                    "explanation": (
                        "The category could not "
                        "be analyzed."
                    ),
                    "source_url": "",
                    "section": "",
                    "risk_score": 0,
                    "risk_level": "unknown",
                    "error": str(error),
                }
            )

    return findings
