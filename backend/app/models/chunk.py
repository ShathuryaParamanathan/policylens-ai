from datetime import datetime, timezone
from bson import ObjectId


def create_chunk_document(
    website_id: ObjectId,
    document_id: ObjectId,
    document_type: str,
    source_url: str,
    section_title: str,
    chunk_index: int,
    content: str,
):
    now = datetime.now(timezone.utc)

  
    return {
        "website_id": website_id,
        "document_id": document_id,
        "document_type": document_type,
        "source_url": source_url,
        "section_title": section_title,
        "chunk_index": chunk_index,
        "content": content,
        "content_length": len(content),
        "embedding": None,
        "embedding_model": None,
        "created_at": now,
        "updated_at": now,
    }