from pydantic import BaseModel


class PolicyFinding(BaseModel):
    category: str
    finding: str
    severity: str
    evidence: str
    explanation: str
    source_url: str
    section: str
    