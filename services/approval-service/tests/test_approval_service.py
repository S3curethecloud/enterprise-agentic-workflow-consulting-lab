import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import APPROVALS_PATH, app


client = TestClient(app)


def reset_approval_store():
    Path(APPROVALS_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(APPROVALS_PATH).write_text("[]", encoding="utf-8")


def read_approvals():
    return json.loads(Path(APPROVALS_PATH).read_text(encoding="utf-8"))


def sample_approval_payload():
    return {
        "workflow_id": "workflow-review-001",
        "trace_id": "trace-review-001",
        "agent_id": "agent-policy-support-v1",
        "requested_by": "ola.consultant",
        "approver": "ai-governance-reviewer",
        "review_reason": "Responsible AI review required before workflow can proceed.",
        "rai_decision": "REVIEW_REQUIRED",
        "policy_decision": "APPROVAL_REQUIRED",
        "risk_tier": "medium",
        "data_classification": "confidential",
        "requested_action": "read_customer_record",
        "requested_tool": "query_policy",
    }


def test_health_check():
    reset_approval_store()

    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "approval-service"
    assert body["status"] == "healthy"
    assert body["approval_count"] == 0


def test_create_approval_request():
    reset_approval_store()

    response = client.post("/approvals", json=sample_approval_payload())
    assert response.status_code == 200

    body = response.json()
    assert body["approval_id"].startswith("approval-")
    assert body["workflow_id"] == "workflow-review-001"
    assert body["trace_id"] == "trace-review-001"
    assert body["agent_id"] == "agent-policy-support-v1"
    assert body["approval_status"] == "pending"
    assert body["decision_reason"] is None
    assert body["decided_at"] is None

    approvals = read_approvals()
    assert len(approvals) == 1
    assert approvals[0]["approval_id"] == body["approval_id"]


def test_list_approvals():
    reset_approval_store()

    client.post("/approvals", json=sample_approval_payload())

    response = client.get("/approvals")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 1
    assert body["approvals"][0]["approval_status"] == "pending"


def test_filter_pending_approvals():
    reset_approval_store()

    client.post("/approvals", json=sample_approval_payload())

    response = client.get("/approvals?status=pending")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 1
    assert body["approvals"][0]["approval_status"] == "pending"


def test_get_approval_by_id():
    reset_approval_store()

    create_response = client.post("/approvals", json=sample_approval_payload())
    approval_id = create_response.json()["approval_id"]

    response = client.get(f"/approvals/{approval_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["approval_id"] == approval_id
    assert body["workflow_id"] == "workflow-review-001"


def test_get_missing_approval_returns_404():
    reset_approval_store()

    response = client.get("/approvals/approval-missing")
    assert response.status_code == 404


def test_approve_pending_request():
    reset_approval_store()

    create_response = client.post("/approvals", json=sample_approval_payload())
    approval_id = create_response.json()["approval_id"]

    response = client.patch(
        f"/approvals/{approval_id}/approve",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Approved because source grounding and business justification were sufficient.",
        },
    )
    assert response.status_code == 200

    body = response.json()
    assert body["approval_status"] == "approved"
    assert body["decision_reason"] == "Approved because source grounding and business justification were sufficient."
    assert body["decided_at"] is not None

    approvals = read_approvals()
    assert approvals[0]["approval_status"] == "approved"


def test_reject_pending_request():
    reset_approval_store()

    create_response = client.post("/approvals", json=sample_approval_payload())
    approval_id = create_response.json()["approval_id"]

    response = client.patch(
        f"/approvals/{approval_id}/reject",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Rejected because the request lacked sufficient justification.",
        },
    )
    assert response.status_code == 200

    body = response.json()
    assert body["approval_status"] == "rejected"
    assert body["decision_reason"] == "Rejected because the request lacked sufficient justification."
    assert body["decided_at"] is not None


def test_cannot_approve_already_decided_request():
    reset_approval_store()

    create_response = client.post("/approvals", json=sample_approval_payload())
    approval_id = create_response.json()["approval_id"]

    approve_response = client.patch(
        f"/approvals/{approval_id}/approve",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Approved once.",
        },
    )
    second_approve_response = client.patch(
        f"/approvals/{approval_id}/approve",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Approve again.",
        },
    )

    assert approve_response.status_code == 200
    assert second_approve_response.status_code == 409


def test_cannot_reject_already_decided_request():
    reset_approval_store()

    create_response = client.post("/approvals", json=sample_approval_payload())
    approval_id = create_response.json()["approval_id"]

    reject_response = client.patch(
        f"/approvals/{approval_id}/reject",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Rejected once.",
        },
    )
    second_reject_response = client.patch(
        f"/approvals/{approval_id}/reject",
        json={
            "approver": "ai-governance-reviewer",
            "decision_reason": "Reject again.",
        },
    )

    assert reject_response.status_code == 200
    assert second_reject_response.status_code == 409
