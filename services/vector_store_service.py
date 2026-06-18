
import os

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


VECTOR_DB_PATH = (
    "vectorstore/faiss_index"
)


_embeddings = None


def create_embeddings():

    global _embeddings

    if _embeddings is None:

        _embeddings = (
            HuggingFaceEmbeddings(
                model_name=
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        )

    return _embeddings


def build_vector_store(
    documents
):

    if not documents:

        raise ValueError(
            "No documents found."
        )

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
    )

    chunks = (
        splitter.split_documents(
            documents
        )
    )

    embeddings = (
        create_embeddings()
    )

    vectorstore = (
        FAISS.from_documents(
            chunks,
            embeddings
        )
    )

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    vectorstore.save_local(
        VECTOR_DB_PATH
    )

    return vectorstore


def load_vector_store():

    if not os.path.exists(
        VECTOR_DB_PATH
    ):

        raise FileNotFoundError(
            "No FAISS index found."
        )

    embeddings = (
        create_embeddings()
    )

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

