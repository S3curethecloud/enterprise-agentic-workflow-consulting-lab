import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import EVIDENCE_RECORDS_PATH, app


client = TestClient(app)


def reset_evidence_store():
    Path(EVIDENCE_RECORDS_PATH).write_text("[]", encoding="utf-8")


def sample_payload(workflow_id="workflow-test-001"):
    return {
        "workflow_id": workflow_id,
        "trace_id": "trace-test-001",
        "user_id": "ola.consultant",
        "request": "Create a ticket after policy review for customer support workflow.",
        "final_decision": "ALLOW",
        "final_status": "workflow_completed",
        "grounded_context_found": True,
        "source_count": 2,
        "policy_id": "POL-DEFAULT-ALLOW",
        "tool_name": "create_ticket",
        "tool_invoked": True,
        "stages": [
            {
                "stage_name": "ai_gateway",
                "status": "completed",
                "details": {
                    "prompt_risk_score": 100,
                    "risk_label": "high",
                    "evidence_created": True
                }
            },
            {
                "stage_name": "rag_retrieval",
                "status": "completed",
                "details": {
                    "grounded_context_found": True,
                    "confidence": 0.85,
                    "source_count": 2,
                    "evidence_created": True
                }
            },
            {
                "stage_name": "policy_evaluation",
                "status": "completed",
                "details": {
                    "decision": "ALLOW",
                    "policy_id": "POL-DEFAULT-ALLOW",
                    "allowed_to_execute": True,
                    "evidence_created": True
                }
            },
            {
                "stage_name": "mcp_tool_invocation",
                "status": "completed",
                "details": {
                    "tool_name": "create_ticket",
                    "tool_invoked": True,
                    "evidence_created": True
                }
            }
        ],
        "metadata": {
            "lab_phase": "phase-07",
            "environment": "local"
        }
    }


def test_health_check():
    reset_evidence_store()

    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "evidence-store"
    assert body["status"] == "healthy"
    assert body["record_count"] == 0


def test_create_evidence_record():
    reset_evidence_store()

    response = client.post("/evidence/records", json=sample_payload())
    assert response.status_code == 200

    body = response.json()
    assert body["record_id"].startswith("evidence-")
    assert body["workflow_id"] == "workflow-test-001"
    assert body["trace_id"] == "trace-test-001"
    assert body["final_decision"] == "ALLOW"
    assert body["final_status"] == "workflow_completed"
    assert body["tool_invoked"] is True
    assert len(body["stages"]) == 4

    stored_records = json.loads(Path(EVIDENCE_RECORDS_PATH).read_text(encoding="utf-8"))
    assert len(stored_records) == 1
    assert stored_records[0]["workflow_id"] == "workflow-test-001"


def test_list_evidence_records():
    reset_evidence_store()

    client.post("/evidence/records", json=sample_payload("workflow-test-001"))
    client.post("/evidence/records", json=sample_payload("workflow-test-002"))

    response = client.get("/evidence/records")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 2
    assert len(body["records"]) == 2


def test_get_evidence_record_by_id():
    reset_evidence_store()

    create_response = client.post("/evidence/records", json=sample_payload())
    record_id = create_response.json()["record_id"]

    response = client.get(f"/evidence/records/{record_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["record_id"] == record_id
    assert body["workflow_id"] == "workflow-test-001"


def test_get_missing_evidence_record_returns_404():
    reset_evidence_store()

    response = client.get("/evidence/records/evidence-missing")
    assert response.status_code == 404


def test_get_records_by_workflow_id():
    reset_evidence_store()

    client.post("/evidence/records", json=sample_payload("workflow-shared"))
    client.post("/evidence/records", json=sample_payload("workflow-shared"))
    client.post("/evidence/records", json=sample_payload("workflow-other"))

    response = client.get("/evidence/workflows/workflow-shared")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 2
    assert all(record["workflow_id"] == "workflow-shared" for record in body["records"])
