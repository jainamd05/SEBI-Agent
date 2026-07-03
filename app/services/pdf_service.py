import fitz

from app.core.logger import get_logger

logger = get_logger(__name__)


class PDFService:
    """
    Service responsible for PDF parsing.
    """

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a PDF document.
        """

        try:
            document = fitz.open(file_path)

            text = []

            for page in document:
                page_text = page.get_text("text")

                if page_text:
                    text.append(page_text)

            document.close()

            logger.info(
                "Successfully extracted text from %s",
                file_path,
            )

            return "\n".join(text)

        except Exception as exc:
            logger.exception(
                "Failed to extract PDF text."
            )
            raise RuntimeError(
                "Unable to process PDF."
            ) from exc