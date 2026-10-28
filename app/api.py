from fastapi import FastAPI
from app.config import PROJECT_NAME, PROJECT_VERSION
from app.models.schemas import AskRequest
from app.services.rag_pipeline import RAGPipeline


app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": PROJECT_NAME
    }

@app.post("/ask")
def ask_question(request: AskRequest):
    rag = RAGPipeline()

    result = rag.ask(request.question)

    return result