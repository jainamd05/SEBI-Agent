from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.db import get_db
from app.database.models import User
from app.schemas.document import DocumentUploadResponse, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = await DocumentService.upload_document(
        db=db,
        file=file,
        owner_id=current_user.id,
    )

    return DocumentUploadResponse(
        message="Document uploaded successfully.",
        document=DocumentResponse.model_validate(document),
    )