from datetime import datetime, timezone
from bson import ObjectId


def create_website_document(url: str, domain: str):
    return {
        "url": url,
        "domain": domain,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }