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
