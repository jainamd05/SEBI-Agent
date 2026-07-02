from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """
    Response returned after uploading or fetching a document.
    """

    id: int
    filename: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    """
    Response after a successful upload.
    """

    message: str
    document: DocumentResponse