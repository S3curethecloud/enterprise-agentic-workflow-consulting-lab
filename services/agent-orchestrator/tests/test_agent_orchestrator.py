import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import AGENT_REGISTRY_PATH, EVIDENCE_RECORDS_PATH, app


client = TestClient(app)


def reset_evidence_store():
    Path(EVIDENCE_RECORDS_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(EVIDENCE_RECORDS_PATH).write_text("[]", encoding="utf-8")


def seed_agent_registry():
    Path(AGENT_REGISTRY_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(AGENT_REGISTRY_PATH).write_text(
        json.dumps(
            [
                {
                    "agent_id": "agent-policy-support-v1",
                    "agent_name": "policy-support-agent",
                    "version": "1.0.0",
                    "owner": "ai-platform-team",
                    "description": "Agent that supports policy lookup, source grounding, and controlled ticket creation.",
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
                    "risk_tier": "high",
                    "data_access_scope": [
                        "public",
                        "internal",
                        "confidential"
                    ],
                    "status": "active",
                    "created_at": "2026-07-02T00:00:00+00:00",
                    "updated_at": "2026-07-02T00:00:00+00:00"
                },
                {
                    "agent_id": "agent-disabled-v1",
                    "agent_name": "disabled-demo-agent",
                    "version": "1.0.0",
                    "owner": "ai-platform-team",
                    "description": "Disabled demo agent used to validate lifecycle enforcement.",
                    "capabilities": [
                        "policy_lookup"
                    ],
                    "allowed_tools": [
                        "search_internal_docs"
                    ],
                    "risk_tier": "low",
                    "data_access_scope": [
                        "public",
                        "internal"
                    ],
                    "status": "disabled",
                    "created_at": "2026-07-02T00:00:00+00:00",
                    "updated_at": "2026-07-02T00:00:00+00:00"
                },
                {
                    "agent_id": "agent-low-risk-v1",
                    "agent_name": "low-risk-reader-agent",
                    "version": "1.0.0",
                    "owner": "ai-platform-team",
                    "description": "Low-risk reader agent.",
                    "capabilities": [
                        "policy_lookup"
                    ],
                    "allowed_tools": [
                        "search_internal_docs"
                    ],
                    "risk_tier": "low",
                    "data_access_scope": [
                        "public",
                        "internal"
                    ],
                    "status": "active",
                    "created_at": "2026-07-02T00:00:00+00:00",
                    "updated_at": "2026-07-02T00:00:00+00:00"
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def reset_all():
    reset_evidence_store()
    seed_agent_registry()


def read_evidence_records():
    return json.loads(Path(EVIDENCE_RECORDS_PATH).read_text(encoding="utf-8"))


def base_payload(**overrides):
    payload = {
        "agent_id": "agent-policy-support-v1",
        "user_id": "ola.consultant",
        "role": "security_architect",
        "department": "ai_platform",
        "request": "Search internal AI policy for ticket creation guidance.",
        "action": "search_internal_docs",
        "tool_name": "search_internal_docs",
        "data_classification": "internal",
        "user_region": "us",
        "data_region": "us",
        "risk_tier": "low",
        "approval_present": False,
        "pii_detected": False,
        "business_justification": "Policy research"
    }
    payload.update(overrides)
    return payload


def test_health_check():
    reset_all()

    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "agent-orchestrator"
    assert body["status"] == "healthy"
    assert body["workflow"] == "gateway-rag-policy-mcp-evidence-trace-telemetry"


def test_active_authorized_agent_workflow_persists_evidence():
    reset_all()

    response = client.post("/agent/workflow", json=base_payload())
    assert response.status_code == 200

    body = response.json()
    assert body["agent_id"] == "agent-policy-support-v1"
    assert body["agent_name"] == "policy-support-agent"
    assert body["agent_version"] == "1.0.0"
    assert body["agent_registry_decision"] == "ALLOW"
    assert body["agent_registry_status"] == "agent_registry_allowed"
    assert body["final_decision"] == "ALLOW"
    assert body["final_status"] == "workflow_completed"
    assert body["tool_invoked"] is True
    assert body["evidence_persisted"] is True
    assert body["stage_event_count"] == 5
    assert len(body["trace_timeline"]) == 5

    records = read_evidence_records()
    assert len(records) == 1
    assert records[0]["metadata"]["agent_id"] == "agent-policy-support-v1"
    assert records[0]["metadata"]["agent_registry_decision"] == "ALLOW"
    assert records[0]["metadata"]["stage_event_count"] == 5


def test_missing_agent_denies_workflow():
    reset_all()

    response = client.post("/agent/workflow", json=base_payload(agent_id="agent-missing"))
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "DENY"
    assert body["agent_registry_status"] == "agent_not_found"
    assert body["final_decision"] == "DENY"
    assert body["final_status"] == "workflow_denied"
    assert body["tool_invoked"] is False
    assert body["agent_name"] is None

    records = read_evidence_records()
    assert records[0]["policy_id"] == "REGISTRY-AGENT_NOT_FOUND"


def test_disabled_agent_denies_workflow():
    reset_all()

    response = client.post("/agent/workflow", json=base_payload(agent_id="agent-disabled-v1"))
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "DENY"
    assert body["agent_registry_status"] == "agent_not_active"
    assert body["final_decision"] == "DENY"
    assert body["tool_invoked"] is False
    assert body["agent_name"] == "disabled-demo-agent"


def test_tool_not_allowed_denies_workflow():
    reset_all()

    response = client.post(
        "/agent/workflow",
        json=base_payload(
            agent_id="agent-low-risk-v1",
            tool_name="create_ticket",
            action="create_ticket",
            request="Create a ticket.",
        ),
    )
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "DENY"
    assert body["agent_registry_status"] == "tool_not_allowed"
    assert body["final_decision"] == "DENY"
    assert body["tool_invoked"] is False


def test_data_scope_not_allowed_denies_workflow():
    reset_all()

    response = client.post(
        "/agent/workflow",
        json=base_payload(
            agent_id="agent-low-risk-v1",
            data_classification="confidential",
            request="Read confidential customer data.",
        ),
    )
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "DENY"
    assert body["agent_registry_status"] == "data_scope_not_allowed"
    assert body["final_decision"] == "DENY"
    assert body["tool_invoked"] is False


def test_risk_tier_exceeded_denies_workflow():
    reset_all()

    response = client.post(
        "/agent/workflow",
        json=base_payload(
            agent_id="agent-low-risk-v1",
            risk_tier="high",
            request="Search internal policy for high risk workflow.",
        ),
    )
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "DENY"
    assert body["agent_registry_status"] == "risk_tier_exceeded"
    assert body["final_decision"] == "DENY"
    assert body["tool_invoked"] is False


def test_confidential_customer_data_requires_approval_after_registry_allows():
    reset_all()

    response = client.post(
        "/agent/workflow",
        json=base_payload(
            request="Read confidential customer data for support investigation.",
            action="read_customer_record",
            tool_name="query_policy",
            data_classification="confidential",
            risk_tier="medium",
            approval_present=False,
            business_justification="Support investigation",
        ),
    )
    assert response.status_code == 200

    body = response.json()
    assert body["agent_registry_decision"] == "ALLOW"
    assert body["final_decision"] == "APPROVAL_REQUIRED"
    assert body["final_status"] == "workflow_waiting_for_approval"
    assert body["tool_invoked"] is False


def test_trace_timeline_starts_with_agent_registry_event():
    reset_all()

    response = client.post("/agent/workflow", json=base_payload())
    assert response.status_code == 200

    body = response.json()
    timeline = body["trace_timeline"]

    assert body["stage_event_count"] == 5
    assert timeline[0]["stage_name"] == "agent_registry_enforcement"
    assert timeline[0]["event_type"] == "agent_authorization_check"

    stage_names = [event["stage_name"] for event in timeline]
    assert stage_names == [
        "agent_registry_enforcement",
        "ai_gateway",
        "rag_retrieval",
        "policy_evaluation",
        "mcp_tool_invocation",
    ]

    assert body["total_latency_ms"] == sum(event["latency_ms"] for event in timeline) + body["performance_telemetry"]["evidence_latency_ms"]


def test_cost_and_performance_telemetry_still_present():
    reset_all()

    response = client.post(
        "/agent/workflow",
        json=base_payload(
            request="Create a ticket after policy review for customer support workflow.",
            action="create_ticket",
            tool_name="create_ticket",
            data_classification="confidential",
            risk_tier="high",
            approval_present=True,
            business_justification="Approved policy review",
        ),
    )
    assert response.status_code == 200

    body = response.json()
    assert body["performance_telemetry"]["total_latency_ms"] > 0
    assert body["performance_slo_status"] == "within_slo"
    assert body["cost_telemetry"]["total_tokens"] > 0
    assert body["evidence_summary"]["agent_registry_decision"] == "ALLOW"
