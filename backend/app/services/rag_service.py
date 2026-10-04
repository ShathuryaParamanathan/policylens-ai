from bson import ObjectId

from .embedding_service import generate_embeddings
from .vector_search import search_similar_chunks
from .llm_service import generate_answer


def retrieve_context(
    question: str,
    website_id: ObjectId,
    limit: int = 5,
):
    query_embedding = generate_embeddings(
        [question]
    )[0]

    results = search_similar_chunks(
        query_embedding=query_embedding,
        website_id=website_id,
        limit=limit,
    )

    context_parts = []

    for index, result in enumerate(results):

        context_parts.append(
            f"""
SOURCE {index + 1}

Document Type:
{result.get("document_type", "")}

Section:
{result.get("section_title", "")}

URL:
{result.get("source_url", "")}

Content:
{result.get("content", "")}
""".strip()
        )

    context = "\n\n".join(context_parts)

    return context, results


def answer_question(
    question: str,
    website_id: ObjectId,
    limit: int = 5,
):
    context, sources = retrieve_context(
        question=question,
        website_id=website_id,
        limit=limit,
    )

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }
