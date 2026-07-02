from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "ai-gateway"
    assert body["status"] == "healthy"


def test_gateway_request_medium_risk():
    payload = {
        "user_id": "ola.consultant",
        "role": "security_architect",
        "department": "ai_platform",
        "request": "Search the internal AI policy and create a ticket if this workflow is non-compliant.",
        "data_region": "us",
        "risk_tier": "medium",
    }

    response = client.post("/gateway/request", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["user_id"] == "ola.consultant"
    assert body["risk_label"] in ["medium", "high"]
    assert body["policy_handoff_required"] is True
    assert body["evidence_created"] is True
    assert body["status"] == "accepted_for_agent_processing"


def test_gateway_request_low_risk():
    payload = {
        "user_id": "demo.user",
        "role": "reader",
        "department": "training",
        "request": "Summarize what an AI gateway does.",
        "data_region": "us",
        "risk_tier": "low",
    }

    response = client.post("/gateway/request", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["risk_label"] in ["low", "medium"]
    assert body["evidence_created"] is True
