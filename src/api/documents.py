from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Depends, File, UploadFile
import aiofiles
from pathlib import Path
import asyncio

from services.embedding_service import service as emb_service, EmbeddingService
from services.vectore_store import WeaviteVectoreStore, get_vectore_store
from utils.documetns import prepare_documents
from schemas import DocumentChunk

router = APIRouter(prefix="/documents")


@router.post("/")
async def upload_file(
    embedding_service: Annotated[EmbeddingService, Depends(emb_service.as_dependency)],
    vectore_store: Annotated[WeaviteVectoreStore, Depends(get_vectore_store)],
    files: list[UploadFile] = File(...),
):
    tasks = []
    async with aiofiles.tempfile.TemporaryDirectory() as tmp_dir:
        for file in files:
            file_path = Path(tmp_dir) / file.filename

            async with aiofiles.open(file_path, "wb") as tmp_file:
                while content := await file.read(
                    1024 * 1024
                ):  # TODO: make paramter for reading size
                    await tmp_file.write(content)
            tasks.append(prepare_documents(str(file_path)))

        documents_list = await asyncio.gather(*tasks)
    documents_vectors_tasks = [
        embedding_service.get_documents_embedding(
            [chunk.page_content for chunk in document]
        )
        for document in documents_list
    ]
    documents_vectors = await asyncio.gather(*documents_vectors_tasks)
    vectore_store_tasks = []
    for document, vectors in zip(documents_list, documents_vectors):
        for chunk, chunk_vector in zip(document, vectors):
            vectore_store_tasks.append(
                vectore_store.insert_document(
                    document=chunk.page_content,
                    document_name=chunk.metadata["title"],
                    user_id=uuid4(),
                    document_vector=chunk_vector,
                )
            )
    documents_ids = await asyncio.gather(*vectore_store_tasks)
    return {"Total documents uploaded": len(documents_ids)}


@router.get("/")
async def get_relevant_docs(
    query: str,
    embedding_service: Annotated[EmbeddingService, Depends(emb_service.as_dependency)],
    vectore_store: Annotated[WeaviteVectoreStore, Depends(get_vectore_store)],
) -> list[DocumentChunk]:
    query_emb = await embedding_service.get_query_embedding(query)
    docs = await vectore_store.get_similar(query_vec=query_emb)

    return docs
