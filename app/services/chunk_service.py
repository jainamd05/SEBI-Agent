from typing import List


class ChunkService:
    """
    Service responsible for splitting extracted text into
    overlapping chunks for embedding.
    """

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    @classmethod
    def split_text(
        cls,
        text: str,
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        """

        if not text.strip():
            return []

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + cls.CHUNK_SIZE

            chunk = text[start:end]

            chunks.append(chunk)

            start += cls.CHUNK_SIZE - cls.CHUNK_OVERLAP

        return chunks