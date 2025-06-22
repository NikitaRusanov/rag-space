from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
import aiofiles
from pathlib import Path
import asyncio

from services.embedding_service import service as emb_service, EmbeddingService
from utils.documetns import prepare_documents

router = APIRouter(prefix="/documents")


@router.post("/")
async def upload_file(
    embedding_service: Annotated[EmbeddingService, Depends(emb_service.as_dependency)],
    files: list[UploadFile] = File(...),
):
    tasks = []
    async with aiofiles.tempfile.TemporaryDirectory() as tmp_dir:
        for file in files:
            file_path = Path(tmp_dir) / file.filename
            print(file_path)

            async with aiofiles.open(file_path, "wb") as tmp_file:
                while content := await file.read(
                    1024 * 1024
                ):  # TODO: make paramter for reading size
                    await tmp_file.write(content)
            tasks.append(prepare_documents(str(file_path)))

        chunks_list = await asyncio.gather(*tasks)

    return {"Total documents uploaded": len(chunks_list)}
