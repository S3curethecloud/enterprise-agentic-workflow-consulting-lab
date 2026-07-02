from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
TOOL_REGISTRY_PATH = BASE_DIR / "registry" / "tools.json"
CUSTOMER_RECORDS_PATH = BASE_DIR / "data" / "customer-records.json"
TICKETS_PATH = BASE_DIR / "data" / "tickets.json"


app = FastAPI(
    title="MCP-Style Tool Server",
    description="Local MCP-style tool server for enterprise agentic workflow consulting lab.",
    version="0.1.0",
)


class ToolInvocationRequest(BaseModel):
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    trace_id: str | None = Field(default=None, examples=["trace-123"])
    arguments: Dict[str, Any]


class ToolInvocationResponse(BaseModel):
    invocation_id: str
    trace_id: str
    tool_name: str
    user_id: str
    risk_tier: str
    requires_policy_check: bool
    requires_approval: bool
    policy_status: str
    execution_status: str
    result: Dict[str, Any]
    evidence_created: bool
    timestamp: str


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_tools() -> list[dict]:
    return read_json(TOOL_REGISTRY_PATH)


def get_tool(tool_name: str) -> dict:
    for tool in load_tools():
        if tool["tool_name"] == tool_name:
            return tool
    raise HTTPException(status_code=404, detail=f"Tool not found: {tool_name}")


def validate_required_arguments(tool: dict, arguments: dict):
    required_keys = set(tool["input_schema"].keys())
    provided_keys = set(arguments.keys())
    missing = required_keys - provided_keys

    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Missing required tool arguments.",
                "missing": sorted(missing),
            },
        )


def policy_status_for_tool(tool: dict, role: str) -> str:
    if tool["requires_approval"]:
        return "approval_required"

    if tool["requires_policy_check"]:
        return "policy_check_required"

    return "policy_not_required"


def execute_search_internal_docs(arguments: dict) -> dict:
    query = arguments["query"]
    max_results = arguments.get("max_results", 3)

    return {
        "message": "Search request accepted by MCP-style tool layer.",
        "query": query,
        "max_results": max_results,
        "note": "This tool currently simulates document search. Phase 5 can integrate this with the RAG service.",
    }


def execute_query_policy(arguments: dict) -> dict:
    action = arguments["action"]
    data_classification = arguments["data_classification"]
    user_role = arguments["user_role"]

    if data_classification in ["restricted", "confidential"]:
        decision = "approval_required"
    elif action.lower() in ["delete", "modify_production", "disable_control"]:
        decision = "deny"
    else:
        decision = "allow"

    return {
        "action": action,
        "data_classification": data_classification,
        "user_role": user_role,
        "decision": decision,
        "reason": "Policy simulation based on action and data classification.",
    }


def execute_read_customer_record(arguments: dict) -> dict:
    customer_id = arguments["customer_id"]
    purpose = arguments["purpose"]

    records = read_json(CUSTOMER_RECORDS_PATH)
    record = next((item for item in records if item["customer_id"] == customer_id), None)

    if not record:
        return {
            "found": False,
            "customer_id": customer_id,
            "message": "Customer record not found.",
        }

    return {
        "found": True,
        "customer_id": customer_id,
        "purpose": purpose,
        "record": record,
        "warning": "This is synthetic lab data. Real customer data access would require policy approval.",
    }


def execute_create_ticket(arguments: dict) -> dict:
    tickets = read_json(TICKETS_PATH)

    ticket = {
        "ticket_id": f"ticket-{uuid4()}",
        "title": arguments["title"],
        "severity": arguments["severity"],
        "description": arguments["description"],
        "status": "created",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    tickets.append(ticket)
    write_json(TICKETS_PATH, tickets)

    return ticket


def execute_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name == "search_internal_docs":
        return execute_search_internal_docs(arguments)

    if tool_name == "query_policy":
        return execute_query_policy(arguments)

    if tool_name == "read_customer_record":
        return execute_read_customer_record(arguments)

    if tool_name == "create_ticket":
        return execute_create_ticket(arguments)

    raise HTTPException(status_code=404, detail=f"Execution handler not found for tool: {tool_name}")


@app.get("/health")
def health_check():
    return {
        "service": "mcp-server",
        "status": "healthy",
        "tool_count": len(load_tools()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tools")
def list_tools():
    return {
        "tools": load_tools(),
        "count": len(load_tools()),
    }


@app.get("/tools/{tool_name}")
def describe_tool(tool_name: str):
    return get_tool(tool_name)


@app.post("/tools/{tool_name}/invoke", response_model=ToolInvocationResponse)
def invoke_tool(tool_name: str, payload: ToolInvocationRequest):
    tool = get_tool(tool_name)
    validate_required_arguments(tool, payload.arguments)

    trace_id = payload.trace_id or f"trace-{uuid4()}"
    policy_status = policy_status_for_tool(tool, payload.role)

    result = execute_tool(tool_name, payload.arguments)

    return ToolInvocationResponse(
        invocation_id=f"invoke-{uuid4()}",
        trace_id=trace_id,
        tool_name=tool_name,
        user_id=payload.user_id,
        risk_tier=tool["risk_tier"],
        requires_policy_check=tool["requires_policy_check"],
        requires_approval=tool["requires_approval"],
        policy_status=policy_status,
        execution_status="completed",
        result=result,
        evidence_created=True,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
