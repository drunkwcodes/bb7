import os
from datetime import datetime

import chromadb
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.readers.file import PDFReader
from llama_index.readers.file.markdown import MarkdownReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from peewee import *
from platformdirs import user_data_dir

bb7_dir = user_data_dir(appname="bb7", appauthor="drunkwcodes")
CHROMA_DB_PATH = f"{bb7_dir}/chroma_db"

COLLECTIONS_DB = f"{bb7_dir}/collections.sqlite"

cdb = SqliteDatabase(COLLECTIONS_DB, check_same_thread=False)


class BaseModel(Model):
    class Meta:
        database = cdb


class Collection(BaseModel):
    name = CharField(unique=True)
    path = CharField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)


def init_db():
    Collection.create_table()


if not os.path.exists(COLLECTIONS_DB):
    init_db()


def load_markdown_documents(path: str):
    parser = MarkdownReader()
    file_extractor = {".md": parser}
    documents = SimpleDirectoryReader(
        input_files=[path], file_extractor=file_extractor
    ).load_data()

    return documents


def load_pdf_documents(path: str):
    # PDF Reader with `SimpleDirectoryReader`
    parser = PDFReader()
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(
        input_files=[path], file_extractor=file_extractor
    ).load_data()

    return documents


def create_index(collection_name: str, documents):
    # create client
    db = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    chroma_collection = db.get_or_create_collection(collection_name)
    embed_model = HuggingFaceEmbedding()

    # save embedding to disk
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model
    )

    # The VectorStoreIndex class, in conjunction with the storage_context (which points to the ChromaDB collection),
    # stores these embeddings and their corresponding document metadata in the specified ChromaDB collection.


def update_index(collection_name: str, documents):
    db = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    db.delete_collection(collection_name)

    chroma_collection = db.get_or_create_collection(collection_name)
    embed_model = HuggingFaceEmbedding()

    # save embedding to disk
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model
    )


def load_index(collection_name: str, db_path: str | None = None):
    db_path = db_path or CHROMA_DB_PATH
    db = chromadb.PersistentClient(path=db_path)
    chroma_collection = db.get_or_create_collection(collection_name)
    embed_model = HuggingFaceEmbedding()
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    return index


def ask(query: str, collection_name: str, db_path: str | None = None):
    llm = Ollama(model="llama3.2", request_timeout=120)
    index = load_index(collection_name=collection_name, db_path=db_path)
    query_engine = index.as_query_engine(llm=llm)

    response = query_engine.query(query)

    return str(response)


if __name__ == "__main__":
    documents = load_markdown_documents(
        "/home/drunkwcodes/projects/myfoam/kb/package_manager/pdm.md"
    )
    create_index("pdm", documents)

    print(ask("what is pdm?", "pdm"))
