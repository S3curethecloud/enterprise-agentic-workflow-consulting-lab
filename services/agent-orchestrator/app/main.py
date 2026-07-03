from datetime import datetime, timezone
from typing import Any, Dict, Literal
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


Decision = Literal["ALLOW", "DENY", "REDACT", "APPROVAL_REQUIRED"]


app = FastAPI(
    title="Local Agent Workflow Orchestrator",
    description="End-to-end local agent workflow simulation for enterprise agentic AI.",
    version="0.1.0",
)


class AgentWorkflowRequest(BaseModel):
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    department: str = Field(default="ai_platform", examples=["ai_platform"])
    request: str = Field(..., examples=["Search policy and create a ticket if confidential data access requires approval."])
    action: str = Field(default="search_internal_docs", examples=["create_ticket"])
    tool_name: str = Field(default="search_internal_docs", examples=["create_ticket"])
    data_classification: Literal["public", "internal", "confidential", "restricted"] = "internal"
    user_region: str = Field(default="us", examples=["us"])
    data_region: str = Field(default="us", examples=["us"])
    risk_tier: Literal["low", "medium", "high"] = "medium"
    approval_present: bool = False
    pii_detected: bool = False
    business_justification: str | None = Field(default=None, examples=["Policy review"])


class WorkflowStage(BaseModel):
    stage_name: str
    status: str
    details: Dict[str, Any]


class AgentWorkflowResponse(BaseModel):
    workflow_id: str
    trace_id: str
    user_id: str
    final_decision: Decision
    final_status: str
    grounded_context_found: bool
    tool_invoked: bool
    tool_name: str | None
    stages: list[WorkflowStage]
    evidence_summary: Dict[str, Any]
    timestamp: str


def score_gateway_risk(request_text: str, risk_tier: str) -> tuple[int, str, bool, str]:
    lowered = request_text.lower()
    score = 20

    if risk_tier == "medium":
        score += 25
    elif risk_tier == "high":
        score += 50

    sensitive_terms = [
        "customer",
        "confidential",
        "restricted",
        "credential",
        "production",
        "delete",
        "disable",
        "override",
        "ticket",
    ]

    for term in sensitive_terms:
        if term in lowered:
            score += 8

    score = min(score, 100)

    if score >= 70:
        risk_label = "high"
    elif score >= 40:
        risk_label = "medium"
    else:
        risk_label = "low"

    policy_handoff_required = risk_label in ["medium", "high"]

    if risk_label == "high":
        route = "agent_runtime_with_policy_review"
    elif risk_label == "medium":
        route = "agent_runtime"
    else:
        route = "direct_response_or_agent_runtime"

    return score, risk_label, policy_handoff_required, route


def retrieve_grounded_context(query: str) -> tuple[bool, float, list[dict]]:
    lowered = query.lower()

    sources = []

    if "policy" in lowered or "confidential" in lowered or "customer" in lowered:
        sources.append(
            {
                "source_file": "customer-data-handling-policy.md",
                "snippet": "Customer data access requires role validation, data classification check, policy decision, evidence record, and output review.",
                "classification_hint": "confidential",
                "score": 85,
            }
        )

    if "ticket" in lowered or "incident" in lowered or "approval" in lowered:
        sources.append(
            {
                "source_file": "internal-ai-policy.md",
                "snippet": "AI agents must produce audit evidence and require human approval for high-risk actions.",
                "classification_hint": "internal",
                "score": 72,
            }
        )

    if not sources:
        return False, 0.0, []

    confidence = min(sources[0]["score"] / 100, 0.95)
    return True, round(confidence, 2), sources[:3]


def contains_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "bypass policy",
        "override policy",
        "disable guardrails",
        "reveal secrets",
        "show me the system prompt",
        "act as admin",
        "jailbreak",
    ]
    return any(phrase in lowered for phrase in suspicious_phrases)


def is_region_mismatch(user_region: str, data_region: str) -> bool:
    if data_region.lower() == "global":
        return False
    return user_region.lower() != data_region.lower()


def evaluate_policy(payload: AgentWorkflowRequest) -> tuple[Decision, str, str]:
    if contains_prompt_injection(payload.request):
        return (
            "DENY",
            "POL-AI-001",
            "Prompt injection or policy bypass language detected.",
        )

    if is_region_mismatch(payload.user_region, payload.data_region):
        return (
            "DENY",
            "POL-REGION-001",
            "User region and data region are incompatible.",
        )

    if payload.data_classification == "restricted" and not payload.approval_present:
        return (
            "DENY",
            "POL-DATA-002",
            "Restricted data access requires explicit approval before execution.",
        )

    if payload.pii_detected:
        return (
            "REDACT",
            "POL-PII-001",
            "PII detected and must be redacted before response is returned.",
        )

    if payload.risk_tier == "high" and not payload.approval_present:
        return (
            "APPROVAL_REQUIRED",
            "POL-TOOL-001",
            "High-risk tool or action requires approval before execution.",
        )

    if payload.data_classification == "confidential" and not payload.approval_present:
        return (
            "APPROVAL_REQUIRED",
            "POL-DATA-001",
            "Confidential data access requires approval before execution.",
        )

    return (
        "ALLOW",
        "POL-DEFAULT-ALLOW",
        "No blocking, redaction, or approval-required policy matched.",
    )


