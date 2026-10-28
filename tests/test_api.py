from fastapi.testclient import TestClient
from app.api import app
from unittest.mock import patch

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ask_endpoint():
    fake_result = {
        "answer": "Tocca il pulsante + [SOURCE_1].",
        "sources": [
            {
                "id": "SOURCE_1",
                "page": 9,
                "source": "Manuale-PharmaBox.pdf"
            }
        ],
        "citations_valid": True
    }

    with patch("app.api.RAGPipeline") as mock_pipeline:
        mock_pipeline.return_value.ask.return_value = fake_result

        response = client.post(
            "/ask",
            json={"question": "Come creo una lista?"}
        )

    assert response.status_code == 200
    assert response.json() == fake_result

def test_ask_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 422