from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


async def prepare_documents(file_name: str) -> list[Document]:
    document = await PyMuPDFLoader(file_path=file_name).aload()
    chunks = await splitter.atransform_documents(documents=document)
    return list(chunks)
