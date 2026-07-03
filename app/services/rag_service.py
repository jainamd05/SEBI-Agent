from google import genai

from app.core.config import settings
from app.core.logger import get_logger

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

logger = get_logger(__name__)


class RAGService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        # We will improve this later (see note below)
        self.vector_service = VectorService(
            dimension=3072
        )

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

    def ask(
        self,
        question: str,
    ):

        logger.info(
            "Searching relevant chunks..."
        )

        query_embedding = self.embedding_service.embed_query(
            question
        )

        chunks = self.vector_service.search(
            query_embedding,
            top_k=5,
        )

        context = "\n\n".join(
            chunk["text"]
            for chunk in chunks
        )

        prompt = f"""
You are a SEBI AI assistant.

Answer ONLY using the supplied context.

If the answer is not present in the context,
reply:

"I could not find the answer in the uploaded documents."

Context:

{context}

Question:

{question}
"""

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        return {
            "answer": response.text,
            "sources": chunks,
        }