class TextChunker:

    def __init__(self, chunk_size: int = 500, overlap: int = 100):

        if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("Invalid chunk_size or overlap")

        self.chunk_size = chunk_size
        self.overlap = overlap

    # Logica di suddivisione
    def split_text(self, text: str) -> list[str]:
        chunks = []

        step = self.chunk_size - self.overlap

        for start in range(0, len(text), step):
            chunk = text[start:start + self.chunk_size]
            chunks.append(chunk)

            if start + self.chunk_size >= len(text):
                break

        return chunks

    # Logica di creazione dei chunk
    def chunk_pages(self, pages: list[dict]) -> list[dict]:
        all_chunks = []

        for page in pages:
            text_chunks = self.split_text(page["text"])

            for chunk in text_chunks:
                all_chunks.append({
                    "text": chunk,
                    "page": page["page"],
                    "source": page["source"]
                })

        return all_chunks