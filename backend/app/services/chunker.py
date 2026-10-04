import re


def normalize_text(text: str):
    """
    Normalize whitespace while preserving paragraph boundaries.
    """

    text = text.replace("\r\n", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


def split_into_paragraphs(text: str):
    """
    Split text into paragraphs.
    """

    text = normalize_text(text)

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def split_long_text(
    text: str,
    max_characters: int
):
    """
    Split large text into smaller chunks
    without cutting words.
    """

    words = text.split()

    chunks = []
    current_words = []
    current_length = 0

    for word in words:

        additional_length = (
            len(word)
            if not current_words
            else len(word) + 1
        )

        if (
            current_words
            and current_length + additional_length
            > max_characters
        ):
            chunks.append(
                " ".join(current_words)
            )

            current_words = []
            current_length = 0

        current_words.append(word)
        current_length += additional_length

    if current_words:
        chunks.append(
            " ".join(current_words)
        )

    return chunks


def chunk_text(
    text: str,
    max_characters: int = 2000
):
    """
    Basic document chunking.

    Returns a list of text chunks.
    """

    paragraphs = split_into_paragraphs(text)

    chunks = []

    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        if paragraph_length > max_characters:

            if current_chunk:
                chunks.append(
                    "\n\n".join(current_chunk)
                )

                current_chunk = []
                current_length = 0

            chunks.extend(
                split_long_text(
                    paragraph,
                    max_characters
                )
            )

            continue

        additional_length = (
            paragraph_length
            if not current_chunk
            else paragraph_length + 2
        )

        if (
            current_chunk
            and current_length + additional_length
            > max_characters
        ):
            chunks.append(
                "\n\n".join(current_chunk)
            )

            current_chunk = []
            current_length = 0

        current_chunk.append(paragraph)
        current_length += additional_length

    if current_chunk:
        chunks.append(
            "\n\n".join(current_chunk)
        )

    return chunks

def is_heading(text: str):
    """
    Detect whether a line looks like a section heading.
    """

    text = text.strip()

    if not text:
        return False

    words = text.split()

    # Ignore extremely long lines
    if len(words) > 12:
        return False

    # Common heading indicators
    heading_patterns = [
        r"^#{1,6}\s+",
        r"^[A-Z][A-Za-z0-9 ,&()'/-]{2,80}$",
    ]

    return any(
        re.match(pattern, text)
        for pattern in heading_patterns
    )
