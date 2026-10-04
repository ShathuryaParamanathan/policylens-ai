from bson import ObjectId

from ..config import settings
from ..database import db
from .embedding_service import generate_embeddings


def embed_document_chunks(
    document_id: ObjectId,
    batch_size: int = 20,
):
    """
    Generate embeddings for all chunks belonging
    to a document that do not already have embeddings.
    """

    chunks = list(
        db.chunks.find(
            {
                "document_id": document_id,
                "embedding": None,
            }
        ).sort(
            "chunk_index",
            1
        )
    )

    if not chunks:
        return 0

    total_embedded = 0

    for start in range(
        0,
        len(chunks),
        batch_size
    ):
        batch = chunks[
            start:start + batch_size
        ]

        texts = [
            chunk["content"]
            for chunk in batch
        ]

        embeddings = generate_embeddings(
            texts
        )

        if len(embeddings) != len(batch):
            raise RuntimeError(
                "Embedding count does not match "
                "chunk count."
            )

        for chunk, embedding in zip(
            batch,
            embeddings
        ):
            db.chunks.update_one(
                {
                    "_id": chunk["_id"]
                },
                {
                    "$set": {
                        "embedding": embedding,
                        "embedding_model": (
                            settings.openrouter_embedding_model
                        )
                    }
                }
            )

            total_embedded += 1

    return total_embedded