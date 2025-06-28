from typing import Self
from langchain_ollama import OllamaEmbeddings

from config import settings


class EmbeddingService:
    def __init__(self) -> None:
        self.model = OllamaEmbeddings(  # TODO: Need to replace langchain_ollama with original ollama libary
            model=settings.embeddings.model_name,
        )

    def as_dependency(self) -> Self:
        return self

    async def get_query_embedding(self, query: str) -> list[float]:
        vec = await self.model.aembed_query(query)
        return vec

    async def get_embeddings_func(self):
        return self.get_query_embedding

    async def get_documents_embedding(self, documents: list[str]) -> list[list[float]]:
        documents_vecs = await self.model.aembed_documents(documents)
        return documents_vecs


service = EmbeddingService()
