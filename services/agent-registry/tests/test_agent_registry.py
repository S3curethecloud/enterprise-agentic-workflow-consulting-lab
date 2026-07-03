import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import AGENTS_PATH, app


client = TestClient(app)


def reset_agent_registry():
    Path(AGENTS_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(AGENTS_PATH).write_text("[]", encoding="utf-8")


def sample_agent_payload(
    agent_name="policy-support-agent",
    version="1.0.0",
    status="active",
    risk_tier="medium",
):
    return {
        "agent_name": agent_name,
        "version": version,
        "owner": "ai-platform-team",
        "description": "Agent that supports policy lookup and controlled ticket creation.",
        "capabilities": [
            "policy_lookup",
            "source_grounding",
            "ticket_creation"
        ],
        "allowed_tools": [
            "search_internal_docs",
            "query_policy",
            "create_ticket"
        ],
        "risk_tier": risk_tier,
        "data_access_scope": [
            "internal",
            "confidential"
        ],
        "status": status
    }


def read_agents():
    return json.loads(Path(AGENTS_PATH).read_text(encoding="utf-8"))


def test_health_check():
    reset_agent_registry()

    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "agent-registry"
    assert body["status"] == "healthy"
    assert body["agent_count"] == 0


def test_create_agent():
    reset_agent_registry()

    response = client.post("/agents", json=sample_agent_payload())
    assert response.status_code == 200

    body = response.json()
    assert body["agent_id"].startswith("agent-")
    assert body["agent_name"] == "policy-support-agent"
    assert body["version"] == "1.0.0"
    assert body["owner"] == "ai-platform-team"
    assert body["risk_tier"] == "medium"
    assert body["status"] == "active"
    assert "query_policy" in body["allowed_tools"]

    stored_agents = read_agents()
    assert len(stored_agents) == 1
    assert stored_agents[0]["agent_id"] == body["agent_id"]


def test_duplicate_agent_name_and_version_returns_409():
    reset_agent_registry()

    payload = sample_agent_payload()
    first_response = client.post("/agents", json=payload)
    second_response = client.post("/agents", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_list_agents():
    reset_agent_registry()

    client.post("/agents", json=sample_agent_payload("policy-support-agent", "1.0.0", "active", "medium"))
    client.post("/agents", json=sample_agent_payload("incident-triage-agent", "1.0.0", "draft", "high"))

    response = client.get("/agents")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 2
    assert len(body["agents"]) == 2


def test_filter_agents_by_status():
    reset_agent_registry()

    client.post("/agents", json=sample_agent_payload("policy-support-agent", "1.0.0", "active", "medium"))
    client.post("/agents", json=sample_agent_payload("incident-triage-agent", "1.0.0", "draft", "high"))

    response = client.get("/agents?status=active")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 1
    assert body["agents"][0]["status"] == "active"


def test_filter_agents_by_risk_tier():
    reset_agent_registry()

    client.post("/agents", json=sample_agent_payload("policy-support-agent", "1.0.0", "active", "medium"))
    client.post("/agents", json=sample_agent_payload("incident-triage-agent", "1.0.0", "draft", "high"))

    response = client.get("/agents?risk_tier=high")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 1
    assert body["agents"][0]["risk_tier"] == "high"


def test_get_agent_by_id():
    reset_agent_registry()

    create_response = client.post("/agents", json=sample_agent_payload())
    agent_id = create_response.json()["agent_id"]

    response = client.get(f"/agents/{agent_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["agent_id"] == agent_id
    assert body["agent_name"] == "policy-support-agent"


def test_get_missing_agent_returns_404():
    reset_agent_registry()

    response = client.get("/agents/agent-missing")
    assert response.status_code == 404


def test_update_agent_status():
    reset_agent_registry()

    create_response = client.post("/agents", json=sample_agent_payload(status="draft"))
    agent_id = create_response.json()["agent_id"]

    response = client.patch(f"/agents/{agent_id}/status", json={"status": "active"})
    assert response.status_code == 200

    body = response.json()
    assert body["agent_id"] == agent_id
    assert body["status"] == "active"
    assert body["updated_at"] >= body["created_at"]

    stored_agents = read_agents()
    assert stored_agents[0]["status"] == "active"


def test_update_missing_agent_status_returns_404():
    reset_agent_registry()

    response = client.patch("/agents/agent-missing/status", json={"status": "disabled"})
    assert response.status_code == 404
