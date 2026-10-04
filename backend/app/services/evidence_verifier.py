import re


def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def verify_evidence(
    evidence: str,
    sources: list[dict],
) -> dict:
    """
    Check whether the LLM-generated evidence
    actually appears in retrieved source content.
    """

    if not evidence:
        return {
            "verified": False,
            "matched_source": None,
        }

    normalized_evidence = normalize_text(
        evidence
    )

    for source in sources:

        content = normalize_text(
            source.get("content", "")
        )

        if normalized_evidence in content:
            return {
                "verified": True,
                "matched_source": source,
            }

    return {
        "verified": False,
        "matched_source": None,
    }
