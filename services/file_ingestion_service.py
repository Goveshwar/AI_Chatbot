
from services.document_loader import (
    load_document
)

from services.vector_store_service import (
    build_vector_store
)


def ingest_file(
    file_path: str
):

    documents = load_document(
        file_path
    )

    build_vector_store(
        documents
    )

    return True

