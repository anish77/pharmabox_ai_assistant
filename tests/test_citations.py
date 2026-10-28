from app.services.rag_pipeline import RAGPipeline


def test_valid_citation():
    sources = [
        {"id": "SOURCE_1", "page": 9},
        {"id": "SOURCE_2", "page": 7}
    ]

    answer = "Per creare una lista, tocca + [SOURCE_1]."

    result = RAGPipeline.validate_citations(
        None,
        answer,
        sources
    )

    assert result is True

def test_invalid_citation():
    sources = [
        {"id": "SOURCE_1", "page": 9},
        {"id": "SOURCE_2", "page": 7}
    ]

    answer = "Per creare una lista, tocca + [SOURCE_9]."

    result = RAGPipeline.validate_citations(
        None,
        answer,
        sources
    )

    assert result is False

def test_missing_citation():
    sources = [
        {"id": "SOURCE_1", "page": 9},
        {"id": "SOURCE_2", "page": 7}
    ]

    answer = "Per creare una lista, tocca il pulsante +."

    result = RAGPipeline.validate_citations(
        None,
        answer,
        sources
    )

    assert result is False