from app.infrastructure.embedding_service import EmbeddingService
from app.infrastructure.vector_store import VectorStore
from app.infrastructure.llm_service import LLMService
import re

class RAGPipeline:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()

    def retrieve(self, question: str, top_k: int = 3) -> list[dict]:
        query_embedding = self.embedding_service.embed_text(question)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        retrieved_chunks = []

        for index, document in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][index]

            retrieved_chunks.append({
                "text": document,
                "page": metadata["page"],
                "source": metadata["source"]
            })

        return retrieved_chunks

    def build_context(self, chunks: list[dict]) -> str:
        context_parts = []

        for index, chunk in enumerate(chunks, start=1):
            context_parts.append(
                f"[SOURCE_{index}]\n"
                f"Documento: {chunk['source']}\n"
                f"Pagina: {chunk['page']}\n"
                f"Testo: {chunk['text']}"
            )

        return "\n\n".join(context_parts)

    def ask(self, question: str) -> dict:
        chunks = self.retrieve(question, top_k=3)

        if not chunks:
            return {
                "answer": "Non ho trovato informazioni sufficienti.",
                "sources": [],
                "citations_valid": False
            }

        context = self.build_context(chunks)

        answer = self.llm_service.generate_answer(
            question=question,
            context=context
        )

        sources = []

        for index, chunk in enumerate(chunks, start=1):
            sources.append({
                "id": f"SOURCE_{index}",
                "page": chunk["page"],
                "source": chunk["source"]
            })

        citations_valid = self.validate_citations(
            answer=answer,
            sources=sources
        )

        return {
            "answer": answer,
            "sources": sources,
            "citations_valid": citations_valid
        }

    def validate_citations(self, answer: str, sources: list[dict]) -> bool:
        citation_ids = re.findall(r"\[SOURCE_\d+\]", answer)

        if not citation_ids:
            return False

        valid_ids = {
            f"[{source['id']}]"
            for source in sources
        }

        return all(
            citation_id in valid_ids
            for citation_id in citation_ids
        )