from datetime import datetime, timezone
from bson import ObjectId


def create_policy_document(
    website_id: ObjectId,
    url: str,
    title: str,
    document_type: str,
    content: str,
    headings: list,
):
    now = datetime.now(timezone.utc)

    return {
        "website_id": website_id,
        "url": url,
        "title": title,
        "document_type": document_type,
        "content": content,
        "headings": headings,
        "created_at": now,
        "updated_at": now,
    }