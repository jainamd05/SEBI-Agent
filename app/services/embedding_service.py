from typing import List

from google import genai

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """
    Handles text embedding generation using Google's Gemini API.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate an embedding for a single text.
        """

        try:

            response = self.client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
            )

            return response.embeddings[0].values

        except Exception as exc:

            logger.exception(
                "Embedding generation failed."
            )

            raise RuntimeError(
                "Unable to generate embeddings."
            ) from exc

    def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple chunks.
        """

        vectors = []

        for text in texts:
            vectors.append(
                self.embed_text(text)
            )

        return vectors