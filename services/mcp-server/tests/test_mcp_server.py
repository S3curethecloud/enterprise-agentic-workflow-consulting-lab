from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "mcp-server"
    assert body["status"] == "healthy"
    assert body["tool_count"] == 4


def test_list_tools():
    response = client.get("/tools")
    assert response.status_code == 200

    body = response.json()
    assert body["count"] == 4

    tool_names = [tool["tool_name"] for tool in body["tools"]]
    assert "search_internal_docs" in tool_names
    assert "query_policy" in tool_names
    assert "read_customer_record" in tool_names
    assert "create_ticket" in tool_names


def test_describe_tool():
    response = client.get("/tools/read_customer_record")
    assert response.status_code == 200

    body = response.json()
    assert body["tool_name"] == "read_customer_record"
    assert body["risk_tier"] == "high"
    assert body["requires_policy_check"] is True
    assert body["requires_approval"] is True


def test_invoke_query_policy_tool():
    payload = {
        "user_id": "ola.consultant",
        "role": "security_architect",
        "trace_id": "trace-test-001",
        "arguments": {
            "action": "read",
            "data_classification": "confidential",
            "user_role": "security_architect"
        }
    }

    response = client.post("/tools/query_policy/invoke", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["tool_name"] == "query_policy"
    assert body["requires_policy_check"] is True
    assert body["policy_status"] == "policy_check_required"
    assert body["result"]["decision"] == "approval_required"
    assert body["evidence_created"] is True


def test_invoke_read_customer_record_tool():
    payload = {
        "user_id": "ola.consultant",
        "role": "security_architect",
        "trace_id": "trace-test-002",
        "arguments": {
            "customer_id": "cust-001",
            "purpose": "support investigation"
        }
    }

    response = client.post("/tools/read_customer_record/invoke", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["tool_name"] == "read_customer_record"
    assert body["risk_tier"] == "high"
    assert body["requires_approval"] is True
    assert body["policy_status"] == "approval_required"
    assert body["result"]["found"] is True
    assert body["evidence_created"] is True


def test_invoke_create_ticket_tool():
    payload = {
        "user_id": "ola.consultant",
        "role": "security_architect",
        "trace_id": "trace-test-003",
        "arguments": {
            "title": "AI policy review required",
            "severity": "medium",
            "description": "Agent workflow requires policy review before accessing confidential data."
        }
    }

    response = client.post("/tools/create_ticket/invoke", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["tool_name"] == "create_ticket"
    assert body["risk_tier"] == "medium"
    assert body["requires_policy_check"] is True
    assert body["result"]["status"] == "created"
    assert body["evidence_created"] is True


def test_missing_required_argument():
    payload = {
        "user_id": "ola.consultant",
        "role": "security_architect",
        "trace_id": "trace-test-004",
        "arguments": {
            "customer_id": "cust-001"
        }
    }

    response = client.post("/tools/read_customer_record/invoke", json=payload)
    assert response.status_code == 400

    body = response.json()
    assert "missing" in body["detail"]
    assert "purpose" in body["detail"]["missing"]
