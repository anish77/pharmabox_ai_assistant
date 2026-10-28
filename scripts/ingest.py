from pathlib import Path

from app.infrastructure.pdf_reader import read_pdf
from app.services.chunker import TextChunker
from app.infrastructure.embedding_service import EmbeddingService
from app.infrastructure.vector_store import VectorStore


def main():
    pdf_path = Path("data/raw/Manuale-PharmaBox.pdf")

    pages = read_pdf(pdf_path)

    chunker = TextChunker(chunk_size=500, overlap=100)
    chunks = chunker.chunk_pages(pages)

    embedding_service = EmbeddingService()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_service.embed_texts(texts)

    vector_store = VectorStore()
    vector_store.add_chunks(chunks, embeddings)

    print(f"Ingestion completed: {len(chunks)} chunks stored.")


if __name__ == "__main__":
    main()