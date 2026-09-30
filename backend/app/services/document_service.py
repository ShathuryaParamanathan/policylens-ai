from bson import ObjectId

from ..database import db
from ..models.document import create_policy_document


def save_policy_document(
    website_id: ObjectId,
    document: dict,
):
    policy_document = create_policy_document(
        website_id=website_id,
        url=document["url"],
        title=document["title"],
        document_type=document["document_type"],
        content=document["cleaned_text"],
        headings=document["headings"],
    )

    result = db.documents.insert_one(policy_document)

    return result.inserted_id