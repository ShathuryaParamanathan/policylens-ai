import httpx

from ..config import settings


OPENROUTER_EMBEDDINGS_URL = (
    "https://openrouter.ai/api/v1/embeddings"
)


def generate_embeddings(texts: list[str]):
    """
    Generate embeddings for multiple texts.
    """

    if not texts:
        return []

    response = httpx.post(
        OPENROUTER_EMBEDDINGS_URL,
        headers={
            "Authorization": (
                f"Bearer {settings.openrouter_api_key}"
            ),
            "Content-Type": "application/json",
        },
        json={
            "model": settings.openrouter_embedding_model,
            "input": texts,
        },
        timeout=90,
    )

    response.raise_for_status()

    result = response.json()

    # OpenRouter returns one vector per input.
    data = sorted(
        result["data"],
        key=lambda item: item["index"]
    )

    return [
        item["embedding"]
        for item in data
    ]