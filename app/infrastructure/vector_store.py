import chromadb


class VectorStore:

    def __init__(self, persist_directory: str = "data/chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name="pharmabox_manual"
        )

    def add_chunks(self, chunks: list[dict], embeddings):
        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            ids.append(f"chunk_{index}")
            documents.append(chunk["text"])
            metadatas.append({
                "page": chunk["page"],
                "source": chunk["source"]
            })

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k: int = 3):
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        return results