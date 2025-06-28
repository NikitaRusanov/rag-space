from uuid import UUID
from pydantic import BaseModel


class DocumentChunk(BaseModel):
    text: str
    document_name: str
    author: UUID
    documnet_id: UUID | None = None