def invoke_tool_if_allowed(tool_name: str, payload: AgentWorkflowRequest) -> tuple[bool, dict]:
    if tool_name == "search_internal_docs":
        return True, {
            "tool_name": tool_name,
            "result": "Internal document search completed through controlled tool contract.",
            "query": payload.request,
        }

    if tool_name == "query_policy":
        return True, {
            "tool_name": tool_name,
            "result": "Policy query completed through controlled tool contract.",
            "action": payload.action,
            "data_classification": payload.data_classification,
        }

    if tool_name == "create_ticket":
        return True, {
            "tool_name": tool_name,
            "ticket_id": f"ticket-{uuid4()}",
            "status": "created",
            "title": "Agent workflow policy review",
            "severity": payload.risk_tier,
        }

    if tool_name == "read_customer_record":
        return True, {
            "tool_name": tool_name,
            "customer_id": "cust-001",
            "status": "read_simulated",
            "warning": "Synthetic lab response only. Real access requires enterprise authorization.",
        }

    return False, {
        "tool_name": tool_name,
        "error": "Tool not found in orchestrator simulation.",
    }


@app.get("/health")
def health_check():
    return {
        "service": "agent-orchestrator",
        "status": "healthy",
        "workflow": "gateway-rag-policy-mcp",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/agent/workflow", response_model=AgentWorkflowResponse)
def agent_workflow(payload: AgentWorkflowRequest):
    workflow_id = f"workflow-{uuid4()}"
    trace_id = f"trace-{uuid4()}"
    stages: list[WorkflowStage] = []

    risk_score, risk_label, policy_handoff_required, routing_decision = score_gateway_risk(
        payload.request,
        payload.risk_tier,
    )

    stages.append(
        WorkflowStage(
            stage_name="ai_gateway",
            status="completed",
            details={
                "prompt_risk_score": risk_score,
                "risk_label": risk_label,
                "policy_handoff_required": policy_handoff_required,
                "routing_decision": routing_decision,
                "evidence_created": True,
            },
        )
    )

    grounded_context_found, confidence, sources = retrieve_grounded_context(payload.request)

    stages.append(
        WorkflowStage(
            stage_name="rag_retrieval",
            status="completed",
            details={
                "grounded_context_found": grounded_context_found,
                "confidence": confidence,
                "source_count": len(sources),
                "sources": sources,
                "evidence_created": True,
            },
        )
    )

    decision, policy_id, reason = evaluate_policy(payload)

    stages.append(
        WorkflowStage(
            stage_name="policy_evaluation",
            status="completed",
            details={
                "decision": decision,
                "policy_id": policy_id,
                "reason": reason,
                "allowed_to_execute": decision == "ALLOW",
                "requires_approval": decision == "APPROVAL_REQUIRED",
                "requires_redaction": decision == "REDACT",
                "evidence_created": True,
            },
        )
    )

    tool_invoked = False
    tool_result: dict[str, Any] = {}

    if decision == "ALLOW":
        tool_invoked, tool_result = invoke_tool_if_allowed(payload.tool_name, payload)
        tool_status = "completed" if tool_invoked else "failed"
    else:
        tool_status = "skipped"
        tool_result = {
            "message": "Tool invocation skipped because policy decision did not allow execution.",
            "decision": decision,
        }

    stages.append(
        WorkflowStage(
            stage_name="mcp_tool_invocation",
            status=tool_status,
            details={
                "tool_name": payload.tool_name,
                "tool_invoked": tool_invoked,
                "result": tool_result,
                "evidence_created": True,
            },
        )
    )

    if decision == "ALLOW":
        final_status = "workflow_completed"
    elif decision == "APPROVAL_REQUIRED":
        final_status = "workflow_waiting_for_approval"
    elif decision == "REDACT":
        final_status = "workflow_requires_redaction"
    else:
        final_status = "workflow_denied"

    evidence_summary = {
        "workflow_id": workflow_id,
        "trace_id": trace_id,
        "gateway_evidence": True,
        "rag_evidence": True,
        "policy_evidence": True,
        "tool_evidence": True,
        "source_count": len(sources),
        "final_policy_id": policy_id,
        "final_decision": decision,
    }

    return AgentWorkflowResponse(
        workflow_id=workflow_id,
        trace_id=trace_id,
        user_id=payload.user_id,
        final_decision=decision,
        final_status=final_status,
        grounded_context_found=grounded_context_found,
        tool_invoked=tool_invoked,
        tool_name=payload.tool_name if tool_invoked else None,
        stages=stages,
        evidence_summary=evidence_summary,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
