from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "rag-service"
    assert body["status"] == "healthy"
    assert body["document_count"] >= 4


def test_rag_query_customer_confidential_data():
    payload = {
        "query": "What should an AI agent do before accessing confidential customer data?",
        "user_id": "ola.consultant",
        "role": "security_architect",
        "data_region": "us",
        "max_results": 3,
    }

    response = client.post("/rag/query", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["result_count"] > 0
    assert body["confidence"] > 0
    assert body["evidence_created"] is True
    assert body["status"] == "sources_found"

    source_files = [source["source_file"] for source in body["sources"]]
    assert any(
        source_file in source_files
        for source_file in [
            "customer-data-handling-policy.md",
            "data-classification-standard.md",
            "internal-ai-policy.md",
        ]
    )


def test_rag_query_no_result():
    payload = {
        "query": "banana ocean guitar unrelated phrase",
        "user_id": "demo.user",
        "role": "reader",
        "data_region": "us",
        "max_results": 3,
    }

    response = client.post("/rag/query", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["result_count"] == 0
    assert body["confidence"] == 0.0
    assert body["status"] == "no_sources_found"
    assert body["evidence_created"] is True
