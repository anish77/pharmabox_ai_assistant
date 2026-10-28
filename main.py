from app.services.rag_pipeline import RAGPipeline


def main():
    rag = RAGPipeline()

    sources = [
        {"id": "SOURCE_1", "page": 9},
        {"id": "SOURCE_2", "page": 7},
        {"id": "SOURCE_3", "page": 29}
    ]

    answer_1 = "Per creare una lista, tocca + [SOURCE_1]."
    answer_2 = "Per creare una lista, tocca + [SOURCE_8]."

    print(rag.validate_citations(answer_1, sources))
    print(rag.validate_citations(answer_2, sources))


if __name__ == "__main__":
    main()