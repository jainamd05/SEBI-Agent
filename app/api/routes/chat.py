from fastapi import APIRouter
from fastapi import Depends

from app.core.security import get_current_user
from app.database.models import User
from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResponse
from app.services.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

rag_service = RAGService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ask a question about uploaded documents.
    """

    result = rag_service.ask(
        request.question
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )