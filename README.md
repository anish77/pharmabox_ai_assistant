# PharmaBox AI Assistant

**A Retrieval-Augmented Generation (RAG) assistant built with Python, FastAPI, ChromaDB, Sentence Transformers, and OpenAI.**

PharmaBox AI Assistant is a portfolio project designed to answer questions about the PharmaBox application using information retrieved from its official user manual.

Instead of relying only on the language model's general knowledge, the assistant retrieves relevant document passages and uses them to generate grounded answers with source references.

The project demonstrates a modular RAG architecture, local semantic embeddings, persistent vector storage, REST API development, and automated testing.

## Key Features

- **PDF ingestion:** Extract text and page metadata from PDF documents using PyMuPDF.
- **Text chunking:** Split documents into configurable overlapping chunks.
- **Semantic embeddings:** Generate vector representations using Sentence Transformers.
- **Persistent vector database:** Store and retrieve embeddings with ChromaDB.
- **Semantic search:** Retrieve relevant passages based on the user's question.
- **RAG answer generation:** Generate context-grounded answers using OpenAI.
- **Source citations:** Return document names, page numbers, and citation identifiers.
- **Citation validation:** Check whether generated citation identifiers correspond to retrieved sources.
- **REST API:** Expose the assistant through FastAPI.
- **Automated testing:** Test API endpoints, request validation, and citation validation using pytest.

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| API Framework | FastAPI |
| Language Model | OpenAI GPT-4.1 mini |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Library | Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |
| Data Validation | Pydantic |
| Testing | pytest, FastAPI TestClient |
| Package Management | uv |
| Version Control | Git and GitHub |

## Architecture

The application follows a modular architecture that separates document processing, semantic retrieval, answer generation, and API handling.

### Document Ingestion

The ingestion pipeline prepares the knowledge base before users submit questions.

```text
PharmaBox User Manual (PDF)
          |
          v
     PDF Reader
          |
          v
   Text Chunking
          |
          v
  Sentence Transformers
          |
          v
       ChromaDB
  (Persistent Storage)
```

The ingestion process:

1. Reads the PDF and extracts text with page metadata.
2. Splits the text into overlapping chunks.
3. Generates semantic embeddings for each chunk.
4. Stores the chunk text, embeddings, and metadata in ChromaDB.

The ingestion script rebuilds the manual's collection to prevent outdated chunks from remaining after document updates.

### Question-Answering Pipeline

When a user submits a question, the RAG pipeline retrieves relevant information from the existing vector database.

```text
       User Question
             |
             v
      Query Embedding
             |
             v
      ChromaDB Search
             |
             v
      Top-K Documents
             |
             v
      Context Building
             |
             v
        OpenAI LLM
             |
             v
     Citation Validation
             |
             v
     Answer + Sources
```

The application does not regenerate embeddings for the entire manual for each question. Only the question embedding is generated during retrieval.

## Project Structure

```text
pharmabox_ai_assistant/
|
|-- app/
|   |-- api.py
|   |-- config.py
|   |
|   |-- infrastructure/
|   |   |-- pdf_reader.py
|   |   |-- embedding_service.py
|   |   |-- vector_store.py
|   |   |-- llm_service.py
|   |
|   |-- services/
|   |   |-- chunker.py
|   |   |-- rag_pipeline.py
|   |
|   |-- models/
|       |-- schemas.py
|
|-- scripts/
|   |-- ingest.py
|
|-- tests/
|   |-- test_api.py
|   |-- test_citations.py
|
|-- data/
|   |-- raw/
|   |-- chroma_db/
|
|-- pyproject.toml
|-- uv.lock
|-- README.md
```

The `data/raw/` directory contains local source documents, while `data/chroma_db/` contains the generated vector database. Their contents are excluded from version control.

## Installation

### Prerequisites

Before starting, ensure you have:

- Python 3.12 or a compatible Python 3.12+ environment
- Git
- [uv package manager](https://docs.astral.sh/uv/)
- An OpenAI API key
- Access to the PharmaBox user manual PDF

An internet connection is required for dependency installation, the initial embedding model download, and OpenAI API requests.

### 1. Clone the Repository

```bash
git clone https://github.com/anish77/pharmabox_ai_assistant.git
cd pharmabox_ai_assistant
```

### 2. Install Dependencies

```bash
uv sync --locked
```

This installs the dependencies defined in `pyproject.toml` using the versions recorded in `uv.lock`.

### 3. Configure the OpenAI API Key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your own OpenAI API key.

**Security:** Never commit API keys or the `.env` file to GitHub. Keep `.env` excluded through `.gitignore`.

The application reads `OPENAI_API_KEY` from its environment. The startup command below uses uv's `--env-file` option to load the variable.

### 4. Add the User Manual

Place the PharmaBox user manual at:

```text
data/raw/Manuale-PharmaBox.pdf
```

The manual is not included in this repository. You must provide an authorized copy to build the knowledge base.

The current ingestion script expects this filename and location.

### 5. Build the Vector Database

Run the ingestion script:

```bash
uv run python -m scripts.ingest
```

This process:

1. Reads the manual.
2. Creates overlapping text chunks.
3. Generates embeddings using `all-MiniLM-L6-v2`.
4. Rebuilds the ChromaDB collection.
5. Stores the new chunks and metadata persistently.

Example output:

```text
Ingestion completed: 146 chunks stored.
```

The number of chunks depends on the source document and chunking configuration.

**Important:** Re-running ingestion replaces the existing manual collection. It should not be run concurrently with requests that depend on that collection.

## Running the Application

Start the FastAPI development server:

```bash
uv run --env-file .env uvicorn app.api:app --reload
```

Open the interactive Swagger documentation:

http://127.0.0.1:8000/docs

FastAPI also provides the OpenAPI schema at:

http://127.0.0.1:8000/openapi.json

The `--reload` option is intended for local development.

## API Endpoints

### GET /health

Checks whether the API is responding.

Example request:

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok",
  "project": "PharmaBox AI Assistant"
}
```

This endpoint confirms that the API is reachable. It does not verify the availability of ChromaDB or the OpenAI service.

### POST /ask

Accepts a question about PharmaBox and returns an AI-generated answer with source references.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Come posso creare una lista in PharmaBox?"}'
```

Example response structure:

```json
{
  "answer": "Per creare una lista, utilizza il pulsante + e inserisci un titolo. [SOURCE_1]",
  "sources": [
    {
      "id": "SOURCE_1",
      "page": 9,
      "source": "Manuale-PharmaBox.pdf"
    }
  ],
  "citations_valid": true
}
```

This is an illustrative response. Actual generated answers and retrieved sources may differ.

### Request Validation

The API uses Pydantic to validate incoming requests.

An empty question is rejected with HTTP status `422 Unprocessable Entity`.

Example invalid request:

```json
{
  "question": ""
}
```

## Citation System

Retrieved document chunks are assigned identifiers such as:

```text
[SOURCE_1]
[SOURCE_2]
[SOURCE_3]
```

Each identifier corresponds to a retrieved chunk and is associated with the source document and page number.

The language model is instructed to cite the retrieved information it uses.

The application validates whether citation identifiers appearing in the generated answer belong to the retrieved source set.

**Note:** Citation validation checks identifier consistency. It does not independently verify that each cited passage supports the generated claim.

## Running Tests

Run the automated test suite:

```bash
uv run pytest tests/ -v
```

The current suite contains six tests:

| Test | Purpose |
|---|---|
| Health endpoint | Verify the API health response |
| Ask endpoint | Verify the response using a mocked RAG pipeline |
| Empty question | Verify Pydantic request validation |
| Valid citation | Accept a citation with a known source identifier |
| Invalid citation | Reject an unknown source identifier |
| Missing citation | Detect an answer without citation identifiers |

The API test uses mocking to avoid real OpenAI calls and unnecessary model initialization during testing.

Latest verified local result:

```text
6 passed
```

These are unit and API tests, not a complete end-to-end evaluation of answer accuracy.

## Design Decisions

### Why RAG?

A general-purpose language model does not automatically have access to the latest PharmaBox user manual.

RAG retrieves relevant information from the manual and supplies it as context before answer generation.

This approach makes it possible to answer application-specific questions, include source references, and reduce reliance on unsupported model knowledge.

### Why Local Embeddings?

The `all-MiniLM-L6-v2` model generates embeddings locally without requiring an OpenAI embedding API call.

The model produces 384-dimensional vectors and supports semantic similarity search.

### Why ChromaDB?

ChromaDB provides persistent vector storage, metadata support, and semantic retrieval suitable for a compact document-based RAG application.

### Why Modular Architecture?

Separating PDF ingestion, chunking, embeddings, vector storage, LLM integration, and API handling makes the project easier to maintain, test, and extend.

## Current Limitations

- The knowledge base currently uses a single PharmaBox PDF manual.
- Answer quality depends on the accuracy and completeness of the retrieved document passages.
- Citation validation verifies source identifiers, not factual support.
- The ingestion process rebuilds the active collection. If ingestion fails after the reset, the previous indexed data may no longer be available.
- The application does not yet provide an automated evaluation framework for retrieval relevance or answer quality.
- The current API initializes RAG dependencies for each `/ask` request, which may increase response latency.
- The API does not currently implement authentication or request rate limiting.
- The project has not been validated for production-scale deployment.

## Future Improvements

Potential improvements include:

- Safer ingestion using collection versioning and controlled switching
- Retrieval relevance thresholds
- Improved chunking and document preprocessing
- Automated RAG evaluation
- Structured API response models
- Better error handling and logging
- Reuse of initialized embedding and LLM services
- API authentication and rate limiting
- Support for multiple documents
- Containerization and deployment
- AI agent capabilities and tool integration

## Project Status

**Portfolio Project #1 — RAG Application**

Implemented:

- Document ingestion
- Text chunking and embeddings
- Persistent vector storage
- Semantic retrieval
- OpenAI answer generation
- Citation identifiers and validation
- FastAPI endpoints
- Automated tests

This project is intended as a practical demonstration of RAG engineering concepts and is not presented as a fully production-hardened service.

## Author

Developed as part of a hands-on AI/LLM Engineering learning journey, focusing on Python, Retrieval-Augmented Generation, semantic search, API development, and software engineering practices.
