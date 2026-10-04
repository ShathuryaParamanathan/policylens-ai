from bson import ObjectId

from ..database import db


VECTOR_INDEX_NAME = "policy_vector_index"


def search_similar_chunks(
    query_embedding: list[float],
    website_id: ObjectId,
    limit: int = 5,
):
    """
    Search policy chunks using MongoDB Atlas Vector Search.
    """

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": limit * 10,
                "limit": limit,
                "filter": {
                    "website_id": website_id
                },
            }
        },
        {
            "$project": {
                "_id": 1,
                "document_id": 1,
                "document_type": 1,
                "source_url": 1,
                "section_title": 1,
                "chunk_index": 1,
                "content": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                },
            }
        },
    ]

    return list(
        db.chunks.aggregate(pipeline)
    )
