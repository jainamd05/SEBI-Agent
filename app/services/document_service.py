from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.database.crud import create_document
from app.services.pdf_service import PDFService

logger = get_logger(__name__)


class DocumentService:

    UPLOAD_DIRECTORY = Path("uploads")

    ALLOWED_TYPES = {
        "application/pdf",
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    @classmethod
    async def upload_document(
        cls,
        db: Session,
        file: UploadFile,
        owner_id: int,
    ):

        if file.content_type not in cls.ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        content = await file.read()

        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum size.",
            )

        cls.UPLOAD_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        unique_filename = (
            f"{uuid4().hex}_{file.filename}"
        )

        file_path = (
            cls.UPLOAD_DIRECTORY / unique_filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        document = create_document(
            db=db,
            filename=file.filename,
            filepath=str(file_path),
            file_size=len(content),
            mime_type=file.content_type,
            owner_id=owner_id,
        )

        extracted_text = PDFService.extract_text(
            str(file_path)
        )

        logger.info(
            "Extracted %d characters.",
            len(extracted_text),
        )

        return document