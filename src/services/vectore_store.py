from uuid import UUID

import weaviate
from weaviate.connect import ConnectionParams
import weaviate.classes as wvc

from schemas import DocumentChunk


async def get_weavite_client():
    client = weaviate.WeaviateAsyncClient(  # TODO: read params from config
        connection_params=ConnectionParams.from_params(
            http_host="localhost",
            http_port=8080,
            http_secure=False,
            grpc_host="localhost",
            grpc_port=50051,
            grpc_secure=False,
        )
    )
    await client.connect()
    try:
        yield client
    finally:
        await client.close()


class WeaviteVectoreStore:
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name
        self.client = weaviate.WeaviateAsyncClient(  # TODO: read params from config
            connection_params=ConnectionParams.from_params(
                http_host="localhost",
                http_port=8080,
                http_secure=False,
                grpc_host="localhost",
                grpc_port=50051,
                grpc_secure=False,
            )
        )

    async def init_collection(self) -> None:
        if await self.client.collections.exists(self.collection_name):
            await self.client.collections.delete(self.collection_name)

        self.collection = await self.client.collections.create(
            name=self.collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            properties=[
                wvc.config.Property(
                    name="chunk_text", data_type=wvc.config.DataType.TEXT
                ),
                wvc.config.Property(
                    name="document_name", data_type=wvc.config.DataType.TEXT
                ),
                wvc.config.Property(
                    name="author_id", data_type=wvc.config.DataType.UUID
                ),
            ],
        )

    async def insert_document(
        self,
        document: str,
        document_name: str,
        user_id: UUID,
        document_vector: list[float],
    ) -> UUID:
        collection = self.client.collections.get(self.collection_name)
        document_id = await collection.data.insert(
            {
                "chunk_text": document,
                "document_name": document_name,
                "author_id": user_id,
            },
            vector=document_vector,
        )
        return document_id

    async def get_similar(
        self, query_vec: list[float], k: int = 3
    ) -> list[DocumentChunk]:
        collection = self.client.collections.get(self.collection_name)
        relevant_documents = await collection.query.near_vector(
            near_vector=query_vec, limit=k
        )
        documents = []
        for document in relevant_documents.objects:
            documents.append(
                DocumentChunk(
                    text=document.properties["chunk_text"],
                    document_name=document.properties["document_name"],
                    author=document.properties["author_id"],
                    documnet_id=document.uuid,
                )
            )
        return documents


store = WeaviteVectoreStore("aboba")  # TODO: make collection name read from config


async def get_vectore_store():
    return store
