from bson import ObjectId

from ..database import db
from ..models.chunk import create_chunk_document
from .chunker import chunk_text


def find_section_for_chunk(
    chunk: str,
    headings: list
):
    """
    Find the most likely section heading
    associated with a chunk.
    """

    if not headings:
        return ""

    first_text = chunk[:300].lower()

    selected_heading = ""

    for heading in headings:

        heading_text = heading.get(
            "text",
            ""
        ).strip()

        if not heading_text:
            continue

        if heading_text.lower() in first_text:
            selected_heading = heading_text

    return selected_heading


def create_document_chunks(
    website_id: ObjectId,
    document_id: ObjectId,
    document: dict,
):
    content = document["content"]

    chunks = chunk_text(
        content,
        max_characters=2000
    )

    headings = document.get(
        "headings",
        []
    )

    chunk_documents = []

    for index, chunk in enumerate(chunks):

        section_title = find_section_for_chunk(
            chunk,
            headings
        )

        chunk_document = create_chunk_document(
            website_id=website_id,
            document_id=document_id,
            document_type=document["document_type"],
            source_url=document["url"],
            section_title=section_title,
            chunk_index=index,
            content=chunk,
        )

        chunk_documents.append(
            chunk_document
        )

    return chunk_documents


def save_document_chunks(
    website_id: ObjectId,
    document_id: ObjectId,
    document: dict,
):
    chunks = create_document_chunks(
        website_id=website_id,
        document_id=document_id,
        document=document
    )

    if not chunks:
        return []

    result = db.chunks.insert_many(
        chunks
    )

    return result.inserted_ids

