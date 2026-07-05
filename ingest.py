from dotenv import load_dotenv
import os
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"),
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)


def ingest_text(raw_text, url, title, source):

    texts = text_splitter.create_documents(
        [raw_text],
        metadatas=[
            {
                "title": title,
                "url": url,
                "source": source
            }
        ]
    )

    uuids = [str(uuid4()) for _ in texts]

    vector_store.add_documents(
        documents=texts,
        ids=uuids
    )