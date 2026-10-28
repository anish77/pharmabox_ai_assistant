# PharmaBox AI Assistant

An AI-powered assistant that answers questions about the PharmaBox application using Retrieval-Augmented Generation (RAG).

The assistant retrieves relevant information from the PharmaBox user manual and generates answers grounded in the retrieved content, including references to the source document and page numbers.

## Key Features

- PDF document ingestion using PyMuPDF
- Text chunking with configurable overlap
- Semantic embeddings using Sentence Transformers
- Persistent vector storage with ChromaDB
- Retrieval-Augmented Generation using the OpenAI API
- Source references and citation ID validation
- REST API built with FastAPI
- Automated tests using pytest

## Tech Stack

- **Language:** Python 3.12
- **API Framework:** FastAPI
- **LLM:** OpenAI GPT-4.1 mini
- **Embedding Model:** all-MiniLM-L6-v2
- **Vector Database:** ChromaDB
- **PDF Processing:** PyMuPDF
- **Testing:** pytest, FastAPI TestClient

## Architecture

The application follows a modular RAG architecture:

1. **PDF Ingestion** — Extract text and page metadata using PyMuPDF.
2. **Chunking** — Split document text into overlapping chunks.
3. **Embeddings** — Convert chunks into semantic vectors using Sentence Transformers.
4. **Vector Storage** — Store embeddings and metadata persistently in ChromaDB.
5. **Retrieval** — Find the most relevant chunks for a user question.
6. **Generation** — Generate an answer using OpenAI and the retrieved context.
7. **Citation Validation** — Check that cited source IDs exist among the retrieved sources.
8. **REST API** — Expose the assistant through FastAPI.
