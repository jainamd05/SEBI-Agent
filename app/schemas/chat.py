from typing import List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    User question.
    """

    question: str = Field(
        ...,
        min_length=3,
        max_length=5000,
    )


class Source(BaseModel):
    """
    Source document returned by RAG.
    """

    document_id: int
    chunk_index: int
    text: str


class ChatResponse(BaseModel):
    """
    Final response returned to client.
    """

    answer: str
    sources: List[Source]